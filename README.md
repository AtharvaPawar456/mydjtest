# mydjtest (handmadeprojects)

A Django 5.0.3 monolith for a "handmade / STEM projects" marketplace and internship platform. Single app (`mainapp`) serving hand-rolled HTML views (no DRF/REST API).

## What it does

- **Product catalog** — engineering/hardware/software project kits (`ProductInfo`), accessories (`AccessoriesProd`), AI content (`AicontentProd`), YouTube project videos (`YTvideos`).
- **Business directory** — a "shops" listing (`Businesswebinfo`).
- **Internships** — listings (`InternDetails`) plus static seed data (`intern_opportunities_data.py`) and an intern profile/gallery.
- **Earn Tasks** — a paid gig/task board (`EarnTask`).
- **Team/About** — team member profiles (`TeamMember`).
- **Affiliate program** — a static info page describing commission tiers (no tracking logic implemented yet).
- **Accounts** — Django's built-in `auth.User` extended with a `UserDetails` profile (address, contact, referral id) and `UserFavProjects` (bookmarks/favorites).
- **Admin** — the real Django admin at `/hpmadmin/`, plus a set of hand-rolled "admin" views (add/edit product, developer, intern, hero images, video) gated by a hardcoded username check rather than staff/permission flags.

## Project layout

```
handmadeprojects/   Django project (settings, root urls, wsgi/asgi)
mainapp/            The entire application
  models.py         All models
  views.py           ~955-line monolithic view module
  urls.py           URL routes
  admin.py          Django admin customizations
  seo_views.py      robots.txt / sitemap.xml
  migrations/       0001-0012
  templates/        AffiliateProgram, earnTasks, InternSection, ProductSection,
                     systemsetup, TeamSection, UserSection, BusinessSection,
                     AccessoriesSection, AiContentSection, YoutubeSection, projectscategory
  static/           mostly vendored Django-admin JS
oldCodes/           legacy, not wired into the live app (see below)
```

`oldCodes/` holds a one-off SQLite → CSV → SQLite migration script (`pyMigrate.py`) and a stale Render.com deploy manifest (`render.yaml`) that references an old/incorrect project name — kept for historical reference only.

## Stack

- Django 5.0.3
- gunicorn (WSGI server)
- whitenoise (static files)
- Turso / libSQL (cloud SQLite) via `django-libsql-backend` when `TURSO_DATABASE_URL` + `TURSO_AUTH_TOKEN` are set
- Local SQLite fallback (`db.sqlite3`) when those env vars are missing or `USE_TURSO=0`
- dj-database-url (SQLite fallback / optional `DATABASE_URL`)
- Pillow

## Database

Copy `.env.example` to `.env` and fill in Turso credentials from https://app.turso.tech. AWS Turso endpoints are used over HTTP (`libsql://` is converted to `https://`).

```
pip install -r requirements.txt
python test/migrate_sqlite_to_turso.py --dry-run
python test/migrate_sqlite_to_turso.py
python manage.py runserver
```

Rollback to the local file without touching Turso:

```
$env:USE_TURSO = "0"
python manage.py runserver
```

Tests always use SQLite and never the cloud database:

```
python manage.py test mainapp --settings=handmadeprojects.settings_test
```

See [ai-space/tasks/task-11.md](ai-space/tasks/task-11.md) for the migration plan and notes. Do **not** run `test/db-con-guide.py`'s CRUD walkthrough against the app database — it drops a `users` table.

## Running locally

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment

Deployed to Render.com (`mydjtest.onrender.com`) using gunicorn; hostname is picked up from the `RENDER_EXTERNAL_HOSTNAME` environment variable. Set `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` on the host (do not commit `.env`).

## Known issues

The project currently has `DEBUG = True` and a hardcoded `SECRET_KEY` committed to source — **not production-safe as configured**. See [ai-space/tasks/task-5.md](ai-space/tasks/task-5.md) for a full list of known bugs and suggested fixes.
