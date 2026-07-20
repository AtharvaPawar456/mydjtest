# Task 6

## Plan / Todo

- [x] I1 - Plan properly and fix these small UI/UX changes:
  - [x] 1. Homepage (`/`) — add the HMP logo image next to the "HandMadeProjects" brand text in the site header (currently just a text "HP" badge, no real logo image).
  - [x] 2. Improve UI/UX of `/engineering-projects/` — modernize the plain FontAwesome-icon-circle cards to match the site's established design language (gradients, rounded-2xl cards, hover states) used on `productlist.html`/`internship_listing.html`.
  - [x] 3. Improve UI/UX of `/ourteam/` — modernize team grid cards, add breadcrumb nav, richer card layout with role/experience preview.
  - [x] 4. Improve UI/UX of `/ourteam/profile/?name=<name>` — modernize the profile page to match `intern_profile.html`'s richer layout (gradient header banner, social links row, sectioned content).
  - [x] 5. Rebuild `/gallery/` as a Pinterest-style masonry layout (reuse the CSS-columns masonry technique already used in `shop.html`'s gallery) so images keep their natural aspect ratio and no grid space is wasted.
  - [x] 6. Homepage (`/`) — add a clear "Contact us" section showing the phone number **+91 81692 39027** with direct Call and WhatsApp buttons and the text "Contact us via Call/WhatsApp for any query or for mentoring."
- [x] I2 - Replace the shared default placeholder image on the 31 newly-uploaded project ideas (Task 5 I8) with `https://raw.githubusercontent.com/AtharvaPawar456/HandMadeProjects/refs/heads/main/siteimages/promoimg.png`.
- [x] I3 - Small changes:
  - [x] 1. Improve UI/UX of `/productlist/?productcat=<...>` — Pinterest/masonry-style image display so product images (many of which are base64, arbitrary aspect ratio) show properly instead of being force-cropped into a fixed-height box.
  - [x] 2. Remove the public login/register flow from the website entirely — visitors should never see or use a login/register page. Only the Django admin login (`/hpmadmin/login/`) remains, for the site owner when they need to manage content. Every admin-gated view must keep working via that same session.
  - [x] 3. `/contactus/` — remove the contact form entirely; show the phone number **+91 81692 39027** with Call/WhatsApp buttons instead (same treatment as the homepage contact section).
- [x] I4 - List down code-side and user-side improvements needed on the website (analysis only, see "I4 - Improvement list").

## I1 - Implementation notes

1. **Header logo** (`mainapp/templates/systemsetup/base.html`) — replaced the plain "HP" text badge with an `<img>` pointing at the existing HMP logo asset, sized `h-9 w-9 rounded-xl`, kept next to the "HandMadeProjects" text as before. Added an `onerror` fallback that swaps back to the old gradient "HP" badge if the external image ever fails to load, so the header never breaks. Shared across every page via `base.html`, so it now also shows correctly at `/`.

2. **`/engineering-projects/`** (`mainapp/templates/projectscategory/engineering_projects_category.html`) — rewritten to match the site's card language: breadcrumb nav, hero heading + subtitle, 4 category cards using `rounded-2xl border shadow-sm hover:shadow-lg hover:-translate-y-1` with color-coded gradient icon badges (blue/emerald/red/amber) instead of the old plain `rounded-full` icon circles, plus a bottom CTA band linking to the full catalog / contact page (same pattern as `productlist.html`'s footer CTA).

3. **`/ourteam/`** (`mainapp/templates/TeamSection/ourteam.html`) — added breadcrumb nav and a proper hero header (eyebrow label + h1 + subtitle), rewrote the grid to a 4-column card layout matching `internship_listing.html`'s intern cards (rounded-2xl, gradient avatar background, role + experience preview, "View profile →" link), and removed the dead commented-out duplicate card markup that was left in the file. Also swapped the raw `/add-developer` href for `{% url 'add_developer' %}`.

4. **`/ourteam/profile/`** (`mainapp/templates/TeamSection/ourteam_profile.html`) — rebuilt the profile card to match `intern_profile.html`'s layout: breadcrumb nav, gradient header banner (brand colors instead of the old indigo/purple), visible LinkedIn/GitHub link pills (previously present but hidden via a stray `hidden` class), sectioned "Experience"/"About" content, and a proper 404 empty-state card. The SEO metadata/canonical/Person-schema blocks added in Task 5 (I6) were preserved untouched — only the visual `content` block was rebuilt.

5. **`/gallery/`** (`mainapp/templates/systemsetup/gallery.html`) — replaced the fixed `grid` + `h-48 object-cover` (which cropped every image to the same height and wasted space around differently-shaped images) with the same CSS-columns masonry technique already proven in `shop.html`'s gallery (`columns-1 sm:columns-2 lg:columns-3`, `break-inside-avoid`, images at natural aspect ratio). Added `loading="lazy"`/`decoding="async"`/`fetchpriority="low"` to each image for page-weight since this page can render many images at once.

6. **Homepage contact section** (`mainapp/templates/systemsetup/welcome.html`) — added a dedicated "Contact us via Call / WhatsApp for any query or for mentoring" band right after the hero section, showing **+91 81692 39027** prominently plus two direct action buttons: `tel:+918169239027` (Call now) and `https://wa.me/918169239027` (WhatsApp).

## I2 - Implementation notes

Updated `DEFAULT_IMG` in `mainapp/new_project_ideas_data.py` to the new promo image URL, then re-ran `python manage.py seed_new_project_ideas --force` to push it onto all 31 already-seeded products (`update_or_create` by `productname`, so no duplicates) — output: `created=0 updated=31 skipped=0 total=31 force=True`.

## Verification

- `python manage.py check` — 0 issues.
- Booted the dev server and requested every touched page (`/`, `/engineering-projects/`, `/ourteam/`, `/ourteam/profile/?name=Atharva`, `/gallery/`, `/productlist/?productcat=hardwareprojects`) — all `200`.
- Confirmed on the homepage: logo `<img>` present, `tel:+918169239027` link present, `wa.me/918169239027` link present, phone number text present.
- Confirmed `/ourteam/` now builds profile links via `{% url %}` (previously a raw string).
- Confirmed `/gallery/` renders the `gallery-masonry` CSS-columns layout with `loading="lazy"` images.
- Re-verified `/ourteam/profile/?name=Atharva` still renders valid Person + BreadcrumbList JSON-LD (parsed via a JSON parser) and the canonical still includes `?name=`, and that an unmatched name still correctly returns HTTP 404 (soft-404 fix from Task 5 still holds after the template rewrite).
- Confirmed a seeded project-idea detail page now serves the new `promoimg.png` image instead of the old placeholder.
- No regressions found.

## I3 - Implementation notes

1. **`/productlist/?productcat=<...>` masonry** (`mainapp/templates/ProductSection/productlist.html`, `_product_results.html`) — replaced the fixed `grid` + `h-52 object-cover` crop (which forced every product image, many of them arbitrary-aspect-ratio base64 images, into the same box) with the same CSS-columns masonry technique used on `/gallery/` and `shop.html`: `.product-masonry` (`columns-1 sm:columns-2 lg:columns-3`, `break-inside-avoid`), images at natural aspect ratio with `loading="lazy"`/`decoding="async"`. The style lives in `productlist.html`'s `extra_head` block, so it's already loaded on the page before the AJAX-swapped partial (`_product_results.html`) ever renders — no separate stylesheet needed for the AJAX path.

2. **Removed the public login/register flow**:
   - Deleted the `register` and `loginView` views (and the now-unused `generateUniqueRefId` helper) from `mainapp/views/system.py`, updated `views/__init__.py`'s re-exports accordingly.
   - Removed the `register/` and `login/` URL entries from `mainapp/urls.py`; kept `logout/` (still useful for the admin to end their session from the public site).
   - Deleted the `login.html` and `register.html` templates.
   - Set `LOGIN_URL = '/hpmadmin/login/'` in `handmadeprojects/settings.py`, then stripped every `@login_required(login_url='login')` down to a bare `@login_required` across `admin_views.py`, `product.py`, `user.py` (8 views) — they now all fall back to the new `LOGIN_URL`, so any admin-gated page an anonymous visitor hits redirects straight to the real Django admin login instead of a dead `/login/` route.
   - Removed the `login_required` decorator from `contactus` entirely — it was previously gating the public contact page behind login, which would have made contact permanently unreachable for every real visitor once the public login page was gone (this looks like a pre-existing bug, not intentional; fixing it here was necessary for the removal to not silently break contact access).
   - Removed the anonymous-branch "Log in"/"Get started" links from both the desktop and mobile nav in `base.html`; the authenticated branch (Dashboard/Profile/username/Log out) is untouched since it's still meaningful for the one account (the site owner) that can ever be logged in.
   - Cleaned up the now-stale `Disallow: /login/` and `Disallow: /register/` lines from `robots.txt` (`seo_views.py`).
   - `userdashboard`, `profile`, `add-to-favorites`, `edit-product`, `edit-developer`, `add-developer`, `add-intern`, `addproduct`, `edit_hero_images`, `analysis`, `add_video` all deliberately left in place and still fully functional — they're only ever reachable by whoever is authenticated, which after this change can only be the site owner via `/hpmadmin/login/` (same Django session, shared across the whole app).

3. **`/contactus/` — form removed** (`mainapp/templates/systemsetup/contactus.html`, `mainapp/views/system.py`): replaced the name/email/message form with the same "Contact us via Call / WhatsApp for any query or for mentoring" treatment used on the homepage — **+91 81692 39027** shown prominently plus `tel:+918169239027` (Call now) and `https://wa.me/918169239027` (WhatsApp) buttons. Simplified the `contactus` view down to a plain `render()` since there's no POST handler left to run (removed the now-dead `Contactus.objects.create(...)` form-submission logic and its unused imports).

### Verification

- `python manage.py check` — 0 issues after every change in this section.
- Booted the dev server and re-checked the full set of previously-passing routes from Task 5's I7 route audit, focused on the ones this section touches:
  - `/login/` → **404** (route gone), `/register/` → **404** (route gone).
  - `/hpmadmin/login/` → **200** (still the one working login page); `/hpmadmin/` → **302** (redirects there for anonymous, as before).
  - `/userdashboard/`, `/profile/`, `/add-to-favorites/1/`, `/addproduct/`, `/add-developer/`, `/edit_hero_images/` → all **302**, redirect target confirmed to be `/hpmadmin/login/?next=...` (previously `/login/?next=...` or, for `edit_hero_images`, the dead `/accounts/login/`).
  - `/contactus/` → **200**, form markup gone, phone number/Call/WhatsApp links present.
  - `/productlist/?productcat=hardwareprojects` → **200**, `product-masonry` class present, no more fixed `h-52` crop; re-verified the AJAX-filtered partial (`X-Requested-With` header) also renders the masonry markup correctly.
- Grepped every template for stray `{% url 'login' %}` / `{% url 'register' %}` / hardcoded `/login/` / `/register/` references — none remain outside the deleted files.
- No regressions found.

## I4 - Improvement list

Analysis only — nothing implemented here. Grounded in the current state of the codebase as of Task 6 (I1–I3), plus everything already flagged and left deferred across Task 5's I2 (bug scan), I5 (SEO audit) and this session's own changes.

### Code-side

- [ ] **Hardcoded `username != 'atharva'` admin check, duplicated 16 times across 8 files** (`admin_views.py` ×8, plus templates `ourteam.html`, `ourteam_profile.html`, `productinfo.html`, `internship_listing.html`, `youtube_projects.html`, `herosection.html`, `base.html` ×2) — brittle single-superuser pattern (Task 5 I2 bug #4, still unresolved). Replace with `is_staff`/a real permission check so it isn't tied to one hardcoded username string.
- [ ] **Hardcoded `SECRET_KEY` committed to source** (`handmadeprojects/settings.py`) — Task 5 I2 bug #1, still unresolved.
- [ ] **`DEBUG = True`** alongside production-style config (Task 5 I2 bug #2, still unresolved).
- [ ] **Wildcard `ALLOWED_HOSTS = ['*', ...]`** (Task 5 I2 bug #3, still unresolved).
- [ ] **`|safe` on admin-editable rich-text fields** — stored-XSS risk if any admin account is compromised (Task 5 I2 bug #6, still unresolved).
- [ ] **No `.gitignore`; `db.sqlite3` committed to the repo root** (Task 5 I2 bug #7, still unresolved).
- [ ] **No `MEDIA_ROOT`/real `ImageField`s — every image on the site is base64 inlined into a `TextField`** (Task 5 I2 bug #23 / I5 SEO item #18). This is the root cause of several other open items: bloated HTML payload on every list page, images invisible to Google Images, and the same payload sometimes rendered twice on one page (e.g. intern profile thumbnail + lightbox). Highest-leverage fix on this list.
- [ ] **Contact phone number hardcoded in 6 separate templates** (`welcome.html`, `contactus.html`, `base.html`, `productlist.html`, `productinfo.html`, `affiliateInfo.html`) — no single source of truth; a future number change means editing 6 files. Move to a settings constant + context processor, or a template include.
- [ ] **`Contactus` model + its admin registration are now semi-orphaned** — the public form that fed it was removed in this session (I3.3), so no new submissions can ever arrive; only historical rows remain viewable in `/hpmadmin/`. Decide: keep purely as an archive, or remove the model/admin registration/migration entirely.
- [ ] **`userdashboard`, `profile`, `add-to-favorites` (and the `UserDetails`/`UserFavProjects` models behind them) are now dead-end features** — since public registration/login was removed in I3.2, no visitor can ever reach them, and the site owner has no real reason to use a "user dashboard"/"favorites" screen meant for regular accounts. Worth a decision: repurpose, or remove this subsystem to cut maintenance surface.
- [ ] **Stale `oldCodes/render.yaml`** — references a wrong project/module name (Task 5 I2 bug #15, still unresolved).
- [ ] **Numeric-ID URLs instead of slugs** for `productinfo`, `intern_profile`, `accessoriesview`, `aicontentview` (Task 5 I5 SEO item #11, deferred — would need a redirect layer to avoid breaking existing links).
- [ ] **No ItemList/CollectionPage schema** on any listing page (Task 5 I5 SEO item #17, deferred).
- [ ] **Tailwind loaded via CDN with runtime JIT compilation** in `base.html` — real Core Web Vitals cost, Tailwind's own docs advise against this in production (Task 5 I5 SEO item #19, deferred; needs a build step / npm tooling not currently in the project).
- [ ] **Favicon/logo/OG-image all point to an external GitHub Pages repo** (`atharvapawar456.github.io/...`), now also used as the actual header brand logo added in this session's I1.1 — a third-party dependency for a core brand asset with no cache/CDN control (Task 5 I5 SEO item #26, deferred; no local asset exists yet to swap in).
- [ ] **No automated tests anywhere in the project** (`mainapp/tests.py` is the default empty stub) — every verification this session (and in Task 5) was manual dry-run testing against a live dev server. Any future change risks silent regressions with nothing to catch them automatically.
- [ ] **`STATICFILES_DIRS` duplicates the app's auto-discovered static folder**, producing ~250+ "Found another file with the destination path" warnings on `collectstatic` (found during Task 5 I4's dry run, cosmetic but should be cleaned up).
- [ ] **Sitemap silently truncates at 2000 products / 1000 shops/interns/videos/accessories/AI-content** (`seo_views.py`) — not a real problem yet at current volume, but no warning fires when a table crosses the cap (Task 5 I5 SEO item #23, deferred).
- [ ] **No image-sitemap (`<image:image>`) extension** despite an image-heavy catalog (Task 5 I5 SEO item #24, deferred — low value until the base64-image issue above is fixed).
- [ ] **Broad `except Exception` blocks remain in many views** (`viewShop`, `viewAllShop`, `accessoriesProjects`/`accessoriesView`, `aicontentList`/`aicontentView`, `productinfo`, `productlist`) — they already correctly return `status=500` now (Task 5 I6), but still swallow the real exception type; narrowing these to expected exception classes would make failures easier to diagnose.

### User-side (UX / product)

- [ ] **No pagination anywhere** — `productlist` (87+ products and growing), `allshops`, `internship_listing`, `aicontentlist`, `accessprodlist` all load and render the entire result set in one response. Will get slow and unwieldy as the catalog keeps growing; needs pagination or infinite-scroll.
- [ ] **Inconsistent visual polish across the site** — `engineering-projects/`, `ourteam/`, `ourteam/profile/`, `gallery/`, `productlist/` were modernized this session (breadcrumbs, gradient cards, masonry), but `accessprodlist.html`, `aicontentlist.html`, `accessprodview.html`, `aicontentview.html`, `video_player.html` and `active_earn_tasks.html` still use the older plain Bootstrap-ish design language — the site now reads as visually two different eras.
- [ ] **No lightbox/zoom on product gallery images** (`productinfo.html`) — team/intern photos got a fullscreen lightbox earlier, but product gallery images just sit in a static grid with no way to view them larger.
- [ ] **No site-wide "back to top"** on the now-longer masonry pages (`/gallery/`, `/productlist/`) — scrolling back up a long single-column masonry feed has no shortcut.
- [ ] **Header search only covers products** — there's no way to search interns, shops, team members, or accessories/AI-content from the global search box; visitors have to know which section to browse into first.
- [ ] **No floating/persistent Call-WhatsApp CTA** on deeper pages (`productinfo`, `shop`, `intern_profile`, etc.) — the new Call/WhatsApp contact block only lives on the homepage and `/contactus/`; a visitor deep in a product page has to navigate away to find contact info.
- [ ] **No custom 404/500 error pages** — likely still Django's bare default templates, which would look jarringly off-brand compared to the rest of the redesigned site.
- [ ] **No cookie-consent / privacy-policy / terms page**, despite the Ahrefs analytics script already running on every page load — a trust/compliance gap for a public-facing site.
- [ ] **No active-page highlighting in the nav** — the header nav (`base.html`) doesn't indicate which section the visitor is currently in.
- [ ] **No dark mode** — the whole site is light-theme only.
- [ ] **Inconsistent price formatting** — raw `{{ prodcost }}`/`{{ apsale }}`/`{{ aisale }}` values are rendered directly (e.g. "₹{{ product.prodcost }}") with no thousands-separator formatting, so a price like `15000` shows as "₹15000" instead of "₹15,000".
