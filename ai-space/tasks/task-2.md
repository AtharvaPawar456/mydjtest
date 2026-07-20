# Task 2 — Sitewide marketplace UI (improve-ui-merge-v1)

**Status:** I1 shell implemented (base + welcome + auth + product list/detail polish)  
**Ref:** [`improve-ui-merge-v1/`](../../improve-ui-merge-v1/)  
**Theme:** White only (no dark mode)

---

## 1. Assigned work

| ID | Work |
|----|------|
| **Task 2 plan** | Findings, assumptions, dependencies, execution steps |
| **I1** | Implement merge-v1 UI properly on **every** app page |

**Source of truth**

- Home pattern → `improve-ui-merge-v1/index.html` → Django `/` (`welcome`)
- Detail/shell pattern → `improve-ui-merge-v1/detailed/` → shared `base.html` for all extending templates

---

## 2. Findings

| Area | Current | Target |
|------|---------|--------|
| `base.html` | Gray **sidebar** + mobile drawer + bottom nav | White **top nav**, promo bar, dark footer, no sidebar |
| `welcome.html` | Standalone old landing | Marketplace home matching merge-v1 |
| ~36 templates | `{% extends base.html %}` | Auto-inherit new shell when base changes |
| login/register | Standalone old Tailwind 2 forms | Align white brand chrome (optional extend base) |
| Search | None in chrome | Form GET → `/productlist/?q=` |
| Theme | Mixed | White/light surfaces + indigo brand only |

**Pages covered by base rewrite (extends base):** product list/info, shops, team, intern, gallery, about, contact, youtube, accessories, AI content, earn tasks, user dashboard/profile, admin forms, herosection/dashboard, etc.

---

## 3. Assumptions

1. Rewriting `base.html` is the correct way to hit every extending page.
2. Welcome should use the **same chrome** (extend `base.html`) to avoid dual systems.
3. Footer may stay dark slate (merge-v1); page chrome stays white.
4. No model/URL renames required for I1.
5. Font Awesome kept for existing page icons; shell itself can be SVG-light.
6. Static merge-v1 folder remains as design reference, not production routes.

---

## 4. Dependencies

- `improve-ui-merge-v1/index.html` + `detailed/index.html`
- `mainapp/templates/systemsetup/base.html`, `welcome.html`
- Named URLs: `welcome`, `engineering_projects_category`, `productlist`, `viewallshop`, `internship_listing`, `our_team`, `gallery`, `login`, `register`, `profile`, `logout`, `addproduct`, etc.
- Tailwind CDN + optional Inter font + brand config

---

## 5. Execution steps (I1)

| # | Step | Result |
|---|------|--------|
| 1 | Write this plan | `task-2.md` |
| 2 | Replace `base.html` with marketplace shell + auth-aware nav + messages | All extends pages |
| 3 | Rebuild `welcome.html` as merge-v1 home content (extends base) | `/` |
| 4 | Align login/register to white marketplace look | Auth pages |
| 5 | Spot-check product list/detail padding; fix only if broken | Detail UX |
| 6 | Manual smoke: `/`, list, detail, shops, intern, login | Done criteria |

---

## 6. Out of scope (I1)

- Per-page full visual redesign of every card (shell first; content polish iterative)
- Dark theme / improve-ui-2/3
- New backend features

---

## 7. Done criteria

- [x] Plan documented  
- [x] Every `extends base` page shows white top-nav shell (via `base.html` rewrite)  
- [x] `/` matches merge-v1 marketplace home structure with real URLs  
- [x] Search submits to product list  
- [x] Auth pages use white marketplace shell  
- [x] White theme only  
- [ ] Optional: restyle remaining page *inner* cards (team/shop grids) to match merge-v1 cards 1:1  

## 8. Files changed (I1)

| File | Change |
|------|--------|
| `mainapp/templates/systemsetup/base.html` | Marketplace top nav + promo + footer |
| `mainapp/templates/systemsetup/welcome.html` | merge-v1 home, extends base |
| `mainapp/templates/systemsetup/login.html` | Extends base, white form |
| `mainapp/templates/systemsetup/register.html` | Extends base, white form |
| `mainapp/templates/ProductSection/productlist.html` | Catalog header/search chips |
| `mainapp/templates/ProductSection/productinfo.html` | Breadcrumb + detail chrome |
| `ai-space/tasks/task-2.md` | This plan |

## 9. How to verify

```bash
pip install -r requirements.txt
python manage.py runserver
```

Open `/`, `/productlist/`, a product detail, `/allshops/`, `/login/`. Confirm top nav (no sidebar) and white theme.

---

*I1 complete for shell sitewide; inner content polish can continue incrementally.*
