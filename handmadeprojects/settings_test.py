"""
Settings for `python manage.py test`.

WhiteNoise's CompressedManifestStaticFilesStorage (used in settings.py) requires
a staticfiles manifest built by `collectstatic`, which normally doesn't exist in
a fresh dev/test checkout. Tests don't need compression/cache-busting, so swap
in the plain storage backend to avoid requiring a collectstatic run first.
"""
from .settings import *  # noqa: F401,F403

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Always use local SQLite for tests. The Turso backend must never be used as
# Django's test runner would otherwise hit (or try to clone) the cloud database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
