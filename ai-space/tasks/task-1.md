# Task 1 — Implementation Plan: Project Guide

**Goal:** Understand the repository and produce a proper `project-guide.md` (documentation only).  
**Scope of this file:** Analysis + plan. **No application code changes in this task.**  
**Deliverable of the follow-on work:** `project-guide.md` (recommended location: repo root or `ai-space/project-guide.md` — see Assumptions).

---

## 1. Assigned task (restated)

1. Analyze the codebase structure, stack, features, and conventions.
2. Draft a concise implementation plan (this document) covering findings, assumptions, dependencies, and execution steps.
3. Later: write a clear, accurate `project-guide.md` so a new contributor (or AI agent) can navigate, run, and extend the project without reverse-engineering.

---

## 2. Findings (codebase understanding)

### 2.1 What the product is

| Item | Detail |
|------|--------|
| **Product name** | HandMadeProjects |
| **Public site** | https://www.handmadeprojects.in/ |
| **Repo name** | `mydjtest` (GitHub workspace) |
| **Django project package** | `handmadeprojects` |
| **Main app** | `mainapp` (all domain logic, templates, static) |
| **Purpose** | Marketplace / content site for DIY, IoT, engineering student projects, accessories, AI content packs, earn-tasks, internships, team profiles, and business “shop” showcase pages |

### 2.2 Tech stack

| Layer | Choice |
|-------|--------|
| Framework | Django **5.0.3** (`requirements.txt`); settings comments still mention 4.0.6 |
| Server | Gunicorn + WhiteNoise |
| DB | `dj-database-url` → default **SQLite** (`db.sqlite3`); production can inject Postgres via env |
| Images | Pillow; many assets stored as **base64 text** or external URL strings, not FileFields |
| Frontend | Server-rendered HTML; **Tailwind via CDN**, Font Awesome CDN |
| Deploy | [Render](https://render.com) via `render.yaml` + `gunicorn handmadeprojects.wsgi:application` |
| Keep-alive | GitHub Action `.github/workflows/ping-render.yml` hits production every 15 minutes |
| Analytics | Ahrefs script in `base.html` |

### 2.3 Repository layout (high level)

```
mydjtest/
├── manage.py
├── requirements.txt
├── render.yaml
├── db.sqlite3                 # local SQLite DB (present in tree)
├── README.md                  # stub only ("mydjtest")
├── details.txt / p.txt        # ad-hoc notes, not formal docs
├── robots.txt, sitemap.xml
├── handmadeprojects/          # Django project (settings, root urls, wsgi/asgi)
├── mainapp/                   # single app: models, views, urls, admin, templates, static
│   ├── models.py
│   ├── views.py               # ~40+ view functions, ~670+ lines
│   ├── urls.py                # all app routes
│   ├── admin.py               # all models registered (plain)
│   ├── migrations/            # 0001–0010
│   ├── templates/             # feature folders (see below)
│   └── static/
├── static/                    # collected/copied admin + images (also under mainapp)
├── media/                     # present; media config largely unused/commented
├── strategy/                  # content/SEO notes (aiContent packs, seo-fix)
├── oldCodes/                  # legacy snippets
├── .github/workflows/         # Render ping
└── ai-space/tasks/            # AI task plans (this file)
```

### 2.4 Domain models (`mainapp/models.py`)

| Model | Role |
|-------|------|
| `UserDetails` | 1:1 with Django `User` — address, contact, unique **refid** |
| `UserFavProjects` | User ↔ `ProductInfo` favorites |
| `Contactus` | Contact form submissions |
| `TeamMember` | Team profiles (photo as base64 text) |
| `InternDetails` | Intern profiles + application/certificate links |
| `Homeimgs` | Hero / gallery image titles + links |
| `ProductInfo` | Core catalog: name, category, tags, cost, highlight, info, gallery/YT as semicolon-separated text |
| `YTvideos` | Standalone YouTube video list |
| `EarnTask` | Paid/affiliate-style tasks (title, amount, seats, status) |
| `AccessoriesProd` | Accessories catalog |
| `AicontentProd` | AI content product packs |
| `Businesswebinfo` | Business/shop pages (name, gallery, links as text fields) |

**Patterns:** Custom auto PKs (`prodid`, `aiid`, …); heavy use of `TextField` with default `"*"`; multi-value fields as **`;`-separated strings** rather than related tables.

### 2.5 Routing

- Root: `handmadeprojects/urls.py` → `include('mainapp.urls')` only.
- **Django admin URL is commented out** (`# path('hpmadmin/', admin.site.urls)`). Admin models are registered but the site is not mounted unless re-enabled.
- App routes (`mainapp/urls.py`) group into:
  - **System:** `/`, `/dashboard/`, gallery, contact, about, hero edit
  - **Auth:** register, login, logout
  - **User:** userdashboard, profile, favorites
  - **Catalog:** productlist, productinfo, add/edit product
  - **Categories:** kids-projects, engineering-projects
  - **YouTube:** youtube-projects, video-player, add-video
  - **Accessories / AI content:** list + detail
  - **Earn / affiliate:** earn-tasks, affiliateinfo
  - **Business shops:** allshops, shop/`<shopname>`
  - **Team / internships:** ourteam, internship*, add/edit developer/intern
  - **Admin-ish UI:** analysis, addproduct, etc.

### 2.6 Views & access control

- Single module: `mainapp/views.py`.
- Auth: Django session auth; `@login_required(login_url='/login')` on user and admin-ish pages.
- **Hard-coded superuser gate:** many write/admin views allow only `request.user.username == 'atharva'` (not `is_staff` / groups).
- Product categories used when adding products:  
  `softwareprojects`, `hardwareprojects`, `mechanicalprojects`, `simulationprojects`, `kidsscience`, `kidscraft`.
- Quick filters for software vs hardware tag chips in `getQuickFilters()`.
- Images for team/intern often uploaded then stored as **data-URL base64** in DB.

### 2.7 Templates & UI

- Base layout: `mainapp/templates/systemsetup/base.html` — Tailwind CDN, mobile nav + desktop sidebar, SEO/OG blocks.
- Feature folders: `ProductSection`, `YoutubeSection`, `TeamSection`, `InternSection`, `AccessoriesSection`, `AiContentSection`, `BusinessSection`, `earnTasks`, `AffiliateProgram`, `UserSection`, `projectscategory`, `systemsetup`.
- Branding assets often loaded from external GitHub Pages URL (`atharvapawar456.github.io/HandMadeProjects/...`).

### 2.8 Config & ops notes

- `DEBUG = True` currently; `SECRET_KEY` hardcoded in settings (security debt for guide’s “ops / caveats” section).
- `ALLOWED_HOSTS` includes `*`, localhost, `mydjtest.onrender.com`, plus Render hostname env.
- `TIME_ZONE = 'Asia/Kolkata'`.
- Static: WhiteNoise + `STATICFILES_DIRS` → `mainapp/static`; `STATIC_ROOT` = `staticfiles`.
- Local DB default: SQLite via `DATABASE_URL` / dj-database-url fallback.
- README is empty of useful onboarding content → **project-guide.md is the primary onboarding doc**.

### 2.9 Docs / non-code assets already present

- `strategy/aiContent.txt` — sample AI pack product copy.
- `strategy/seo-fix.txt` — SEO notes.
- `details.txt` — old setup/gunicorn reminders.
- `p.txt` — marketing WhatsApp copy for AI services.

---

## 3. Assumptions

1. **Task 1 deliverable is this plan only** (`ai-space/tasks/task-1.md`). Writing `project-guide.md` is the **execution phase** of this plan (or Task 1b), not mixed with code changes.
2. **`project-guide.md` path:** default **repo root** `project-guide.md` for maximum visibility; if the user prefers agent-local docs, use `ai-space/project-guide.md`. Plan execution should confirm once if ambiguous.
3. Audience is **developers and AI coding agents**, not end customers — tone is technical, factual, navigable.
4. Guide describes **current behavior as implemented**, including known shortcuts (hardcoded admin username, admin URL disabled, DEBUG True), without rewriting product strategy.
5. No requirement to fix security or refactor code as part of this documentation task.
6. Local run assumes Python 3.10+ (pycache shows 3.10 and 3.13), virtualenv, and `pip install -r requirements.txt`.
7. Production DB/env vars on Render are not fully visible in-repo; guide will document the **pattern** (`DATABASE_URL`, `RENDER_EXTERNAL_HOSTNAME`) rather than secret values.

---

## 4. Dependencies

| Dependency | Needed for |
|------------|------------|
| Accurate model/url/view inventory (done above) | Guide accuracy |
| `requirements.txt` versions | Setup section |
| `manage.py` / Django project name | Run commands |
| `render.yaml` + workflow | Deploy section |
| Template folder map | UI extension guide |
| User confirmation of guide **path** (root vs `ai-space/`) | Optional, if policy differs |
| *No* external API keys for docs | N/A |
| *No* code changes, migrations, or deploys for Task 1 | Plan-only constraint |

---

## 5. Target outline for `project-guide.md`

Recommended sections (concise, skimmable):

1. **Overview** — product purpose, live URL, repo vs package names  
2. **Stack & runtime** — Django, Gunicorn, WhiteNoise, DB, frontend CDN  
3. **Project structure** — tree with one-line roles  
4. **Local setup** — venv, install, migrate, runserver, create superuser (note admin URL may be disabled)  
5. **Configuration** — key settings, env vars, static/media, timezone  
6. **Architecture** — request flow: URL → view → model → template  
7. **Domain model** — table of models and relationships  
8. **URL map** — grouped routes with view names  
9. **Auth & authorization** — login/register, `UserDetails.refid`, username gate for admin UI  
10. **Feature areas** — products, YT, accessories, AI content, earn tasks, shops, team/interns  
11. **Templates & static conventions** — base blocks, Tailwind CDN, image storage style  
12. **Deployment** — Render build/start, WhiteNoise, keep-alive workflow  
13. **Common tasks** — add product, add team member, filter catalog, add shop  
14. **Caveats & tech debt** — hardcoded secrets/DEBUG, admin mount, stringly-typed multi-fields, base64-in-DB  
15. **Related files** — strategy notes, sitemap/robots  
16. **Glossary** — productcat values, field separators (`;`)

---

## 6. Execution steps (for writing the guide)

| Step | Action | Output |
|------|--------|--------|
| 1 | Confirm guide location (default: repo root `project-guide.md`) | Path decision |
| 2 | Write Overview + Stack from findings above | Draft sections 1–2 |
| 3 | Write Structure + Local setup with exact commands for this repo | Sections 3–4 |
| 4 | Document settings/env from `handmadeprojects/settings.py` (no secrets pasted if rotated later—note current risk) | Section 5 |
| 5 | Document models + relationships from `models.py` | Section 7 |
| 6 | Document URL groups from `mainapp/urls.py` + view roles | Sections 6, 8–10 |
| 7 | Document auth rules and admin username gate from `views.py` | Section 9 |
| 8 | Map template folders to features | Section 11 |
| 9 | Document Render + GitHub Action deploy/ops | Section 12 |
| 10 | Add “common tasks” runbooks and caveats | Sections 13–14 |
| 11 | Cross-check: every major model and route appears once; no invented APIs | QA pass |
| 12 | Keep README stub or add one-line pointer to `project-guide.md` **only if** user asks (out of scope unless requested) | Optional |

**Done criteria for the guide:**

- New contributor can install, migrate, and run locally from the guide alone.  
- New contributor knows where to add a model, view, URL, and template.  
- Feature list matches live routes/models.  
- Caveats include auth model and deployment reality.  
- No application code modified as part of documentation work.

---

## 7. Out of scope (explicit)

- Refactoring views/models or extracting apps  
- Enabling Django admin URL or replacing username checks  
- Security hardening (SECRET_KEY, DEBUG, ALLOWED_HOSTS)  
- Writing tests, CI for app code, or changing `render.yaml`  
- Customer-facing marketing copy (belongs in site/strategy, not engineering guide)

---

## 8. Risks / open points

| Risk | Mitigation in guide |
|------|---------------------|
| Admin site not routed | Document that management is mostly custom views + username check |
| README empty | Guide becomes source of truth |
| Secrets in settings | Call out risk; do not invent env-based secrets without implementing them |
| Dual static trees (`static/` vs `mainapp/static`) | Clarify `STATICFILES_DIRS` vs collected `staticfiles` |
| Stringly multi-value fields | Document `;` separators for gallery/links |

---

## 9. Status

| Item | Status |
|------|--------|
| Codebase analysis | **Complete** (for planning depth) |
| Plan file `ai-space/tasks/task-1.md` | **Complete** |
| `project-guide.md` written | **Pending** (next execution step) |
| Application code changes | **None** (by design) |

---

*Generated for Task 1. Next action when approved: author `project-guide.md` per sections 5–6.*
