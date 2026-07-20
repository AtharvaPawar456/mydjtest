# Reusable prompt: 3 improved UI designs for HandMadeProjects

Copy-paste into any design/coding assistant. Adjust constraints as needed.

---

## Prompt

```
You are a senior product designer + frontend implementer.

### Product
**HandMadeProjects** (live: https://www.handmadeprojects.in/) is a Django site for:
- Engineering / IoT / AI / software project catalog (categories: softwareprojects, hardwareprojects, mechanicalprojects, simulationprojects, kidsscience, kidscraft)
- Project detail pages (tags, gallery, cost, YouTube links)
- Team & internship listings
- Business “shop” showcase pages
- Gallery, favorites (logged-in), optional AI content packs & earn-tasks
- Brand: student makers, final-year projects, DIY, portfolio proof

### Current UI problems (baseline)
- Desktop uses a left gray sidebar; mobile hamburger drawer
- Tailwind via CDN + Font Awesome; indigo/purple accents, fairly generic
- Home: simple headline + image carousel + domain cards
- Welcome/landing has a separate top-nav layout (inconsistent with app shell)
- Dense feature set not reflected in clear IA or visual hierarchy
- Cards/lists feel basic; weak search-first discovery; mixed marketing vs app chrome

### Your task
Propose **3 clearly different improved UI directions** (not minor color tweaks). For each direction:

1. **Name & thesis** (one sentence)
2. **Visual system**: color, type, spacing, radius, light/dark
3. **Layout / IA**: nav pattern (top vs sidebar vs hybrid), homepage structure, how catalog + internships + shops fit
4. **Key components**: hero, project card, filters, empty/auth states
5. **Mobile strategy**
6. **What stays from current product** (routes/features must remain feasible)
7. **Implementation note**: Tailwind utility patterns only (CDN-friendly)

Then **implement each direction as a standalone static prototype**:
- Files: `improve-ui-1.html`, `improve-ui-2.html`, `improve-ui-3.html`
- **Only** Tailwind CSS via `https://cdn.tailwindcss.com` (optional Google Fonts link is OK; no other CSS frameworks)
- No Django templates, no backend — realistic mock content
- Homepage-focused but show nav to Projects / Shops / Team / Internships
- Responsive (mobile + desktop)
- Distinct enough that a stakeholder can pick one direction in a review

### Direction seeds (use or replace with better ones)
1. **Marketplace** — top nav, search-first, product cards with price/tags (commerce-clean)
2. **Dark maker lab** — sidebar “IDE/lab” shell, mono accents, dense technical lists
3. **Learning campus** — path-based curriculum, warm editorial type, progress milestones

### Output format
- Short comparison table (direction | best for | vibe)
- Then the 3 HTML files (complete, openable in browser)
- End with: which direction fits HandMadeProjects best and why (2–3 bullets)
```

---

## Quick compare (what we shipped in-repo)

| File | Direction | Best for | Vibe |
|------|-----------|----------|------|
| [`improve-ui-1.html`](../improve-ui-1.html) | Marketplace | Selling/browsing project kits | Clean light, indigo, search + cards |
| [`improve-ui-2.html`](../improve-ui-2.html) | Dark maker lab | Engineer/power users | Dark, neon, sidebar + terminal table |
| [`improve-ui-3.html`](../improve-ui-3.html) | Learning campus | Students & paths | Warm sand/teal, editorial, milestones |

## How to preview

Open each file in a browser (double-click or Live Server). No Django required.
