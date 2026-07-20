# Task 7

## Plan / Todo

- [x] I1 - DRY the contact phone number: single source of truth (settings constant + context processor / template include), replace the 6 hardcoded occurrences (`welcome.html`, `contactus.html`, `base.html`, `productlist.html`, `productinfo.html`, `affiliateInfo.html`).
- [x] I2 - Everywhere the phone number now appears (via I1's shared component), make sure a WhatsApp button sits next to Call, so a click opens WhatsApp chat with our number pre-filled for a query.
- [x] I3 - Remove the dead-end `userdashboard`, `profile`, `add-to-favorites` features entirely: views, URLs, templates, nav links, and the `UserDetails`/`UserFavProjects` models (with migration).
- [x] I4 - Write an automated test suite (`mainapp/tests/`) covering models, views and the key flows touched across Tasks 5/6/7, plus a `test-guide.md` explaining how to run and extend it.
- [x] I5 - Sitemap: log/warn when a table's row count exceeds the 2000/1000 slice caps, so silent truncation becomes visible.
- [x] I6 - Add an `<image:image>` sitemap extension for products/shops whose image is a real URL (skip base64-embedded images, which can't be represented this way).
- [x] I7 - Narrow the broad `except Exception` blocks in `viewShop`, `viewAllShop`, `accessoriesProjects`/`accessoriesView`, `aicontentList`/`aicontentView`, `productinfo`, `productlist` to expected exception types, with proper logging for anything unexpected.
- [x] I8 - Add pagination to `productlist`, `allshops`, `internship_listing`, `aicontentlist`, `accessprodlist` (works with existing AJAX filtering where applicable).
- [x] I9 - Modernize the remaining old-style templates to match the rest of the site: `accessprodlist.html`, `aicontentlist.html`, `accessprodview.html`, `aicontentview.html`, `video_player.html`, `active_earn_tasks.html`.
- [x] I10 - Add a lightbox/zoom to product gallery images on `productinfo.html` (reuse the pattern already built for intern/team photos).
- [x] I11 - Add a site-wide "back to top" button (shows on scroll) and expand the header search to also cover interns, shops, team and accessories/AI-content, not just products.
- [x] I12 - Add a floating, persistent Call/WhatsApp button visible on every page (not just homepage/contactus).
- [x] I13 - Custom branded 404 and 500 error pages.
- [x] I14 - Cookie-consent banner + Privacy Policy + Terms of Service pages.
- [x] I15 - Active-page highlighting in the header nav.
- [x] I16 - Dark mode (toggle + persisted preference); full site-wide infra plus the highest-traffic templates first.
- [x] I17 - Consistent price formatting (thousands separator) wherever `prodcost`/`apsale`/`aisale`/`apprice`/`aiprice` are rendered.

## Implementation notes

### I1 + I2 — DRY contact phone number + WhatsApp everywhere

- Added `CONTACT_PHONE_DISPLAY`, `CONTACT_PHONE_TEL`, `CONTACT_WHATSAPP_NUMBER`, `CONTACT_WHATSAPP_DEFAULT_MESSAGE` constants to `handmadeprojects/settings.py` — the single source of truth.
- New `mainapp/context_processors.py` (`contact_info`) exposes `contact_phone_display` / `contact_phone_tel` / `contact_whatsapp_url` (a pre-built `https://wa.me/<number>?text=<message>` URL) to every template; registered in `TEMPLATES.OPTIONS.context_processors`.
- New reusable partial `mainapp/templates/systemsetup/_call_whatsapp_buttons.html` (Call + WhatsApp button pair) — used in `welcome.html`, `contactus.html`, `productinfo.html`'s CTA footer, `accessprodview.html`, and `aicontentview.html`.
- Replaced all 6 originally-hardcoded occurrences, plus 2 more found along the way: the JSON-LD `Organization.telephone` in `base.html`, and the footer contact block in `base.html` (now a real `tel:`/WhatsApp link pair instead of plain text).
- `productlist.html`'s bottom CTA phone span became a real WhatsApp link (satisfying I2 directly on that page too).
- Verified: `grep` for the literal number across all templates returns zero hardcoded matches; live-server check confirms the phone/Call/WhatsApp links render correctly via the context processor.

### I3 — Removed the dead-end user-account subsystem

- Deleted `userdashboard`, `profile`, `add_to_favorites` views (`views/user.py` removed entirely; `add_to_favorites` and its `is_favorite` context-building removed from `views/product.py`), their URL entries, and their templates (`UserSection/profile.html`, `UserSection/userdashboard.html`).
- Removed the `UserDetails` and `UserFavProjects` models from `models.py`, their admin registrations, and generated/applied migration `0013_remove_userfavprojects_prod_and_more`.
- Updated `base.html`'s authenticated-user nav (desktop + mobile): dropped the now-gone Dashboard/Profile links, kept username display + Log out (still meaningful for the one account — the site owner — that can ever be logged in, via `/hpmadmin/login/`).
- Cleaned up the now-stale `Disallow: /userdashboard/` / `Disallow: /profile/` lines in `robots.txt`.
- Verified: all three routes now 404; `manage.py check` and the full test suite confirm nothing else referenced them.

### I5 + I6 — Sitemap truncation warning + image extension

- `seo_views.py`: added `_warn_if_truncated(label, total, cap)`, called once per model (Product/Shop/Intern/Video/Accessory/AI-content) before slicing — logs a warning via Python's `logging` module whenever a table's row count exceeds its cap, so silent truncation is now visible in logs instead of invisible.
- Added `_first_real_image_url()` — extracts the first `http(s)` image URL from a `;`/newline-separated media field, skipping the `*` placeholder and base64 data URIs (which can't be represented in an image sitemap). Wired into the Product/Shop/Accessory/AI-content loops, emitting `<image:image><image:loc>...</image:loc></image:image>` entries under the `xmlns:image` namespace.
- Verified: sitemap parses as valid XML (`[xml]$doc = ...`), contains `xmlns:image`, and produced 119 `<image:loc>` entries against 141 URLs on the live dev data (the 31 project ideas seeded in Task 5 with a real `promoimg.png` URL account for most of them).

### I7 — Narrowed broad exception handling

- `business.py` (`viewShop`, `viewAllShop`), `accessories.py`, `aicontent.py`, `product.py` (`productlist`, `productinfo`): each now catches `django.db.Error` specifically first (logged via `logger.warning` with a user-facing "temporarily unavailable" message), then a final `except Exception` that calls `logger.exception(...)` — so any truly unexpected error is now logged with a full traceback instead of being silently swallowed and shown to the visitor as raw `str(error)` text (which was also a minor information-disclosure smell, now replaced with a generic message).
- Verified via the full test suite (all `except Http404: raise` paths and happy paths still behave identically) plus `manage.py check`.

### I8 — Pagination

- New `paginate(request, queryset, per_page)` helper in `views/_shared.py` — wraps Django's `Paginator`, returns `(page_obj, base_querystring)` where the base querystring has `page` stripped so pagination links compose with existing filters.
- New reusable `mainapp/templates/systemsetup/_pagination.html` (Prev / page X of Y / Next, dark-mode aware).
- Applied to `productlist` (24/page, works through both the full-page and AJAX-partial render paths — `_product_results.html`), `internship_listing` (20/page, same AJAX-aware pattern via `_intern_results.html`), `viewAllShop` (24/page), `aicontentList` (24/page), `accessoriesProjects` (24/page).
- Verified: pagination controls appear only when there's more than one page (confirmed absent for small lists like the 2-row intern/1-row accessory tables), links preserve existing query params (e.g. `?productcat=hardwareprojects&page=2`), an out-of-range `?page=9999` clamps gracefully instead of 500ing (Django's `Paginator.get_page` behavior), and the AJAX-filtered partial responses include working pagination too.

### I9 — Modernized the remaining old-style templates

Rewrote all 6 templates to match the site's established design language (breadcrumb nav, `rounded-2xl` cards, consistent typography, dark-mode classes, the shared Call/WhatsApp partial where relevant):
- `accessprodlist.html`, `aicontentlist.html` — breadcrumb + hero header + card grid (previously plain `rounded-lg`/`shadow-lg` Bootstrap-ish cards).
- `accessprodview.html`, `aicontentview.html` — rewritten to the same two-column image/details layout as `productinfo.html`, keeping the existing SEO meta/Product-schema blocks untouched.
- `video_player.html` — breadcrumb nav, `aspect-video` responsive player, fixed two pre-existing lint issues found while touching the file (missing `<iframe title>`, deprecated `frameborder` attribute).
- `active_earn_tasks.html` — breadcrumb + hero header + card grid.
- Verified: all 6 pages (plus a temporarily-created video record for `video_player`, cleaned up after) return 200 on a live server.

### I10 — Product gallery lightbox

- `productinfo.html`: gallery `<img>` tags now carry a `lightbox-trigger` class; added a fullscreen lightbox overlay (same pattern as the existing intern/team-photo lightbox) with click-to-open, click-outside/✕-button/Escape-to-close. Video items in the gallery are left as-is (they already have native controls).
- Verified on a product with real gallery entries: lightbox markup and trigger class both present in the rendered page.

### I11 — Back-to-top button + site-wide multi-section search

- Back-to-top: a floating button (bottom-right stack, above the Call/WhatsApp buttons) that appears via a `scroll` listener past 400px and smooth-scrolls to top on click.
- Global search: new `mainapp/views/search.py` (`global_search`) queries `ProductInfo`, `InternDetails`, `Businesswebinfo` (visible only), `TeamMember`, `AccessoriesProd`, and `AicontentProd` in one request, capped at 12 results per section, rendered in `systemsetup/search_results.html` grouped by section. Wired at `/search/` and both header search forms (desktop + mobile) now submit there instead of straight to `productlist`.
- Verified: `/search/?q=iot` returns matching results across sections; empty query renders the bare search page without erroring.

### I12 — Floating persistent Call/WhatsApp CTA

- Added a fixed bottom-right button stack (WhatsApp, Call, and — when applicable — Back-to-top) in `base.html`, so it appears on every page including deep pages like `productinfo`/`shop`/`intern_profile` that previously had no visible contact CTA outside the homepage/contact page.

### I13 — Custom 404/500 error pages

- `mainapp/templates/404.html` extends `base.html` (Django's `page_not_found` view renders it *with* request context, so the full nav/footer/contact-info render correctly) — branded, with links back to home and the catalog.
- `mainapp/templates/500.html` is a deliberately **standalone**, self-contained page (no `extends`, inline CSS, no external requests) — Django's `server_error` view renders `500.html` **without** request context or context processors, so relying on `base.html`/`contact_phone_display` etc. wouldn't reliably populate; a minimal always-works page is safer for a genuine outage. The phone number here is the one deliberate hardcoded exception to I1's DRY rule, for that reason.
- Verified via `override_settings(DEBUG=False)` + Django's test client hitting a nonexistent URL (confirms branded 404), and via `django.template.loader.get_template('500.html').render()` (confirms it renders standalone with no context).

### I14 — Cookie consent + Privacy Policy + Terms of Service

- Cookie-consent banner: fixed bottom bar in `base.html`, shown once (checks/sets `localStorage.cookieConsentAccepted`), linking to the new Privacy Policy page.
- New `privacy_policy` / `terms_of_service` views (`views/legal.py`), routes (`/privacy-policy/`, `/terms-of-service/`), and templates — both linked from the footer and mentioned in the cookie banner.
- Verified: both pages return 200; cookie banner markup present on the homepage.

### I15 — Active-page nav highlighting

- New `mainapp/templatetags/nav_tags.py` (`{% nav_active 'url_name' 'other_url_name' ... %}`) — compares `request.resolver_match.url_name` against the given names and returns a highlight class. Applied to every desktop and mobile nav link in `base.html`, grouping related views under one nav item (e.g. Shops is active for both `viewallshop` and `viewshop`).
- Verified: the Home link carries the active-state class on `/`.

### I16 — Dark mode

- Infra (applies everywhere, since it's all in `base.html`): `tailwind.config.darkMode = 'class'`, a pre-paint inline script that applies `dark` to `<html>` based on `localStorage.theme` or `prefers-color-scheme`, a toggle button (sun/moon icon swap) that persists the choice, and `dark:` variants across the entire shell — header, both nav variants, mobile menu, search inputs, footer links, floating CTA area, cookie banner, pagination partial, and the Call/WhatsApp partial.
- Also added `dark:` variants to the 6 templates touched in I9 (`accessprodlist`, `aicontentlist`, `accessprodview`, `aicontentview`, `video_player`, `active_earn_tasks`) and the new I11/I13/I14 pages (search results, 404, privacy policy, terms of service) as they were being built.
- **Scope note**: full dark-mode coverage of every one of the ~50 templates in the app (e.g. `productinfo.html`'s body content, `shop.html`, `intern_profile.html`, the admin-only add/edit forms) was **not** done in this pass — that's a larger follow-up. What's covered: the shell (visible on every page regardless of content) plus every template touched by I9/I11/I13/I14, so dark mode is usable site-wide today without looking broken, but some deeper content areas will still render with their original light-only styling until they get their own `dark:` pass.
- Verified: toggle button, theme-application script, and the `dark:` classes are present and the pre-paint script runs before Tailwind's CDN script, avoiding a flash-of-wrong-theme in the common case.

### I17 — Consistent price formatting

- New `mainapp/templatetags/price_filters.py` (`{{ value|price }}`) — formats numeric-looking price strings with thousands separators via `django.contrib.humanize`'s `intcomma` (added to `INSTALLED_APPS`), passing through unchanged anything non-numeric (the `*` placeholder, `None`, free-text).
- Applied to every visible price display: `productlist.html`/`_product_results.html` (`prodcost`), `productinfo.html` (`prodcost`), `accessprodlist.html`/`accessprodview.html` (`apsale`/`apprice`), `aicontentlist.html`/`aicontentview.html` (`aisale`/`aiprice`). **Not** applied to the JSON-LD `Offer.price` values in structured-data blocks — those need a plain machine-readable number, not `15,000`.
- Verified via unit tests: `"15000"` → `"15,000"`, `"*"` → `"*"` (unchanged), `None`/non-numeric → passed through unchanged.

## I4 — Automated test suite + test-guide.md

- Converted the empty `mainapp/tests.py` stub into a `mainapp/tests/` package: `factories.py` (model-builder helpers), `test_models.py`, `test_views.py`, `test_features.py` — **66 tests, all passing**.
- Coverage: every core model creates/stringifies correctly; every public page returns 200; detail pages 404 for a nonexistent ID; the I3 removals (`userdashboard`/`profile`/`add-to-favorites`/`login`/`register`) are confirmed gone (404); every admin-gated view redirects anonymous visitors specifically to `/hpmadmin/login/` (the exact regression class that caused the `edit_hero_images` bug found in Task 5's I7 manual audit); the custom 404 page renders under `DEBUG=False`; the `price` filter, pagination (present/absent/out-of-range/filter-preserving), the contact context processor, and the AJAX-partial responses.
- Found and fixed a real test-environment issue along the way: WhiteNoise's `CompressedManifestStaticFilesStorage` requires a `collectstatic`-built manifest that doesn't exist in a fresh checkout, so any test rendering a full page (i.e. anything extending `base.html`) failed with `Missing staticfiles manifest entry`. Fixed with a dedicated `handmadeprojects/settings_test.py` (imports the real settings, swaps in the plain static storage backend) — documented as the standard way to run this suite (`python manage.py test mainapp --settings=handmadeprojects.settings_test`).
- `test-guide.md` (repo root) documents how to run the suite, what each file covers, how to extend it, and explicitly notes what it *doesn't* replace (client-side JS behavior — AJAX filters, lightbox, dark-mode toggle, back-to-top — still needs manual browser verification).

## Final verification

- `python manage.py check` — 0 issues, checked after every individual item above and again at the end.
- Byte-compiled every modified `.py` file across `mainapp/views/`, `mainapp/templatetags/`, `mainapp/tests/`, `mainapp/*.py`, and `handmadeprojects/*.py`.
- Full test suite: **66/66 passing** (`--settings=handmadeprojects.settings_test`).
- Live-server smoke test of 30 routes spanning every item in this task (core pages, the two removed-feature checks, the admin-login-redirect checks, the new legal/search pages, robots/sitemap) — **0 mismatches**.
- No regressions found in any previously-verified behavior from Tasks 5 or 6 (AJAX filtering, soft-404 fixes, SEO schema blocks, masonry layouts, the Task 6 login/register removal this task built further on).
