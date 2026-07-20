# Task 4 — SEO improvements (plan + implementation list)

**Goal:** Improve HandMadeProjects for search engines and social previews.  
**Site:** https://www.handmadeprojects.in/  
**Stack:** Django + server-rendered templates (marketplace shell).

---

## 1. Findings (current state)

| Area | Status | Gap |
|------|--------|-----|
| `base.html` title/description/OG | Partial | No Twitter cards; weak `og:site_name`; keywords stuffed |
| Canonical | Present | Always full request URI (query strings create duplicates for `?q=`, `?stipend=`) |
| `robots.txt` / `sitemap.xml` | Files at repo root | **Not routed in Django** — crawlers on app host may 404 |
| Sitemap coverage | Static core URLs only | Missing products, shops, category productlist URLs, `allshops` |
| Structured data | None sitewide | No Organization / WebSite / Product / LocalBusiness JSON-LD |
| Page titles | Inconsistent | Several still say **DigitalAssets** / HandMadeProject (singular) |
| Private pages | Indexable | Login, register, dashboards, admin forms lack `noindex` |
| Welcome H1 | Good | Prototype badge copy (“white marketplace shell”) is non-SEO noise |
| Product/shop pages | Stronger meta | Good title/description blocks; still no JSON-LD |
| Performance SEO | CDN Tailwind | Acceptable for now; not blocking indexation |
| `DEBUG=True` / soft secrets | Ops risk | Not pure SEO but hurts trust/crawl in misconfigured deploys |

---

## 2. SEO improvement backlog (prioritized)

### P0 — Crawl & discoverability (implement now)

1. **Serve `robots.txt` via Django** pointing at live sitemap URL.  
2. **Serve dynamic `sitemap.xml`** including core pages + all products + visible shops + key list URLs.  
3. **Base meta upgrades:** Twitter Card, `og:site_name`, `og:locale`, `theme-color`, overridable `robots` meta.  
4. **JSON-LD Organization + WebSite** (with optional SearchAction to `/productlist/?q=`).  
5. **`noindex`** on auth and private/admin-ish pages (login, register, userdashboard, profile, add/edit forms).  
6. **Normalize brand in titles** (About, Contact, Gallery, etc. → HandMadeProjects).  
7. **Unique meta descriptions** where missing/weak.  
8. **Product JSON-LD** on product detail; **LocalBusiness-style** JSON-LD on shop detail.  
9. **Canonical hygiene:** block to allow path-only canonical on filtered lists (optional override).  
10. Clean welcome badge copy for cleaner brand signals.

### P1 — Content & on-page (follow-up)

11. Unique H1 + intro copy audit on category hubs still thin.  
12. Image `alt` pass on product cards and shop directory (many missing).  
13. Internal linking: footer/home → productcat URLs already good; add breadcrumb schema.  
14. Blog/resources section for long-tail (future content).  
15. `lastmod` in sitemap from model timestamps.

### P2 — Technical ops

16. Production `DEBUG=False`, secure SECRET_KEY, HTTPS force.  
17. Submit sitemap in Google Search Console / Bing.  
18. Fix soft 404s and empty product galleries.  
19. Core Web Vitals (self-host critical CSS later; reduce CDN Tailwind dependency).  
20. hreflang only if multi-language ships.

---

## 3. Assumptions

1. Public production host remains `https://www.handmadeprojects.in`.  
2. Django serves primary traffic (not only static files for robots/sitemap).  
3. Product URLs: `/productinfo/<id>/`; shops: `/shop/<bname>/`.  
4. Filtered query URLs (`?stipend=`, `?q=`) should not all be canonical self-URLs — prefer clean path canonical for lists.  
5. Implementation in this task covers **P0**; P1/P2 documented for later.

---

## 4. Dependencies

| Dependency | Use |
|------------|-----|
| `mainapp.urls` / views | robots + sitemap routes |
| `ProductInfo`, `Businesswebinfo` | Dynamic sitemap entries |
| `systemsetup/base.html` | Global meta + JSON-LD |
| Product/shop templates | Entity JSON-LD |
| Auth/admin templates | noindex |

---

## 5. Execution steps

| Step | Action | Status |
|------|--------|--------|
| 1 | Write this plan | Done |
| 2 | Add `robots_txt` + `sitemap_xml` views and URLs | Implement |
| 3 | Upgrade `base.html` SEO head + Organization JSON-LD | Implement |
| 4 | Fix titles/descriptions; noindex private pages | Implement |
| 5 | Product + shop JSON-LD; welcome copy tweak | Implement |
| 6 | Update static root `robots.txt` / `sitemap.xml` notes or keep as fallback | Implement |
| 7 | Smoke-check `/robots.txt`, `/sitemap.xml`, home head | Implement |

---

## 6. Out of scope (Task 4)

- Full content marketing / blog CMS  
- Paying for backlinks  
- Migrating off Tailwind CDN  
- Changing product URL structure to slugs (good idea later)

---

## 7. Done criteria

- [x] Plan file with listed improvements  
- [x] `/robots.txt` and `/sitemap.xml` work on Django  
- [x] Base has OG/Twitter + Organization schema  
- [x] Private pages `noindex`  
- [x] Brand titles fixed; product/shop structured data  
- [x] Welcome badge SEO copy cleaned  

## 8. Implemented files (P0)

| File | Change |
|------|--------|
| `ai-space/tasks/task-4.md` | Plan + backlog |
| `mainapp/seo_views.py` | Dynamic robots + sitemap |
| `mainapp/urls.py` | Routes for robots/sitemap |
| `mainapp/templates/systemsetup/base.html` | Meta, Twitter, JSON-LD, path canonical |
| `ProductSection/productinfo.html` | Product + Breadcrumb JSON-LD |
| `BusinessSection/shop.html` | LocalBusiness + Breadcrumb JSON-LD |
| Public templates titles/meta | About, Contact, Gallery, Team, YT, Interns, Shops |
| Auth/private templates | `noindex` |
| `robots.txt` (repo root) | Disallow private paths |

### Verify

```
http://127.0.0.1:8000/robots.txt
http://127.0.0.1:8000/sitemap.xml
```

View source on `/` for Organization + WebSite schema.

---

*Task 4 P0 complete. P1/P2 remain as follow-ups (alt text pass, GSC submit, DEBUG=False in prod).*
