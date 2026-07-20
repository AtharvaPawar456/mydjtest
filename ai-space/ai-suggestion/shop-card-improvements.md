# Shop card improvements (`/allshops/`)

**Context:** Current card = image + name + category + highlight (2 lines) + “View Details”. Fits basic directory; under-sells marketplace white shell (Task 2) and AI/gallery-heavy shops (e.g. Ganpati designs).

**Goal:** Richer, scannable cards aligned with merge-v1 product cards — still white theme only.

---

## Problems today

1. No tags (`btags` unused on card).
2. No gallery density signal (user doesn’t know shop has 20+ designs).
3. Category is plain text; no visual chip system.
4. Double max-width padding with new `base.html` container (layout feels nested).
5. Weak hover/CTA vs product catalog cards.
6. No filter/search on directory when count grows beyond 1–10.
7. Placeholder on image error is generic; no brand fallback.

---

## Suggested card anatomy (desktop)

```
┌─────────────────────────────┐
│  Cover image (16:10)        │
│  [category chip]  [NEW?]    │
├─────────────────────────────┤
│  Shop name                  │
│  One-line highlight         │
│  tag · tag · tag            │
│  12 designs · Mumbai        │  ← derived/metadata if available
│  View profile →             │
└─────────────────────────────┘
```

### Fields to surface

| UI element | Source field | Notes |
|------------|--------------|--------|
| Cover | `bmainimg` | Object-cover; aspect fixed |
| Category chip | `bcat` | Brand indigo pill |
| Name | `bname` | Title case; 1 line clamp |
| Highlight | `bhighlight` | 2-line clamp |
| Tags | `btags` (split `,` or space) | Max 3 chips |
| Gallery count | `len(bgallery.split(';'))` | e.g. “24 photos” — needs template compute |
| CTA | link to `viewshop` | “View shop →” brand color |

Optional later (no model change if packed into `btags` / `binfo`): city, “AI designs”, “Open for collab”.

---

## Visual system (match merge-v1)

- Card: `rounded-2xl border border-slate-100 bg-white shadow-sm hover:shadow-lg hover:-translate-y-0.5`
- Image: `aspect-[16/10]` or fixed `h-52`
- Category: `text-[10px] font-bold uppercase bg-brand-50 text-brand-700 rounded-full`
- Tags: `bg-slate-100 text-slate-600 text-xs rounded-full`
- Grid: `1 / 2 / 3` cols same as product list
- Remove redundant outer `max-w-7xl` if base already wraps content

---

## Directory page (above the grid)

1. **Title block:** “Business Directory” + short SEO blurb + count.
2. **Search:** client filter by name/tags or GET `?q=` (view change later).
3. **Category chips:** hospitality, electronics, décor, education, AI services, makerspace… (derived from distinct `bcat` or fixed list).
4. **Empty state:** CTA “List your business” → contact.

---

## Priority implementation order

| P | Change | Effort |
|---|--------|--------|
| P0 | Marketplace card styles + tag chips + gallery count | Template only |
| P1 | Category filter chips | Template + light view |
| P2 | Search `?q=` | View + template |
| P3 | Featured / sponsored badge via tag `featured` | Convention only |

---

## Copy examples

- Highlight: keep benefit-first, ≤120 chars.
- CTA: “View shop →” / “See designs →” for gallery-heavy shops (`bcat` contains décor / design).
- Count line: “Showing 12 businesses · Dec · Services · Local”

---

## Accessibility

- Link wraps whole card or clear single focusable CTA (prefer whole-card `<a>` with aria-label including shop name).
- Alt text = shop name + category.
- Don’t rely on color alone for category (use text chip).

---

## Out of scope for card pass

- Map pins, ratings, phone click-to-call (nice later; need fields or encode in `binfo`).
- Infinite scroll (use simple pagination if >24 shops).
