# Test Guide

This project has an automated test suite under `mainapp/tests/` (previously an empty `tests.py` stub). It was written in Task 7 (I4) to catch the kind of regression that, until now, only manual dry-run testing against a live dev server could catch.

## Running the tests

Static files use WhiteNoise's `CompressedManifestStaticFilesStorage` in `handmadeprojects/settings.py`, which requires a manifest built by `collectstatic` — one doesn't exist in a fresh checkout, and pages using `{% static %}` (i.e. every page, via `base.html`) will fail to render without it. A dedicated test settings module swaps in the plain static storage backend so tests run standalone with no setup step:

```powershell
python manage.py test mainapp --settings=handmadeprojects.settings_test
```

Run a single file, class, or test:

```powershell
python manage.py test mainapp.tests.test_views --settings=handmadeprojects.settings_test
python manage.py test mainapp.tests.test_views.PublicPagesRenderTests --settings=handmadeprojects.settings_test
python manage.py test mainapp.tests.test_views.PublicPagesRenderTests.test_homepage --settings=handmadeprojects.settings_test -v 2
```

`-v 2` (or `-v 3`) gives per-test output instead of just dots.

If you'd rather not pass `--settings` every time, set it once for your shell session:

```powershell
$env:DJANGO_SETTINGS_MODULE = "handmadeprojects.settings_test"
python manage.py test mainapp
```

(Running against the real `handmadeprojects.settings` still works for tests that don't render a full page — e.g. `test_models.py` — but anything hitting `base.html` will fail with `Missing staticfiles manifest entry` unless you've run `python manage.py collectstatic` first. Prefer `settings_test` for the whole suite.)

## What's covered

| File | Covers |
|---|---|
| `mainapp/tests/factories.py` | Not a test file — small helper functions (`make_product()`, `make_shop()`, etc.) that build minimal valid model instances so tests don't repeat model boilerplate. |
| `mainapp/tests/test_models.py` | Every core model can be created and stringified without error; confirms `UserDetails`/`UserFavProjects` are gone (Task 7 I3). |
| `mainapp/tests/test_views.py` | Every public page returns 200; detail pages 404 correctly for a nonexistent ID (product/intern/shop/team profile); `userdashboard`/`profile`/`add-to-favorites`/`login`/`register` all confirmed gone (404); every admin-gated view (`addproduct`, `add-developer`, `add-intern`, `edit_hero_images`, `analysis`, `edit-product`) redirects anonymous visitors to `/hpmadmin/login/` specifically (not a dead `/login/`); the custom branded 404 page renders under `DEBUG=False`; `robots.txt` and `sitemap.xml` return valid content. |
| `mainapp/tests/test_features.py` | The `price` template filter (thousands-separator formatting, passthrough for `*`/non-numeric/`None`); the contact context processor (phone number, `tel:`, `wa.me` links appear on the homepage); pagination (`allshops`/`productlist` — appears past the page-size threshold, absent for small lists, survives an out-of-range `?page=`, preserves existing filters like `?productcat=`); the AJAX-filter partial responses (`X-Requested-With: XMLHttpRequest`) return a bare fragment, not a full HTML page, for `productlist` and `internship_listing`. |

**Current count: 66 tests, all passing.**

## Extending the suite

- Add new model factories to `factories.py` rather than repeating `Model.objects.create(...)` calls in every test.
- New views: add at minimum a "renders 200" test in `test_views.py`, plus a 404 test if it's a detail view backed by `get_object_or_404`.
- New admin-gated views: add a redirect-to-admin-login test in `AdminGatedViewsRedirectToAdminLoginTests` — this is the regression class that would have caught the `edit_hero_images` dead-login-URL bug found during Task 5's manual route audit (I7), before it became a test.
- Template/UI changes: prefer asserting on stable markers (`aria-label="Pagination"`, a URL fragment, specific text) rather than exact HTML strings, since Tailwind classes will keep changing.
- If you add a new model, remember: `python manage.py makemigrations` before running tests — the test database is built from migrations, not directly from `models.py`.

## What this suite does *not* replace

This is view/model-level testing via Django's test client — it doesn't execute JavaScript (the AJAX-filters/lightbox/dark-mode/back-to-top client-side behavior, theme persistence, etc.), so it can't catch a broken `onclick` handler or a CSS regression. For that, keep doing what earlier tasks did: boot `python manage.py runserver` and click through the actual page. The `/verify` skill in this environment follows that same "drive the real flow" approach for nontrivial changes.
