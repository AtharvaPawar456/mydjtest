# Task 10 — Update product 77 from rewritten concept

**Goal:** Replace catalog content for  
`http://127.0.0.1:8000/productinfo/hardware/77/`  
using the rewritten concept in `project-ideas/re-write-ideas/p77.txt`.

---

## 1. Findings

| Item | Detail |
|------|--------|
| Target | `Project_Hardware` prodid **77** — *Smart Wearable Navigation Assistant for Blind People* |
| Source | `project-ideas/re-write-ideas/p77.txt` (structured plain text: Tech, Abstract, Keywords, Description, Features, Specs, Applications, …) |
| Current DB | Already has product-33 HTML (`hmp-full-project-details:v1`) but older concept (GPS/BLE-focused, shorter stack) |
| Rewrite focus | **Waist-mounted belt**, **3 ultrasonic sensors** (front/left/right), **Arduino Nano + ESP32**, custom **mobile app** + **multilingual voice**, custom **IoT server**, custom **PCB** |
| Image | Keep existing `mainimgbasetxt` / gallery unless rewrite provides new assets (none in `p77.txt`) |

---

## 2. Assumptions

1. Update **prodinfo HTML**, **highlighttitle**, **prodtags** (from Keywords), keep **productname** aligned with rewrite title.  
2. Map plain-text sections → product-33 schema via `test/project_details_html.structure_to_html`.  
3. Do not wipe gallery/documents/components.  
4. `prodid` stays **77** (no re-create).

---

## 3. Dependencies

- `project-ideas/re-write-ideas/p77.txt`  
- `test/project_details_html.py` (`normalize_details`, `structure_to_html`, `keywords_to_prodtags`)  
- `mainapp.product_catalog.get_product` / `Project_Hardware`  
- Optional reusable loader script under `project-ideas/` for future `pNN.txt` files  

---

## 4. Execution steps

1. Parse `p77.txt` into schema keys (tech, abstract, keywords list, description, features, hardware/software, applications, advantages, limitations, future_scope, conclusion, highlight).  
2. Build `prodinfo` HTML with `structure_to_html`.  
3. Update product 77 fields in DB.  
4. Verify `/productinfo/hardware/77/` shows new About content (belt, 3 sensors, Nano+ESP32, multilingual app).  

---

## 5. Acceptance criteria

- [x] Product 77 About content matches rewritten concept  
- [x] Keywords/highlight refreshed  
- [x] Page returns 200 with new sections (Tech, Abstract, Features, etc.)  
- [x] Task doc at `ai-space/tasks/task-10.md`  

---

## 6. Implementation notes (done)

| Item | Result |
|------|--------|
| Source | `project-ideas/re-write-ideas/p77.txt` |
| Loader | `project-ideas/apply_rewrite_txt.py` |
| Target | `hardware/77` — Smart Wearable Navigation Assistant for Blind People |
| Updated fields | `productname`, `highlighttitle`, `prodtags`, `prodinfo` (product-33 HTML) |
| Kept | images / gallery / documents / components |
| `prodinfo` size | ~11k HTML chars; validate warns = 0 |

### Re-run

```powershell
python project-ideas/apply_rewrite_txt.py --file project-ideas/re-write-ideas/p77.txt --id 77 --category hardware
python project-ideas/apply_rewrite_txt.py --file project-ideas/re-write-ideas/pNN.txt --id NN --category hardware --dry-run
```

### Rewrite content highlights applied

- Waist-mounted belt, 3 ultrasonic sensors (front/left/right)  
- Arduino Nano (sensing) + ESP32 (wireless)  
- Haptic motors + LED + buzzer  
- Custom mobile app, multilingual voice guidance  
- Custom IoT server + PCB prototype framing  

---

## I2 — Product CTA WhatsApp prefill (Option A) — done

**Accepted message template:**

```text
Hi HandMadeProjects,

I'm interested in this project:

{PROJECT_NAME}
{PROJECT_URL}

Please share details on complete package, documentation, cost, and timeline.
```

| Item | Detail |
|------|--------|
| Scope | All `/productinfo/.../` pages (Primary + Alternate WhatsApp) |
| Implementation | `build_product_cta_contact_numbers()` in `views/product.py` |
| Template | `productinfo.html` passes `contact_numbers=productCtaContactNumbers` |
| Call buttons | Still dial-only (`tel:`) — no body possible |
| Other pages | Homepage / contactus keep generic default message |

Tests: WhatsApp URL encodes interest line + project name/path.

### I2 add-on — Share this project (done)

Share buttons on product detail pages:
1. Header actions (next to Contact)
2. About section (next to Download as .txt)
3. Contact CTA band (below Call/WhatsApp)

Behavior: `navigator.share` when available; else copy project URL + toast “Project link copied”.

---

## I3 — Update product 15 from rewritten concept (done)

| Item | Detail |
|------|--------|
| Target | `http://127.0.0.1:8000/productinfo/hardware/15/` |
| Source | `project-ideas/re-write-ideas/p15.txt` |
| Loader | `python project-ideas/apply_rewrite_txt.py --file project-ideas/re-write-ideas/p15.txt --id 15 --category hardware` |
| Updated | `productname`, `highlighttitle`, `prodtags`, `prodinfo` (~11.8k HTML) |
| Kept | main image / gallery / documents / components |

### Rewrite highlights applied (p15)

- **Title:** Smart Pill Reminder and Automatic Medicine Dispensing System  
- 7-day circular organizer, multi-slot schedule via mobile app  
- Dual servo: rotate compartment + open lid  
- Arduino Nano + ESP32, IoT server, acknowledgement button  
- LED + buzzer alerts, transparent cover, PCB prototype framing