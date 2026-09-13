# Task 11 — SQLite → Turso (libSQL) cloud migration

**Goal:** Move all data from the local `db.sqlite3` file to the existing Turso
cloud database and make the Django app use that database at runtime.

The connection guide is `test/db-con-guide.py`. The cloud target is **Turso**
(libSQL), not a separate product. Turso is SQLite-compatible, which is why this
is a schema-preserving copy rather than a Postgres-style rewrite.

---

## 1. Findings

| Item | Detail |
|------|--------|
| Source | `db.sqlite3` (~9.4 MB), Django 5.0.3, WAL-capable SQLite |
| Target | Turso libSQL `handmadeprojects-atharvapawar.aws-ap-south-1.turso.io` |
| Creds | `.env` → `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN` (do not commit) |
| Guide | `test/db-con-guide.py` — HTTP, not WebSocket |
| Probe | `SELECT 1` succeeded; Turso currently has **0 objects** (empty) |
| Old script | `oldCodes/pyMigrate.py` is SQLite→CSV→SQLite and **must not** be reused (it recreates every column as `TEXT`) |
| Settings today | `dj_database_url.config(default='sqlite:///db.sqlite3')` |
| Tests | `python manage.py test mainapp --settings=handmadeprojects.settings_test` |

### Guide rules that this migration must follow

1. AWS Turso does **not** support WebSockets. `libsql://` is treated as `wss://`
   by `libsql-client`, so convert to `https://` before connecting.
2. Always pass values with `?` placeholders. Never concatenate user input into SQL.
3. HTTP mode has **no** `transaction()` API — use `execute` / `batch`.
4. The guide's `runGuide()` **drops** a `users` table. Do **not** run the guide
   walkthrough against the real app database.

### What must be copied

28 user tables (Django auth/admin/sessions + all `mainapp_*` models), plus:

- indexes with a real `CREATE INDEX` statement (skip `sqlite_autoindex_*`)
- `sqlite_sequence` so AUTOINCREMENT continues from current max IDs
- `django_migrations` so `migrate` does not re-apply 0001–0020

Largest rows are ~20 KB (`mainapp_interndetails` base64 photos). Safe for HTTP
batch inserts.

---

## 2. Approach (two layers)

### Layer A — Data copy (libsql-client)

Same client as the guide. Copy schema SQL from `sqlite_master`, then copy rows
with parameterized `INSERT`. Verify counts + sequences.

Do **not** use `turso db import` — that creates a *new* database named after the
file. We already have a Turso database and credentials.

### Layer B — Django runtime (`django-libsql-backend`)

Django's built-in `sqlite3` backend can only open a local file. Runtime access
to Turso uses `ENGINE = "django_libsql"` over HTTP (AWS-safe).

- If `TURSO_DATABASE_URL` + `TURSO_AUTH_TOKEN` are set and `USE_TURSO` is not
  disabled → Turso.
- Else → local SQLite (rollback).
- Tests always use `django.db.backends.sqlite3`. Never create/destroy a test DB
  on the cloud database.

---

## 3. Execution steps

1. Backup `db.sqlite3`.
2. Add deps: `libsql-client`, `python-dotenv`, `django-libsql-backend`.
3. Write `test/migrate_sqlite_to_turso.py` with `--dry-run` / `--replace`.
4. Dry-run, then copy schema + data.
5. Verify table counts and `sqlite_sequence`.
6. Point `handmadeprojects/settings.py` at Turso; lock tests to SQLite.
7. Add `.gitignore` for `.env` and backups.
8. ORM smoke check + `manage.py test` on `settings_test`.
9. Document env vars and rollback (`USE_TURSO=0`).

---

## 4. Acceptance criteria

- [x] Turso has the same user-table row counts as `db.sqlite3`
- [x] AUTOINCREMENT sequences match
- [x] Django ORM reads catalog data from Turso (e.g. hardware product 77)
- [x] `python manage.py showmigrations` shows mainapp 0001–0020 applied
- [x] `python manage.py test mainapp --settings=handmadeprojects.settings_test` passes
- [x] `.env` is not committed
- [x] Local SQLite file is kept as a rollback copy

---

## 5. Rollback

```powershell
$env:USE_TURSO = "0"
python manage.py runserver
```

App goes back to `db.sqlite3`. The SQLite file is not deleted by this migration.

---

## 6. Render / production

Set these on the host (do not put the token in git):

- `TURSO_DATABASE_URL`
- `TURSO_AUTH_TOKEN`

`python-dotenv` only loads a local `.env`; production must inject env vars.

---

## 7. Implementation notes (done)

| Item | Result |
|------|--------|
| Backup | `backups/db.sqlite3.pre-turso-20260914` (gitignored) |
| Data copy | `test/migrate_sqlite_to_turso.py` — 28 tables, counts + `sqlite_sequence` match |
| Django engine | `django_libsql` over HTTP (`libsql://` → `https://`) |
| Backend pin | `django-libsql-backend==0.1.3` (0.1.0 cannot INSERT; 0.1.2+ imports Django 5.2 `CompositePrimaryKey`) |
| Django 5.0 shim | `_patch_composite_primary_key_for_libsql()` in `settings.py` |
| Tests | Forced SQLite in `settings_test.py` + `manage.py test` guard. **76/76 passing** |
| ORM check | Hardware 77 present; Contactus write/delete round-trip ok |
| Secrets | `.gitignore` covers `.env` and `backups/` |

### Re-run / verify

```powershell
python test/migrate_sqlite_to_turso.py --dry-run
python test/verify_django_turso.py
python manage.py test mainapp --settings=handmadeprojects.settings_test
```

### Backend note

Do not bump `django-libsql-backend` past 0.1.3 without checking Django 5.0.3. Newer releases import `CompositePrimaryKey`, which only exists in Django 5.2+. The settings shim covers 0.1.3; remove it if the project later upgrades Django.
