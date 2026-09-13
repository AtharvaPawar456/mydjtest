"""
Copy schema + data from local SQLite into the Turso (libSQL) cloud database.

Uses the same HTTP connection rules as test/db-con-guide.py:
AWS Turso does not support WebSockets, so libsql:// is converted to https://.

Examples
--------
    python test/migrate_sqlite_to_turso.py --dry-run
    python test/migrate_sqlite_to_turso.py
    python test/migrate_sqlite_to_turso.py --replace
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

from dotenv import load_dotenv
from libsql_client import create_client_sync


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE = ROOT / "db.sqlite3"
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SKIP_TABLES = {"sqlite_stat1", "sqlite_stat4"}
BATCH_SIZE = 25


def assertValidIdentifier(identifier: str) -> str:
    if not IDENTIFIER_PATTERN.match(identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier!r}")
    return identifier


def toHttpUrl(databaseUrl: str) -> str:
    """Convert libsql:// or wss:// to https:// for Turso AWS endpoints."""
    if databaseUrl.startswith("libsql://"):
        return "https://" + databaseUrl[len("libsql://") :]
    if databaseUrl.startswith("wss://"):
        return "https://" + databaseUrl[len("wss://") :]
    return databaseUrl


def getTursoClient():
    databaseUrl = os.getenv("TURSO_DATABASE_URL")
    authToken = os.getenv("TURSO_AUTH_TOKEN")
    if not databaseUrl:
        raise ValueError("TURSO_DATABASE_URL is missing from .env")
    if not authToken:
        raise ValueError("TURSO_AUTH_TOKEN is missing from .env")
    return create_client_sync(url=toHttpUrl(databaseUrl), auth_token=authToken)


def quoteIdent(name: str) -> str:
    assertValidIdentifier(name)
    return f'"{name}"'


def listSqliteTables(sqliteConn: sqlite3.Connection) -> list[str]:
    rows = sqliteConn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()
    return [assertValidIdentifier(row[0]) for row in rows]


def listCreateStatements(sqliteConn: sqlite3.Connection, objectType: str) -> list[tuple[str, str]]:
    rows = sqliteConn.execute(
        """
        SELECT name, sql
        FROM sqlite_master
        WHERE type = ?
          AND sql IS NOT NULL
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """,
        (objectType,),
    ).fetchall()
    return [(assertValidIdentifier(name), sql) for name, sql in rows if sql]


def tableCount(conn, table: str) -> int:
    result = conn.execute(f"SELECT COUNT(*) FROM {quoteIdent(table)}")
    if hasattr(result, "rows"):
        return int(result.rows[0][0])
    return int(result.fetchone()[0])


def tursoTableNames(client) -> set[str]:
    result = client.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )
    return {row[0] for row in result.rows}


def printPlan(sqliteConn: sqlite3.Connection, client) -> dict[str, int]:
    tables = listSqliteTables(sqliteConn)
    remoteTables = tursoTableNames(client)
    print(f"SQLite tables: {len(tables)}")
    print(f"Turso user tables: {len(remoteTables)}")
    counts = {}
    mismatches = []
    for table in tables:
        localCount = tableCount(sqliteConn, table)
        remoteCount = tableCount(client, table) if table in remoteTables else None
        counts[table] = localCount
        remoteLabel = "missing" if remoteCount is None else str(remoteCount)
        mark = "OK" if remoteCount == localCount else "DIFF"
        print(f"  {mark:4}  sqlite={localCount:4}  turso={remoteLabel:>7}  {table}")
        if remoteCount != localCount:
            mismatches.append(table)
    return {"tables": tables, "counts": counts, "mismatches": mismatches, "remote": remoteTables}


def dropRemoteUserTables(client, tables: list[str]) -> None:
    client.execute("PRAGMA foreign_keys = OFF")
    remote = tursoTableNames(client)
    for table in reversed(tables):
        if table in remote:
            client.execute(f"DROP TABLE IF EXISTS {quoteIdent(table)}")
            print(f"Dropped Turso table {table}")
    leftover = tursoTableNames(client)
    for table in leftover:
        client.execute(f"DROP TABLE IF EXISTS {quoteIdent(table)}")
        print(f"Dropped extra Turso table {table}")


def createSchema(sqliteConn: sqlite3.Connection, client) -> None:
    client.execute("PRAGMA foreign_keys = OFF")
    for name, sql in listCreateStatements(sqliteConn, "table"):
        if name in SKIP_TABLES:
            continue
        client.execute(sql)
        print(f"Created table {name}")
    for name, sql in listCreateStatements(sqliteConn, "index"):
        client.execute(sql)
        print(f"Created index {name}")


def copyTable(sqliteConn: sqlite3.Connection, client, table: str) -> int:
    cursor = sqliteConn.execute(f"SELECT * FROM {quoteIdent(table)}")
    columns = [assertValidIdentifier(col[0]) for col in cursor.description]
    quotedCols = ", ".join(quoteIdent(col) for col in columns)
    placeholders = ", ".join(["?"] * len(columns))
    insertSql = f"INSERT INTO {quoteIdent(table)} ({quotedCols}) VALUES ({placeholders})"

    copied = 0
    batch = []
    while True:
        rows = cursor.fetchmany(BATCH_SIZE)
        if not rows:
            break
        statements = [(insertSql, list(row)) for row in rows]
        client.batch(statements)
        copied += len(rows)
        batch.append(len(rows))
        print(f"  {table}: copied {copied} row(s)")
    return copied


def copySqliteSequence(sqliteConn: sqlite3.Connection, client) -> None:
    rows = sqliteConn.execute("SELECT name, seq FROM sqlite_sequence").fetchall()
    client.execute("DELETE FROM sqlite_sequence")
    if not rows:
        print("sqlite_sequence: empty")
        return
    statements = [
        (
            "INSERT INTO sqlite_sequence (name, seq) VALUES (?, ?)",
            [name, seq],
        )
        for name, seq in rows
    ]
    client.batch(statements)
    print(f"sqlite_sequence: copied {len(rows)} row(s)")


def verify(sqliteConn: sqlite3.Connection, client) -> None:
    plan = printPlan(sqliteConn, client)
    if plan["mismatches"]:
        raise RuntimeError(
            "Row-count mismatch after copy: " + ", ".join(plan["mismatches"])
        )

    localSeq = dict(sqliteConn.execute("SELECT name, seq FROM sqlite_sequence").fetchall())
    remoteSeqRows = client.execute("SELECT name, seq FROM sqlite_sequence")
    remoteSeq = {row[0]: row[1] for row in remoteSeqRows.rows}
    if localSeq != remoteSeq:
        raise RuntimeError(
            f"sqlite_sequence mismatch.\n  sqlite={localSeq}\n  turso={remoteSeq}"
        )
    print("Verification passed: row counts and sqlite_sequence match.")


def migrate(sqlitePath: Path, replace: bool, dryRun: bool) -> None:
    if not sqlitePath.exists():
        raise FileNotFoundError(f"SQLite file not found: {sqlitePath}")

    sqliteConn = sqlite3.connect(sqlitePath)
    sqliteConn.row_factory = sqlite3.Row
    client = None
    try:
        client = getTursoClient()
        print("Connected to Turso.")
        print(f"Source: {sqlitePath}")
        printPlan(sqliteConn, client)

        if dryRun:
            print("Dry-run only. No writes.")
            return

        tables = listSqliteTables(sqliteConn)
        remote = tursoTableNames(client)
        if remote and not replace:
            raise RuntimeError(
                "Turso already has tables. Re-run with --replace to drop them "
                "and copy again, or use --dry-run to inspect."
            )

        if replace and remote:
            dropRemoteUserTables(client, tables)

        createSchema(sqliteConn, client)
        client.execute("PRAGMA foreign_keys = OFF")
        for table in tables:
            copied = copyTable(sqliteConn, client, table)
            print(f"Copied {table}: {copied} row(s)")
        copySqliteSequence(sqliteConn, client)
        verify(sqliteConn, client)
    finally:
        sqliteConn.close()
        if client:
            client.close()
            print("Turso client closed.")


def parseArgs(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate local SQLite to Turso.")
    parser.add_argument(
        "--sqlite",
        default=str(DEFAULT_SQLITE),
        help="Path to source SQLite file (default: db.sqlite3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print table counts and exit without writing.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Drop existing Turso user tables before copying.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    load_dotenv(ROOT / ".env")
    args = parseArgs(sys.argv[1:] if argv is None else argv)
    try:
        migrate(Path(args.sqlite), replace=args.replace, dryRun=args.dry_run)
    except Exception as error:
        print(f"Migration failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
