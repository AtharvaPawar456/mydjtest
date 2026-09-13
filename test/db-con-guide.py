"""
Turso / libSQL connection guide (Python)
========================================

This file is a runnable reference for connecting to a Turso (libSQL)
database and performing basic CRUD.

Setup
-----
1. Install packages:

       pip install libsql-client python-dotenv

2. Create a `.env` file next to this script:

       TURSO_DATABASE_URL=libsql://<db>-<org>.<region>.turso.io
       TURSO_AUTH_TOKEN=<token from Turso dashboard or CLI>

   Get the URL and token from:
   https://app.turso.tech

       turso db show --url <database-name>
       turso db tokens create <database-name>

3. Run:

       python db-con-guide.py

Important
---------
Turso databases on AWS do not support WebSockets.
`libsql-client` treats `libsql://` as `wss://`, so this guide converts
the URL to `https://` before connecting.

Always pass values with `?` placeholders. Never concatenate user input
into SQL strings.

Do **not** run this walkthrough against the handmadeprojects Turso
database. `createUsersTable()` drops a table named `users`. Use a
scratch database for the tutorial. App data is migrated with
`test/migrate_sqlite_to_turso.py`.
"""

import os

from dotenv import load_dotenv
from libsql_client import create_client_sync


load_dotenv()


# ---------------------------------------------------------------------------
# 1. Connection
# ---------------------------------------------------------------------------

def toHttpUrl(databaseUrl):
    """Convert libsql:// or wss:// to https:// for Turso AWS endpoints."""
    if databaseUrl.startswith("libsql://"):
        return "https://" + databaseUrl[len("libsql://"):]

    if databaseUrl.startswith("wss://"):
        return "https://" + databaseUrl[len("wss://"):]

    return databaseUrl


def getDatabaseClient():
    """Create a synchronous Turso client from environment variables."""
    databaseUrl = os.getenv("TURSO_DATABASE_URL")
    authToken = os.getenv("TURSO_AUTH_TOKEN")

    if not databaseUrl:
        raise ValueError("TURSO_DATABASE_URL is missing from .env")

    if not authToken:
        raise ValueError("TURSO_AUTH_TOKEN is missing from .env")

    client = create_client_sync(
        url=toHttpUrl(databaseUrl),
        auth_token=authToken,
    )

    print("Connected to Turso.")
    return client


def testConnection(client):
    """Confirm the database accepts queries."""
    result = client.execute("SELECT 1 AS status")
    print(f"Connection check: {result.rows}")
    return True


# ---------------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------------

def printRows(label, result):
    """Print a result set as a list of dictionaries."""
    print(f"{label} ({len(result.rows)} row(s)):")

    if not result.rows:
        print("  (empty)")
        return

    for row in result.rows:
        print(f"  {dict(zip(result.columns, row))}")


# ---------------------------------------------------------------------------
# 3. Schema
# ---------------------------------------------------------------------------

def createUsersTable(client):
    """Drop and recreate a sample users table."""
    client.execute("DROP TABLE IF EXISTS users")
    client.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL
        )
        """
    )
    print("Created table: users")


# ---------------------------------------------------------------------------
# 4. CRUD
# ---------------------------------------------------------------------------

def createUser(client, name, email, city):
    """Insert one user and return the new row id."""
    result = client.execute(
        "INSERT INTO users (name, email, city) VALUES (?, ?, ?)",
        [name, email, city],
    )
    print(f"Created user {email} (id={result.last_insert_rowid})")
    return result.last_insert_rowid


def readUsers(client):
    """Return all users ordered by id."""
    return client.execute(
        "SELECT id, name, email, city FROM users ORDER BY id"
    )


def readUserByEmail(client, email):
    """Return one user by email, or None if missing."""
    result = client.execute(
        "SELECT id, name, email, city FROM users WHERE email = ?",
        [email],
    )
    return result if result.rows else None


def updateUserCity(client, email, city):
    """Update a user's city. Returns the number of rows changed."""
    result = client.execute(
        "UPDATE users SET city = ? WHERE email = ?",
        [city, email],
    )
    print(f"Updated {result.rows_affected} user(s) with email {email}")
    return result.rows_affected


def deleteUserByEmail(client, email):
    """Delete a user by email. Returns the number of rows deleted."""
    result = client.execute(
        "DELETE FROM users WHERE email = ?",
        [email],
    )
    print(f"Deleted {result.rows_affected} user(s) with email {email}")
    return result.rows_affected


# ---------------------------------------------------------------------------
# 5. Walkthrough
# ---------------------------------------------------------------------------

def runGuide(client):
    """Run the connection check, then a full CRUD walkthrough."""
    print("\n--- Connection ---")
    testConnection(client)

    print("\n--- Schema ---")
    createUsersTable(client)

    print("\n--- Create ---")
    createUser(client, "Atharva Pawar", "atharva@example.com", "Pune")
    createUser(client, "Riya Shah", "riya@example.com", "Mumbai")
    createUser(client, "Karan Mehta", "karan@example.com", "Delhi")
    printRows("Users after create", readUsers(client))

    print("\n--- Read ---")
    oneUser = readUserByEmail(client, "riya@example.com")
    printRows("User by email", oneUser)

    print("\n--- Update ---")
    updatedCount = updateUserCity(client, "riya@example.com", "Bengaluru")
    if updatedCount != 1:
        raise RuntimeError("Update failed: expected 1 row to change")

    updatedUser = readUserByEmail(client, "riya@example.com")
    printRows("User after update", updatedUser)

    if updatedUser.rows[0]["city"] != "Bengaluru":
        raise RuntimeError("Update failed: city was not set to Bengaluru")

    print("\n--- Delete ---")
    deletedCount = deleteUserByEmail(client, "karan@example.com")
    if deletedCount != 1:
        raise RuntimeError("Delete failed: expected 1 row to be removed")

    remaining = readUsers(client)
    printRows("Users after delete", remaining)

    remainingEmails = [row["email"] for row in remaining.rows]
    if remainingEmails != ["atharva@example.com", "riya@example.com"]:
        raise RuntimeError("Delete failed: remaining users did not match")

    print("\nGuide checks passed.")


def main():
    """Connect, run the guide, then close the client."""
    client = None

    try:
        client = getDatabaseClient()
        runGuide(client)

    except Exception as error:
        print(f"Guide failed: {error}")

    finally:
        if client:
            try:
                client.close()
                print("Turso client closed.")
            except Exception as error:
                print(f"Failed to close Turso client: {error}")


if __name__ == "__main__":
    main()
