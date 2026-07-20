# Task 3 — Business directory expansion, Ganpati shop, UI suggestions

**Scope of this file:** Analysis + plan + content suggestions only. **No application code.**  
**Related suggestions:**

- [ai-space/ai-suggestion/shop-card-improvements.md](../ai-suggestion/shop-card-improvements.md)  
- [ai-space/ai-suggestion/shop-info-page-improvements.md](../ai-suggestion/shop-info-page-improvements.md)

---

## 1. Assigned work

| ID | Request |
|----|---------|
| **I1** | Expand `/allshops/` beyond 1 business — suggest more shops fitting HandMadeProjects domain |
| **I2** | New shop: **Ganpati decoration designs** (multi-design gallery) + **100 AI image prompts** (you generate images, then add URLs to `bgallery`) |
| **I3** | Improve shop **card** + **shop info** look/details — suggestions only, under `ai-space/ai-suggestion/` |

---

## 2. Findings

### Product / domain

HandMadeProjects is a **student/maker + local business** platform:

- Engineering / IoT / software project catalog  
- Internships, team, gallery  
- **Business showcase** (`Businesswebinfo`) for local shops (e.g. Hotel Mauli–style AI content samples)  
- AI content packs strategy (`strategy/aiContent.txt`)  
- Live area cues: India, Mumbai-ish (Dadar), WhatsApp-first contact  

### Technical (shops)

| Item | Detail |
|------|--------|
| List route | `/allshops/` → `viewAllShop` → `BusinessSection/allshops.html` |
| Detail route | `/shop/<bname>/` → `viewShop` (`bname` case-insensitive) |
| Model | `Businesswebinfo`: `bname`, `bcat`, `bmainimg`, `btags`, `bhighlight`, `binfo`, `bownerimgs`, `bgallery`, `bytlinks`, `bweblinks` (`;`-separated multi-values) |
| Current UX | Basic cards; detail has hero, about, owner, flat gallery, raw links |
| Count | User reports **1** business listed — directory feels empty |

### Constraints for expansion

- No code in Task 3 — suggestions + prompts only.  
- New shops = new **DB rows** (admin or shell) once assets ready.  
- `bname` is URL slug source — use stable names **without** awkward spaces if possible, or match existing pattern (`Hotel-Mauli-Dadar-East` style).  
- Gallery scale (100 images) needs **load-more + lazy** on detail page (documented in I3 suggestions; implement later).

---

## 3. Assumptions

1. Domain fit = makers, education, electronics, AI/creative services, student life, **festival décor**, local hospitality, repair, co-working, printing — not random global brands.  
2. Suggested shops can be **real partners** or **demo/portfolio** listings (like AI trial shops).  
3. Ganpati shop is primarily a **design gallery / lead-gen** page (AI mockups → enquire for real décor).  
4. Images will be hosted externally (GitHub raw, CDN, Drive public) and pasted into `bgallery` as `;`-separated URLs.  
5. White marketplace shell (Task 2) stays; shop UI improvements align with merge-v1.  
6. User generates images offline using the 100 prompts below.

---

## 4. Dependencies

| Dependency | For |
|------------|-----|
| `Businesswebinfo` fields | Adding shops + gallery |
| Image host / CDN | 100 Ganpati assets |
| Optional: Django admin or management command later | Bulk insert (future task) |
| I3 docs | Template redesign when coding starts |
| Existing shop row | Pattern for copy (highlight length, HTML in `binfo`) |

---

## 5. I1 — Suggested shops to expand the directory

Use these as **directory seeds**. Adjust names/cities to real partners when available.  
Suggested `bname` values are URL-safe.

### A. Core domain (engineering / makers) — high priority

| # | bname (URL) | bcat | Why it fits | Highlight seed |
|---|-------------|------|-------------|----------------|
| 1 | `Circuit-Craft-Lab` | Electronics & components | Students buy parts for IoT kits | “Arduino, ESP32, sensors & starter kits for college projects.” |
| 2 | `PCB-Prototyping-Hub` | Hardware services | Complements hardwareprojects | “Fast PCB prototype & assembly guidance for final-year teams.” |
| 3 | `3D-Print-Works` | Digital fabrication | Mechanical + product mockups | “PLA/ABS prints, enclosures, and project casings.” |
| 4 | `Robotics-Garage` | Education / robotics | Workshops + kits | “Weekend robotics labs for school & engineering students.” |
| 5 | `EmbedLab-Studio` | Embedded systems | STM32/RPi projects | “Mentored embedded builds with demo-ready documentation.” |

### B. Software / AI / digital (platform strengths)

| # | bname | bcat | Why | Highlight seed |
|---|-------|------|-----|----------------|
| 6 | `PixelPrompt-AI` | AI content studio | Matches AI packs strategy | “Product photos, banners & social creatives for local brands.” |
| 7 | `CodeMentor-Desk` | EdTech / mentoring | Student audience | “Doubt-solving & project review for Django, ML & web apps.” |
| 8 | `WebCraft-MiniSites` | Web design | Single-page business sites | “Launch a clean one-page site for your shop in days.” |
| 9 | `DataStory-Charts` | Analytics freelancers | Internship-adjacent | “Simple dashboards & report packs for campus clubs.” |
| 10 | `Resume-Forge-Studio` | Career services | Portfolio + placements | “Project-first resumes and GitHub portfolio polish.” |

### C. Student life / campus-adjacent

| # | bname | bcat | Why | Highlight seed |
|---|-------|------|-----|----------------|
| 11 | `Campus-Print-Point` | Printing & binding | Reports, posters | “Project reports, posters & thesis binding near campus.” |
| 12 | `Maker-Cafe-Collab` | Co-working / cafe | Team meetups | “Wi-Fi, whiteboards & group project tables.” |
| 13 | `SkillSprint-Workshops` | Training | Skill growth | “Short courses: IoT basics, Python, UI with Tailwind.” |
| 14 | `Project-Docs-Desk` | Documentation | Delivery quality | “Synopsis, PPT & demo script writing support.” |
| 15 | `Internship-Connect-Desk` | Career / internships | Cross-link internships | “Curated internship prep & mock interviews.” |

### D. Local business / services (showcase + AI trial)

| # | bname | bcat | Why | Highlight seed |
|---|-------|------|-----|----------------|
| 16 | `Hotel-Mauli-Dadar-East` | Hospitality | Already in marketing notes | Keep existing if present |
| 17 | `FreshBite-Tiffin` | Food services | Local service demo | “Homestyle tiffins for students & working professionals.” |
| 18 | `BrightLook-Salon` | Beauty / salon | AI before/after creatives | “Grooming packages with festival-ready looks.” |
| 19 | `QuickFix-Mobile-Care` | Repair | Student device repair | “Screen & battery repair with same-day options.” |
| 20 | `GreenLeaf-Nursery` | Lifestyle | Visual gallery shop | “Indoor plants & desk greenery for hostels.” |

### E. Creative / festival / décor (sets up Ganpati shop)

| # | bname | bcat | Why | Highlight seed |
|---|-------|------|-----|----------------|
| 21 | `Ganpati-Decor-Designs` | Festival decoration | **I2 primary shop** | “100+ AI-assisted mandap & home décor design concepts.” |
| 22 | `Festive-Lights-Co` | Event lighting | Bundle with décor | “LED curtains, fairy lights & stage wash ideas.” |
| 23 | `Mandap-Florals-Studio` | Florals | Cross-sell | “Fresh & artificial floral themes for celebrations.” |
| 24 | `Eco-Idol-Concepts` | Eco festival | Green positioning | “Clay & eco-friendly idol presentation themes.” |
| 25 | `Event-Photo-Booth` | Events / photo | Gallery-heavy | “Backdrop & booth designs for society events.” |

### F. Stretch / later (directory depth)

| # | bname | bcat | Note |
|---|-------|------|------|
| 26 | `Drone-View-Media` | Aerial media | Simulation/hardware crossover |
| 27 | `Solar-Kit-India` | Green energy | Hardware projects |
| 28 | `SmartHome-Installers` | IoT services | Post-kit installation |
| 29 | `College-Merch-Press` | Merch / print | Club merchandise |
| 30 | `Open-Source-Meetup` | Community | Non-commercial community card |

**Recommended first wave to add (after assets):**  
`Ganpati-Decor-Designs` (I2) + 4–6 from A/B/C so directory shows **≥6–8** cards, not 1.

### Category taxonomy (for filters later)

`Electronics` · `Hardware services` · `Digital fabrication` · `Education` · `AI content studio` · `Web design` · `Hospitality` · `Festival decoration` · `Printing` · `Repair` · `Career services`

---

## 6. I2 — Ganpati decoration designs shop (spec)

### Shop record (draft for admin / future insert)

| Field | Suggested value |
|-------|-----------------|
| `bname` | `Ganpati-Decor-Designs` |
| `bcat` | `Festival decoration` |
| `btags` | `ganpati, decoration, mandap, eco-friendly, traditional, LED, premium, Mumbai, seasonal, AI-designs` |
| `bhighlight` | `Browse 100+ Ganpati decoration design concepts—eco, traditional, LED & premium themes—then request a custom quote.` |
| `bmainimg` | Use prompt **#001** output (hero mandap wide shot) |
| `binfo` | HTML sections: intro, style families, what’s included, areas, booking window, AI-mockup disclaimer |
| `bgallery` | `url1;url2;...;url100` (order: hero themes first, then by series) |
| `bweblinks` | Instagram + `https://wa.me/91XXXXXXXXXX` |
| `bytlinks` | Optional process reel |
| `bownerimgs` | Optional designer portrait |

**URL:** `/shop/Ganpati-Decor-Designs/` (exact match depends on stored `bname`).

### Image production workflow

1. Generate with prompts below (same style seed / brand colors if tool allows).  
2. Export web-optimized JPG/WebP (~1200–1600px wide).  
3. Host (GitHub `siteimages/ganpati-decor/`, Cloudflare R2, etc.).  
4. Build `bgallery` string with `;` separators, no spaces around `;` if possible.  
5. Set `bmainimg` to best wide hero.  
6. Only then create/update DB row.

### Style bible for all prompts (append mentally)

- Photorealistic or high-end 3D archviz  
- Indian festive context, respectful depiction of Lord Ganesha idols (clay/eco preferred)  
- Clean composition, Pinterest-quality, no watermarks, no text overlays  
- Lighting: warm festive gold + soft daylight or evening fairy lights  
- Aspect: **4:3 or 3:2** for gallery; **16:9** for heroes (#001–#005)

---

## 7. I2 — 100 AI image generation prompts

**Naming:** `GD-001` … `GD-100` → filename suggestion `ganpati-decor-001.jpg`.

### Series A — Hero / cover (001–010)

1. **GD-001:** Wide 16:9 photorealistic living-room Ganpati decoration, eco-clay Ganesha idol on wooden pedestal, banana leaves, marigold garlands, soft morning light, premium interior magazine style, no text.
2. **GD-002:** Grand society mandap entrance at dusk, marigold toran, LED fairy lights, rangoli foreground, devotees silhouettes soft bokeh, cinematic wide shot.
3. **GD-003:** Close-up beautifully decorated eco Ganesha idol with fresh flowers, diyas, incense smoke wisps, shallow depth of field, warm gold tones.
4. **GD-004:** Modern apartment balcony Ganpati setup, compact mandap, fairy lights, city skyline blurred evening, cozy festive mood.
5. **GD-005:** Overhead flat-lay of decoration materials: marigolds, fabric drapes, LED strings, clay diyas, bamboo sticks, styled product shot on white marble.
6. **GD-006:** Luxury hotel lobby mini-mandap, white and gold theme, crystal accents, professional event photography.
7. **GD-007:** Traditional Maharashtra wada-style courtyard Ganpati décor, rangoli, oil lamps, heritage architecture.
8. **GD-008:** Minimal Scandinavian-Indian fusion home décor for Ganpati, muted colors, single idol, greenery, architectural digest style.
9. **GD-009:** Kids-friendly bright Ganpati corner with paper crafts, balloons, colorful backdrop, cheerful daylight.
10. **GD-010:** Night-time illuminated mandap reflection on wet street after light rain, bokeh lights, festival atmosphere.

### Series B — Eco-friendly themes (011–025)

11. **GD-011:** Eco Ganpati mandap made of banana stem and coconut leaves, natural textures, outdoor garden setting.
12. **GD-012:** Terracotta and jute theme décor frame around clay Ganesha, earthy palette, soft studio light.
13. **GD-013:** Seed-kalash and tulsi plant integrated into decoration, sustainable festival concept, educational poster quality photo.
14. **GD-014:** Recycled paper flower backdrop in pastels behind small eco idol, craft aesthetic.
15. **GD-015:** Bamboo pavilion mandap with cloth canopy, rural eco resort vibe, golden hour.
16. **GD-016:** Clay diya pathways leading to eco idol, top-down pathway composition.
17. **GD-017:** Water-soluble color powders arranged artistically near eco idol (no mess realism), artistic still life.
18. **GD-018:** Biodegradable plate décor with sweets offering arrangement, food styling + décor hybrid.
19. **GD-019:** Vertical garden living wall as Ganpati backdrop, urban eco loft.
20. **GD-020:** Cow-dung cake art patterns as traditional eco backdrop element, respectful cultural documentation style.
21. **GD-021:** Palm-leaf woven panels forming mandap walls, artisan craftsmanship close detail.
22. **GD-022:** Eco idol immersion concept art: gentle riverbank farewell décor (tasteful, serene, no chaos).
23. **GD-023:** Brown kraft paper and dried flower rustic home mandap, Instagram flat aesthetic.
24. **GD-024:** Solar fairy lights on eco mandap at twilight, green-tech festival message without text.
25. **GD-025:** Family arranging banana-leaf décor together, candid warm photojournalism style.

### Series C — Traditional / classic (026–040)

26. **GD-026:** Classic red-yellow marigold full mandap, traditional cloth backdrop with zari border, temple-like home shrine.
27. **GD-027:** Paithani-inspired fabric drapes (colors only, no brand), rich Maharashtrian traditional décor.
28. **GD-028:** Silver and brass vessels arranged with mango leaves, classical still-life décor.
29. **GD-029:** Elaborate rangoli peacock design in front of traditional mandap, top-down + elevation composite feel.
30. **GD-030:** Wooden carved frame mandap, antique finish, oil lamp glow.
31. **GD-031:** Classic dhol-tasha inspired color accents in décor (visual motifs only), energetic festival interior.
32. **GD-032:** Traditional kolam / rangoli threshold with toran of mango leaves and marigolds.
33. **GD-033:** Temple shikhara-inspired backdrop silhouette in home setting, respectful stylization.
34. **GD-034:** Silk umbrella (chatra) decorative element above idol, royal traditional look.
35. **GD-035:** Classic white jasmine and tuberose garland focus, fragrance-evoking soft photo.
36. **GD-036:** Traditional kitchen-adjacent home shrine décor during festival cooking ambience (blurred background).
37. **GD-037:** Gold-plated frame (tasteful) with red velvet backdrop, old-world royal theme.
38. **GD-038:** Classic aarti thali arrangement foreground, mandap soft background bokeh.
39. **GD-039:** Multi-tier traditional fruit offering display (modak nearby), cultural food + décor.
40. **GD-040:** Full traditional living room wide shot, family-ready décor, bright natural window light.

### Series D — LED / modern lights (041–055)

41. **GD-041:** Neon soft-edge LED arch mandap, modern Mumbai apartment, purple-gold lighting.
42. **GD-042:** Pixel LED curtain backdrop shimmering behind idol, night indoor shot.
43. **GD-043:** Warm Edison bulb string canopy over seating + mandap, café-festival hybrid.
44. **GD-044:** Programmable RGB ambient wash on white drapes, contemporary event hall.
45. **GD-045:** Fiber-optic star ceiling effect above compact mandap, magical night mood.
46. **GD-046:** Mirror panel décor with LED edges, glam modern theme, high contrast.
47. **GD-047:** Floating shelf mandap with hidden LED strip under-glow, minimal modern home.
48. **GD-048:** Outdoor terrace LED tunnel walkway to Ganpati corner, long exposure light trails subtle.
49. **GD-049:** Candle + LED hybrid for safety-modern mix, intimate close composition.
50. **GD-050:** Stage-style uplighting on fabric columns, society pandal modern look.
51. **GD-051:** Interactive light floor panels (tasteful, not nightclub), futuristic festive lobby.
52. **GD-052:** Bluetooth speaker subtly integrated in décor furniture, lifestyle modern (no logos).
53. **GD-053:** Cold white + warm gold dual-tone LED mix, architectural lighting photography.
54. **GD-054:** Kids LED star projectors on ceiling with soft mandap, playful family night.
55. **GD-055:** Drone-view of LED-lit housing society courtyard pandal (high angle), festival campus vibe.

### Series E — Premium / luxury (056–070)

56. **GD-056:** White marble and gold leaf accent mandap, luxury villa interior, editorial photography.
57. **GD-057:** Fresh orchid and white rose premium floral mandap, five-star event quality.
58. **GD-058:** Crystal bead curtains framing idol, soft sparkle bokeh, elegant evening.
59. **GD-059:** Velvet lounge seating facing premium mandap, hospitality event setup.
60. **GD-060:** Designer acrylic transparent mandap structure with floral inserts, contemporary luxury.
61. **GD-061:** Black-gold premium theme with restrained festive accents, fashion-event aesthetic.
62. **GD-062:** Champagne gold balloon garland (tasteful, not childish) with premium florals.
63. **GD-063:** Luxury dining table festive centerpiece echoing mandap colors, tablescape photography.
64. **GD-064:** Designer backdrop with 3D relief panels painted ivory and gold.
65. **GD-065:** Premium outdoor lawn mandap with chandelier, twilight wedding-level production.
66. **GD-066:** White thematic “peace & purity” luxury home shrine, lots of negative space.
67. **GD-067:** Italian marble flooring reflection of decorated mandap, luxury real-estate vibe.
68. **GD-068:** Couture fabric waterfall drapes in ivory and blush, soft glamorous light.
69. **GD-069:** Private club lounge Ganpati corner, discreet premium décor.
70. **GD-070:** Hero product-style shot of premium décor package mockup boards leaning on easel (moodboards), studio lighting.

### Series F — Compact / budget / student-hostel (071–080)

71. **GD-071:** Hostel room corner Ganpati décor, bed and study table visible, realistic student life, cheerful thrifty décor.
72. **GD-072:** Shoe-box sized tabletop mandap, portable travel-friendly setup, clean desk photo.
73. **GD-073:** Budget crepe paper and balloon simple backdrop, bright and honest DIY look.
74. **GD-074:** Shared apartment common area mini-decoration, multi-roommate friendly.
75. **GD-075:** Foldable cardboard mandap structure painted gold, clever DIY engineering aesthetic.
76. **GD-076:** Only diyas and one garland minimal budget shrine, powerful simplicity.
77. **GD-077:** Wall-hook hanging mandap cloth for tiny rooms, space-saving design diagram-like photo (still photoreal).
78. **GD-078:** Second-hand furniture upcycled as pedestal with fabric cover, sustainable budget.
79. **GD-079:** Printable backdrop poster on wall (abstract festive pattern, no text), ultra-budget.
80. **GD-080:** Before/after split composition of bare corner vs decorated (single image split), marketing style.

### Series G — Themes & storytelling (081–090)

81. **GD-081:** Underwater-coral artistic backdrop (abstract festive, respectful idol placement), creative theme pandal.
82. **GD-082:** Space/galaxy subtle backdrop with gold stars, youth creative theme (keep idol traditional).
83. **GD-083:** Village farm theme with hay, clay pots, rural charm mandap.
84. **GD-084:** Library/knowledge theme: books and warm lamps near study-friendly shrine (student domain crossover).
85. **GD-085:** Rainy monsoon window with indoor décor coziness, tea cup foreground, lifestyle story.
86. **GD-086:** Women artisans installing floral décor, empowering documentary photo style.
87. **GD-087:** Children learning to make paper lanterns for décor, educational workshop scene.
88. **GD-088:** Night aarti moment, hands holding thali, mandap glow, emotional storytelling (faces optional soft).
89. **GD-089:** Community pandal long queue soft background, focus on beautiful entrance gate décor.
90. **GD-090:** Morning after setup: quiet empty hall with finished mandap, serene documentary wide shot.

### Series H — Detail shots & materials (091–100)

91. **GD-091:** Macro of marigold petals and gold thread, texture for website gallery detail tile.
92. **GD-092:** Macro LED fairy light bokeh abstract festive background (can use as card overlay).
93. **GD-093:** Hands tying toran on doorway, step-by-step process still.
94. **GD-094:** Fabric swatches board for décor planning (red, gold, green, ivory), flat-lay.
95. **GD-095:** Tool kit for décor install: zip ties, hooks, scissors, gloves, neat product layout.
96. **GD-096:** Safety-conscious LED adapter and cable management behind mandap (trust/ pro install).
97. **GD-097:** Close-up of eco idol face with soft sandal paste and flower crown, reverent detail.
98. **GD-098:** Rangoli chalk powders mid-creation, top-down process.
99. **GD-099:** Finished mandap name-plate area with decorative blank plaque (no readable text), designer mock region.
100. **GD-100:** Collage-ready 3x3 grid of mini décor thumbnails on one canvas (nine small scenes), for main shop card image alternative.

**Negative prompt (global, if tool supports):**  
`blurry, low-res, watermark, logo, readable text, garbled letters, extra limbs, disrespectful depiction, horror, violence, overcrowded chaos, stock photo watermark, cartoonish unless specified`

---

## 8. I3 — Shop UI suggestions (pointer)

Full write-ups (do not duplicate here):

| Topic | File |
|-------|------|
| List cards `/allshops/` | [`ai-space/ai-suggestion/shop-card-improvements.md`](../ai-suggestion/shop-card-improvements.md) |
| Detail `/shop/<name>/` | [`ai-space/ai-suggestion/shop-info-page-improvements.md`](../ai-suggestion/shop-info-page-improvements.md) |

**Summary for decision-makers:**

- **Cards:** merge-v1 style, tags, gallery count, category chips, filters when N grows.  
- **Info:** breadcrumb, stronger hero + CTAs, lazy/load-more gallery (required for 100 images), structured `binfo`, WhatsApp CTA, related shops.

---

## 9. Execution steps (future coding / ops — not done in Task 3)

| Step | Owner | Action |
|------|-------|--------|
| 1 | You | Generate images GD-001…100 using prompts |
| 2 | You | Host images; build URL list |
| 3 | Ops/Admin | Insert `Ganpati-Decor-Designs` + first-wave shops from I1 |
| 4 | Dev (later task) | Implement shop card + detail UI per I3 docs |
| 5 | Dev | Add gallery load-more + lazy-load for large shops |
| 6 | QA | `/allshops/` count > 1; open Ganpati shop; mobile gallery |

---

## 10. Out of scope (Task 3)

- Writing Django templates/views/models  
- Actually inserting DB rows  
- Generating binary images  
- Payments / booking engine  

---

## 11. Done criteria (Task 3)

- [x] Plan file `ai-space/tasks/task-3.md` with findings, assumptions, dependencies, steps  
- [x] I1 shop suggestions aligned to domain  
- [x] I2 shop spec + **100** image prompts  
- [x] I3 suggestions under `ai-space/ai-suggestion/`  
- [x] No application code  

---

## 12. Status

| Item | Status |
|------|--------|
| Analysis | Complete |
| I1 suggestions | Complete (30 concepts + first wave) |
| I2 prompts | Complete (100) |
| I3 markdown | Complete |
| Implementation | **Pending** (separate task) |

---

*Task 3 plan only. Next: generate assets → add shops → optional Task 4 UI implementation from ai-suggestion docs.*
