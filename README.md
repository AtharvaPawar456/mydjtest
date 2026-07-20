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
- psycopg2-binary + dj-database-url (Postgres in production, SQLite locally via `DATABASE_URL` env var, default `sqlite:///db.sqlite3`)
- Pillow

## Running locally

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment

Deployed to Render.com (`mydjtest.onrender.com`) using gunicorn; hostname is picked up from the `RENDER_EXTERNAL_HOSTNAME` environment variable.

## Known issues

The project currently has `DEBUG = True` and a hardcoded `SECRET_KEY` committed to source — **not production-safe as configured**. See [ai-space/tasks/task-5.md](ai-space/tasks/task-5.md) for a full list of known bugs and suggested fixes.
