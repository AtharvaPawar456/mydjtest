# Shop info page improvements (`/shop/<name>/`)

**Context:** `shop.html` shows main image + name/category/highlight, about HTML, owner faces, flat gallery grid, raw links, generic CTA. Works for Hotel Mauli–style pages; weak for **design portfolio shops** (Ganpati decorations with 50–100 gallery images).

**Goal:** Rich profile that still uses existing `Businesswebinfo` fields (`bname`, `bcat`, `bmainimg`, `btags`, `bhighlight`, `binfo`, `bownerimgs`, `bgallery`, `bytlinks`, `bweblinks`) — white theme, merge-v1 shell.

---

## Problems today

1. No breadcrumb (Home / Shops / Name).
2. Hero is flat 2-col; no sticky CTA, no tags, no “N designs in gallery”.
3. Gallery is equal tiles only — no lightbox, no categories, no video badge emphasis.
4. Long galleries (100 images) = heavy scroll / slow load; no “load more” or pagination.
5. Links dump raw URLs; no WhatsApp / Instagram button styling.
6. CTA is generic collaborate copy — not “Book decoration” / “Request quote”.
7. `binfo` is free HTML but no structured sections (services, pricing band, area served).
8. Visual mismatch with new marketplace product detail (breadcrumbs, rounded-2xl, brand CTAs).

---

## Suggested page structure

```
Breadcrumb
────────────────────────────────────
Hero: cover | name, cat chips, tags, highlight, primary CTA, secondary CTA
────────────────────────────────────
Stats strip: designs count | category | updated (btimestamp)
────────────────────────────────────
About (binfo) — prose / safe HTML
────────────────────────────────────
Services (optional parse from binfo headings OR fixed template blocks later)
────────────────────────────────────
Design gallery — filter chips + responsive masonry/grid + lightbox
────────────────────────────────────
Owner / team
────────────────────────────────────
Online presence — icon buttons (web, YouTube, IG if in weblinks)
────────────────────────────────────
Related shops (same bcat)
────────────────────────────────────
Bottom CTA band (brand gradient, like product list)
```

---

## Hero (details + look)

| Element | Suggestion |
|---------|------------|
| Cover | Large rounded-2xl, max height ~420px, object-cover |
| Title | `text-3xl md:text-4xl font-extrabold` |
| Category | Brand pill |
| Tags | From `btags` split |
| Highlight | Lead sentence under title |
| Primary CTA | “Contact / Enquire” → `contactus` or first WhatsApp link if present in `bweblinks` |
| Secondary | “View gallery” → `#gallery` |
| Share | Optional copy link (JS) |

For **Ganpati Deco shop** specifically:

- Primary: “Request design quote”
- Secondary: “Browse 100 designs”
- Badge: “Seasonal · Ganesh Chaturthi”

---

## Gallery UX (critical for multi-design shops)

1. **Section id=`gallery`** with count: “Gallery (87)”.
2. **Grid:** `grid-cols-2 md:grid-cols-3 lg:grid-cols-4` for design density; larger gap on desktop.
3. **Lightbox:** click opens full image (simple JS or CSS dialog) — no new dependency required if minimal.
4. **Lazy loading:** `loading="lazy"` on `<img>`.
5. **Video cells:** keep mp4 detect; overlay play icon; don’t autoplay all (perf) — prefer click-to-play for many items.
6. **Optional filters (convention):** encode in filename or query: `theme-eco`, `theme-traditional` — or prefix in URL path comment in admin notes. Without model change, use **tag groups in `btags`** and client-side filter only if data attributes added later.
7. **Load more:** show first 12–24, button reveals rest (client-side) for 100 images.

### Gallery caption convention (optional)

If image URLs can’t store titles, keep a companion line in `binfo` or use descriptive host filenames:  
`.../ganpati-eco-floral-01.png` → display humanized alt from filename.

---

## Content depth (what to put in DB)

Even without schema changes, improve **data quality**:

| Field | Recommendation |
|-------|----------------|
| `bhighlight` | One strong promise (max ~140 chars) |
| `binfo` | Structured HTML: Intro, Services (ul), Areas served, Season notes, How to book |
| `btags` | `ganpati, decoration, eco-friendly, traditional, Mumbai, seasonal` |
| `bgallery` | `;`-separated CDN/raw GitHub URLs; ordered best-first |
| `bweblinks` | Instagram, WhatsApp `https://wa.me/91...`, portfolio |
| `bytlinks` | Process reels / client testimonials |

**Suggested `binfo` outline for Ganpati shop:**

1. Who we are  
2. Decoration styles (eco, traditional, LED, premium mandap)  
3. What’s included (theme board, material list, on-site setup optional)  
4. Service areas  
5. Booking timeline (book 2–6 weeks before Chaturthi)  
6. Disclaimer (AI mockups vs on-site execution if applicable)

---

## Visual system

- Align with product detail: breadcrumb, white cards `rounded-2xl border border-slate-200`, brand CTAs `rounded-full`.
- Stats strip: 3–4 mini cards on slate-50.
- CTA band: `from-brand-600 to-violet-600` (same as catalog).
- Avoid gray-700 legacy footer conflicts (footer is global).

---

## SEO

- Title already uses shop name — good.
- Add H2s that match search intent: “Ganpati decoration designs”, “Eco-friendly mandap themes”.
- Gallery images: meaningful `alt` (shop name + design index or theme).
- JSON-LD `LocalBusiness` optional later.

---

## Priority implementation order

| P | Change | Effort |
|---|--------|--------|
| P0 | Breadcrumb, hero restyle, tags, gallery count, lazy load | Template |
| P1 | Load-more gallery + lightbox | Template + small JS |
| P2 | Related shops by `bcat` | View queryset |
| P3 | WhatsApp/primary CTA from `bweblinks` heuristic | Template logic |
| P4 | Filter chips by filename convention | Template + JS |

---

## Acceptance criteria (when implementing later)

- [ ] Page feels consistent with `/` and product detail (white marketplace).
- [ ] 100-image gallery usable on mobile (lazy + load more).
- [ ] User understands category, offer, and next action in &lt;5 seconds.
- [ ] No dark theme; brand indigo CTAs only.
