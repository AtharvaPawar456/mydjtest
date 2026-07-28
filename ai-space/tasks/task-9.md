# Task 9 — Product detail page UI improvements (`productinfo`)

**Goal:** Improve the project detail page UI/UX (reference:  
`http://127.0.0.1:8000/productinfo/hardware/16/` — *EBike Speed Controller System*),  
especially media gallery, hero carousel, CTA/payment polish, a new **Components** image section,  
and downloadable **About This Project** text.

**Constraint for this document:** Plan only — **no application code in this step**.

**Primary files:**  
`mainapp/templates/ProductSection/productinfo.html` ·  
`mainapp/views/product.py` ·  
`mainapp/templates/systemsetup/_call_whatsapp_buttons.html` ·  
`mainapp/templates/systemsetup/gallery.html` (reference for image loading) ·  
`mainapp/models.py` (if new media field)

---

## 1. Findings (current state)

| Area | Current behavior | Gap vs request |
|------|------------------|----------------|
| **Hero image** | Single static `product.mainimgbasetxt` in left column | Not a carousel; gallery images not included |
| **Project Gallery** | Below **About This Project**; Bootstrap-ish cards; full-width **Download** button under each image; images may load eagerly | Want gallery **above** About; **download icon overlay** bottom-right on image; **lazy/dynamic load** like `/gallery/` |
| **Gallery style** | Fixed `grid` + `max-h-[320px] object-contain` + label chip | `/gallery/` uses CSS-columns masonry + `loading="lazy"` + `decoding="async"` + `fetchpriority="low"` |
| **Lightbox** | Present (`.lightbox-trigger`) | Keep; ensure it still works after overlay/carousel changes |
| **Download JS** | `.downloadBtn` blob fetch (CORS-sensitive for GitHub raw URLs) | Overlay icon should reuse same download helper; CORS failures still possible for some hosts |
| **Block Diagram download** | No dedicated field; product 16 gallery is `file_1…file_4.png` only | Need a clear source: new field, or gallery entry convention, or labeled document |
| **CTA band** (`#contactus`) | Gradient indigo/blue + includes `_call_whatsapp_buttons.html` | Labels use `text-slate-500` → **low contrast** on blue (“Primary · +91 …”) |
| **Call / WhatsApp buttons** | Solid brand/emerald, no white border | Want **white border** (especially on gradient CTA) |
| **Payment Policy** | Plain white card, thick gray border, two bold lines | Looks dated vs rest of page; needs visual polish |
| **Components section** | **Does not exist** | Need new section + data source (model field or convention) |
| **About download** | No export | Need `.txt` download with HandMadeProjects branding + project URL top & bottom |
| **Section order** | Header → Documents → About → Gallery → CTA → Payment | Gallery must move **just above About** |

### Reference product (hardware/16)

- **Name:** EBike Speed Controller System  
- **Gallery:** 4 remote PNGs under `hmp_assets/.../_16_EBike_Speed_Controller_System/`  
- **Main image:** separate URL (should be **slide 1** of hero carousel)

### Partial include issue

`_call_whatsapp_buttons.html` is reused on light backgrounds (homepage, contact) **and** dark gradient CTA.  
Label classes are tuned for light surfaces → broken on `#contactus`.  
Plan: support a **variant** (e.g. `cta_variant="on-dark"`) rather than global color change that breaks other pages.

---

## 2. Assumptions

1. **Scope is primarily `productinfo.html` + view context** (and shared partial for CTA buttons). Apply site-wide only where the partial needs a dark/light variant.  
2. **Hero carousel media** = `[mainimgbasetxt] + gallery image URLs` (dedupe if main already in gallery), images only in slides; videos stay in gallery grid or as non-slide items.  
3. **Auto-scroll carousel** = client-side interval (e.g. 4–5s), pause on hover/focus, prev/next optional, accessible (buttons + `aria`).  
4. **Gallery “like `/gallery/`”** means: lazy attributes + natural aspect / masonry or simple lazy grid — **not** loading the site-wide gallery DB table; still product-scoped `product.gallery`.  
5. **Block Diagram download** = dedicated download control when we can resolve a block-diagram image:
   - Preferred: new optional field **or** gallery item whose label/filename contains `block` / `Block Diagram`, **or** first gallery image if product only has one schematic-style asset.  
   - For product 16 specifically, implementer should pick the correct file among `file_1…4` once assets are reviewed (or add explicit URL in data).  
6. **Components** images need storage analogous to `gallery` — new field `components` (`;`-separated URLs, optional `Label|URL`) default `"*"`. Empty → hide section.  
7. **About `.txt` download** is client-side: strip HTML from the About DOM (or a `data-plain` payload), wrap with branding lines, trigger `Blob` download as `.txt` (not server endpoint unless CORS/plain-text extraction fails).  
8. **Dark mode** must remain intact on all new UI.  
9. No change to SEO JSON-LD beyond optional image list if carousel is first image only (keep current Product image = main).

---

## 3. Dependencies

| Dependency | Role |
|------------|------|
| `productinfo.html` | Layout, section order, carousel, gallery, about export |
| `views/product.py` | Build `carouselImages`, `componentImages`, absolute project URL for download header |
| `models.ProductBase` (+ migration ×6 category tables + legacy `ProductInfo`) | Optional `components` TextField |
| `admin` / edit-product form | Edit `components` (and optionally document block-diagram URL) |
| `_call_whatsapp_buttons.html` | Dark-surface text + white button borders when on CTA |
| `gallery.html` pattern | `loading="lazy" decoding="async" fetchpriority="low"` (+ optional masonry CSS) |
| Existing download JS | Reuse blob/download logic for overlay + block diagram |
| Font Awesome (already on site) | Download / chevron icons |
| Tests | Template/view smoke for product with gallery; optional unit for components parse |

**Non-dependencies:** Changing productlist cards, shop pages, or Ollama/content generation.

---

## 4. Target UX (by section)

### A. Hero — auto-scroll carousel

- Left column becomes a **carousel viewport**.  
- Slide 0 = `mainimgbasetxt` (project thumbnail).  
- Following slides = remaining gallery **images** (not `*` placeholders).  
- Auto-advance; dots or counter; optional prev/next.  
- Respect `prefers-reduced-motion` (disable auto-scroll).

### B. Project Gallery (moved above About)

Order of main content stack (proposed):

1. Header (carousel + title/CTA)  
2. Documents (if any)  
3. **Project Gallery**  
4. **Components** (if any)  
5. **About This Project** (+ download .txt control)  
6. Contact CTA  
7. Payment Policy  

Gallery card UX:

- Image container `relative`.  
- **Download icon** absolute **bottom-right** overlay (rounded, semi-opaque bg, hover solid).  
- Lazy load attrs like `/gallery/`.  
- Keep lightbox on image click (download icon uses `stopPropagation`).  
- Drop bulky full-width Download button under the image (icon replaces it).  
- Prefer masonry or lighter card chrome to match site language.

### C. Block Diagram download

- Dedicated control in gallery header **or** near hero: **“Download Block Diagram”**.  
- Visible only when a block-diagram URL is available.  
- Same download helper as gallery images.

### D. Contact CTA band

- Fix label contrast: e.g. `text-white/80` or `text-brand-100` when `on-dark`.  
- Call + WhatsApp: add `border-2 border-white` (and keep readable hover states).  
- Prefer partial flag so non-CTA pages unchanged.

### E. Payment Policy

- Softer card: `rounded-2xl`, single border, icon row or two-step horizontal split (Advance 50% | Handover 50%).  
- Clear hierarchy; works in dark mode; less “heavy border-4” look.

### F. Components section

- Mirror Project Gallery structure (title, grid/masonry, overlay download, lightbox).  
- Data: new `components` field (`;`-separated URLs).  
- Empty / `*` → section hidden.

### G. Download About as `.txt`

Button near About heading: **Download as text**.

File content pattern:

```text
HandMadeProjects
https://www.handmadeprojects.in/productinfo/<category>/<id>/
(or current request absolute URL)

---
<plain-text about content>
---

HandMadeProjects
https://www.handmadeprojects.in/productinfo/<category>/<id>/
```

Filename suggestion: `{productname_slug}_about.txt`.

---

## 5. Execution steps (implementation order)

### Phase 1 — Structure & data

1. Add `components` TextField on `ProductBase` (+ legacy `ProductInfo`) with migration `0020_…`.  
2. Wire field in Django admin + `edit_product` / `add_product` forms (optional for add).  
3. In `productinfo` view:
   - Parse gallery (split `;`, strip empty/`*`).  
   - Build `carousel_images` = main first + unique gallery image URLs.  
   - Parse `component_images` via same pattern as gallery (or shared helper).  
   - Resolve `block_diagram_url` (convention: URL/filename contains `block` / `diagram`, or explicit optional field if added).  
   - Pass `project_absolute_url` for txt branding.

### Phase 2 — Template reorder & gallery UI

4. Move Gallery block **above** About.  
5. Restyle gallery: overlay download icon, lazy attrs, lighter cards / optional masonry CSS (copy from `gallery.html`).  
6. Unify download JS into one helper (`downloadMedia(src, filename)`) used by gallery, components, block diagram.

### Phase 3 — Hero carousel

7. Replace static hero `<img>` with carousel markup + auto-scroll script.  
8. Pause on hover/focus; keyboard-friendly controls; reduced-motion guard.

### Phase 4 — Components section

9. Add **Components** section (same media UX as gallery).  
10. Hide when no images.

### Phase 5 — About .txt export

11. Add download button; strip HTML to text (preserve line breaks roughly).  
12. Prefix/suffix branding + absolute project URL.

### Phase 6 — CTA + Payment polish

13. Update `_call_whatsapp_buttons.html` with optional dark/CTA variant (label color + white borders).  
14. Pass variant from productinfo CTA include only.  
15. Redesign Payment Policy card (two-step / cleaner layout).

### Phase 7 — Verify

16. Manual check on `/productinfo/hardware/16/` (gallery count, carousel includes main, overlay download, order).  
17. Check product **without** gallery / components (no empty sections, no JS errors).  
18. Check CTA labels readable on gradient; Call/WA white border.  
19. Dark mode smoke.  
20. Optional tests: parse helpers; productinfo 200 + contains “Project Gallery” before “About This Project” in HTML order.

---

## 6. Open decisions (resolve during implement if needed)

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Block diagram source | (a) filename heuristic (b) new `block_diagram` URL field (c) first gallery image | **(a)** for zero schema if names contain “block”; else **(b)** for clarity |
| Components storage | New DB field vs stuffing into `gallery` with prefixes | **New `components` field** — cleaner, matches request for separate section |
| Carousel includes videos? | Images only vs mix | **Images only** in carousel; videos remain in gallery grid |
| About text extraction | Client DOM strip vs server plain field | **Client strip** of `#details` content (simplest) |
| CTA partial change | Global styles vs variant param | **Variant param** so homepage/contact stay correct |

---

## 7. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| CORS blocks blob download from `raw.githubusercontent.com` / CDN | Fallback: open URL in new tab with `download` attr; show friendly toast on failure |
| Auto-scroll accessibility | Pause on hover; honor `prefers-reduced-motion` |
| Partial change breaks light pages | Only apply light text/white border when `variant="on-dark"` |
| Main image duplicated in carousel | Deduplicate by normalized URL |
| Empty gallery still shows section | Keep `nogallery` / empty list checks |
| Large base64 gallery entries | Lazy load still helps; carousel should prefer URL images |

---

## 8. Acceptance criteria

- [ ] `/productinfo/hardware/16/` hero is an **auto-scroll carousel** with **main thumbnail as first slide**.  
- [ ] **Project Gallery** sits **immediately above** “About This Project”.  
- [ ] Gallery images use **lazy loading** pattern aligned with `/gallery/`.  
- [ ] Each gallery image has a **bottom-right overlay download icon** (no bulky under-image button required).  
- [ ] **Block Diagram** download control works when a diagram URL is available.  
- [ ] CTA label text (Primary/Alternate phone lines) is **readable** on the blue gradient.  
- [ ] Call and WhatsApp buttons on that band have a **white border**.  
- [ ] **Payment Policy** section looks modernized and consistent with the page.  
- [ ] New **Components** image section exists (gallery-like), hidden when empty.  
- [ ] User can download **About This Project** as `.txt` with **HandMadeProjects** + project URL at **top and bottom**.  
- [ ] Dark mode + product pages without gallery still work.

---

## 9. Suggested implementation checklist (todo)

- [ ] I1 — Data: `components` field + migration + admin/edit form  
- [ ] I2 — View: carousel list, components list, block-diagram resolution, absolute URL  
- [ ] I3 — Reorder sections: Gallery (then Components) above About  
- [ ] I4 — Gallery UI: overlay download + lazy attrs + keep lightbox  
- [ ] I5 — Hero auto-scroll carousel (main first)  
- [ ] I6 — Block Diagram download control  
- [ ] I7 — About → `.txt` download with branding  
- [ ] I8 — CTA partial dark variant + white borders  
- [ ] I9 — Payment Policy UI polish  
- [ ] I10 — Manual QA on hardware/16 + empty-gallery product + dark mode  

---

## 10. Plan checklist (this document)

- [x] Analyze productinfo + gallery + CTA partial  
- [x] Record findings, assumptions, dependencies  
- [x] Execution steps and acceptance criteria  
- [x] Save as `ai-space/tasks/task-9.md`  
- [x] **No code written** in this planning step  

---

## 11. Implementation notes (done)

| Item | Status |
|------|--------|
| I1 `components` field + migration `0020` | Done |
| I2 View carousel / components / block diagram / absolute URL | Done (`product_media.py`) |
| I3 Gallery + Components above About | Done |
| I4 Overlay download + lazy + masonry + lightbox | Done |
| I5 Hero auto-scroll carousel (main first) | Done |
| I6 Block Diagram button (filename/label hints) | Done — show when name contains block/diagram/schematic/circuit |
| I7 About → `.txt` with HandMadeProjects + URL top/bottom | Done |
| I8 CTA `variant="on-dark"` white labels + borders | Done |
| I9 Payment Policy two-step card | Done |
| Tests | `test_product_media.py` + documents suite OK |

**Edit form:** gallery + components + documents textareas on `edit_product.html`.  
**Block diagram tip:** use `Block Diagram|https://…/file.png` in the gallery field so the download button appears.