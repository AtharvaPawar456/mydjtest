# Task 8 — Generate full project details for promoimg placeholder products

**Goal:** For every project whose `mainimgbasetxt` is (or contains) the shared placeholder image  
`https://raw.githubusercontent.com/AtharvaPawar456/HandMadeProjects/refs/heads/main/siteimages/promoimg.png`,  
generate rich, structured project-detail content (per `project-details-structure.txt`) using **Ollama Cloud** model **`gemma4:cloud`**, then persist it into each product’s `prodinfo` (and related fields where useful).

**Constraint for this document:** Plan only — **no application/feature code in this task step**. Implementation comes after plan approval.

**Site / stack:** Django HandMadeProjects · per-category models (`Project_Hardware`, etc.) · `prodinfo` is HTML rendered with `|safe` on `productinfo.html`.

---

## 1. Findings (current state)

| Area | Status | Gap |
|------|--------|-----|
| Placeholder image | Shared promo URL on seeded “project ideas” | Homepage already **excludes** cards whose image contains `promoimg.png` (`views/system.py`) — those products look thin in catalog/detail SEO |
| Local DB count | **44** rows with `mainimgbasetxt` containing `promoimg.png` (all currently `Project_Hardware` in local sqlite) | Live site sitemap also lists many hardware IDs (≈44–87) with the same promo image URL |
| Seed source | `mainapp/new_project_ideas_data.py` — **31** shortlist ideas + short `PRODINFO_TEMPLATE` (Name / Description / Tech / Applications / fixed Report Contents / Deliverables) | Content is **short marketing blurbs**, not full academic/engineering detail |
| Target structure | Root file `project-details-structure.txt` | Not yet mapped into HTML or used by any generator |
| Detail storage | `ProductBase.prodinfo` (`TextField`, HTML) | Detail page only has short sections today for promo-image products |
| Ollama / LLM | **None** in repo; `requirements.txt` has no `ollama` package | Need a **standalone** script under `/test` using Cloud API |
| Model | User-specified: **`gemma4:cloud`** | Accessible via Ollama Cloud (`https://ollama.com` + API key, or local `ollama` signed in + pull) |
| Output folder | User: **`/test`** | Folder does not exist yet — create under repo root as `test/` |

### `project-details-structure.txt` sections (must generate)

1. **Problem Statement** — 60–80 words  
2. **Background & Literature Context** — 120–150 words  
3. **Abstract** — 120–150 words  
4. **Objectives** — 120–150 words (primary + supporting)  
5. **Motivation & Need** — 120–150 words  
6. **Introduction** — 300–400 words  
7. **Execution Summary** — max 4 lines, ≤12 words each  
8. **Features & Functional Specifications** — major features, each 60–100 words  
9. **Keywords** — 16–32 terms  
10. **Advantages** — 8–10 points  
11. **Limitations** — 5–7 points  
12. **Applications** — 6–10 points  

### Existing content to feed the model (per product)

- `productname`  
- Existing short `prodinfo` / description / technologies (from seed or current HTML)  
- `prodtags`, `highlighttitle`, category (`hardware` for the bulk of promo rows)  
- **Do not invent fake BOM part numbers or false claims**; keep academic-project tone (final-year / diploma / IoT lab)

---

## 2. Assumptions

1. **Scope = image URL match**, not “all hardware”: any product in `ALL_PRODUCT_MODELS` where `mainimgbasetxt` contains `promoimg.png` (case-insensitive).  
2. **Primary write target is `prodinfo`** as styled HTML consistent with existing Tailwind section headings used in `PRODINFO_TEMPLATE` (so the detail page remains readable). Optionally refresh `prodtags` from generated Keywords and `highlighttitle` from Abstract first sentence — only if generation quality is good.  
3. **Image URL stays `promoimg.png`** for this task (no new art generation). Separate task if real thumbnails are needed.  
4. **Auth:** `OLLAMA_API_KEY` env var for direct Cloud API (`Client(host="https://ollama.com", headers=Authorization Bearer …)`), per [Ollama Cloud docs](https://docs.ollama.com/cloud). Fallback: local Ollama signed-in with `ollama pull gemma4:cloud`.  
5. **Generation is offline/batch** via a script under `test/` — not a public web endpoint (cost, rate limits, abuse).  
6. **Idempotent apply:** re-runs should not blindly overwrite good long content unless `--force`; default = skip products whose `prodinfo` already contains full section markers (e.g. “Problem Statement”).  
7. **Model output format:** prefer **JSON** (or strict markdown headings) from the model, then convert to HTML in Python — more reliable than asking for raw HTML.  
8. **Word counts** are targets; post-process lightly (trim / flag under/over) rather than infinite regenerate loops.  
9. **Cost/latency:** ~44 products × long multi-section prompts ≈ significant Cloud usage; script must support resume, dry-run, and single-id mode.  
10. **Secrets:** API key never committed; only env / local `.env` (gitignored if introduced).  

---

## 3. Dependencies

| Dependency | Why |
|------------|-----|
| `ollama` Python package | Official client for Cloud chat API |
| `OLLAMA_API_KEY` (or local Ollama + sign-in) | Authenticate to Cloud |
| Model `gemma4:cloud` available on account | User-specified model |
| Django DB access (same settings as `manage.py`) | Read promoimg products; write `prodinfo` |
| `mainapp.product_catalog.ALL_PRODUCT_MODELS` | Query across category tables |
| `project-details-structure.txt` | Prompt contract / section checklist |
| Existing short title/description/tech (seed or DB) | Grounding context for generation |
| Disk under `test/` | Script + optional cache of raw model responses |
| Network | Calls to `https://ollama.com` |

**Non-dependencies (out of scope for Task 8):** changing homepage featured filter, new product images, UI redesign of detail page, public “generate details” admin button (nice-to-have later).

---

## 4. Deliverables (when implementing — not this plan step)

| Path | Role |
|------|------|
| `test/` | Working folder for generation tooling |
| `test/generate_project_details_ollama.py` (name flexible) | **Separate** Python script: list targets → call `gemma4:cloud` → map structure → optional DB update |
| `test/prompts/` or inline prompt constants | System + user prompt templates aligned to `project-details-structure.txt` |
| `test/output/` (recommended) | Per-product raw JSON/markdown + final HTML (audit trail before DB write) |
| Optional: `test/requirements-ollama.txt` or note in README | `ollama` package pin |
| Optional: Django management command later | Thin wrapper around the same logic — **not required** if standalone script is preferred |

---

## 5. Implementation plan (execution steps)

### Phase A — Inventory & structure mapping

1. Create `test/` at repo root.  
2. Script step **list-targets**: for each model in `ALL_PRODUCT_MODELS`, filter `mainimgbasetxt__icontains="promoimg.png"`; print `category_slug`, `prodid`, `productname`, current `prodinfo` length.  
3. Define a Python dataclass / dict schema matching all 12 sections in `project-details-structure.txt`.  
4. Design `structure_to_html(data) -> str` using the same visual language as `PRODINFO_TEMPLATE` (h2 section titles, paragraphs, `ul`/`li` for lists) so dark-mode detail pages still look coherent.  
5. Decide markers for “already enriched” detection (e.g. presence of `Problem Statement` heading).

### Phase B — Ollama Cloud client (standalone file)

6. Add **one dedicated script** under `test/` (do not bury generation inside `views/`).  
7. Client setup (Cloud API mode):

   ```text
   Client(
     host="https://ollama.com",
     headers={"Authorization": "Bearer " + OLLAMA_API_KEY}
   )
   client.chat(model="gemma4:cloud", messages=[...], stream=False)
   ```

8. Prompt design:  
   - **System:** academic project writer; no fake citations; follow word budgets; return **only JSON** matching schema.  
   - **User:** product name + category + existing short description/tech/applications + paste section requirements from `project-details-structure.txt`.  
9. Parse JSON robustly (strip markdown fences if model wraps them); validate required keys; retry once on parse failure.  
10. CLI flags (recommended):  
    - `--dry-run` — generate to `test/output/` only  
    - `--apply` — write `prodinfo` to DB  
    - `--force` — overwrite even if already enriched  
    - `--id <prodid>` / `--limit N` — subset  
    - `--model gemma4:cloud` — default  
11. Rate-limit / sleep between calls; log token/errors; resume if output file already exists for that prodid.

### Phase C — Persist & verify

12. Dry-run on **1–2** products; human-spot-check word counts, tone, and HTML render on local `/productinfo/hardware/<id>/`.  
13. Batch remaining promoimg products with `--apply`.  
14. Spot-check SEO: `extractKeywords` on new `prodinfo`; detail page length; no broken HTML.  
15. Confirm homepage still correctly **hides** promoimg cards (unchanged behavior).  
16. Document how to re-run in `test/README.md` (env var, example commands).

### Phase D — Optional hardening (if time)

17. Unit-test pure functions: JSON→HTML, “already enriched” detector (no live Ollama in CI).  
18. Cache raw responses under `test/output/raw/` so re-formatting HTML does not re-bill the API.  
19. If Keywords are strong, optionally sync `prodtags` (comma-separated) on apply.

---

## 6. Prompt / data flow (summary)

```text
DB rows (promoimg.png)
    → productname + short context
    → Ollama Cloud gemma4:cloud  (JSON sections)
    → validate + structure_to_html()
    → test/output/<category>_<prodid>.html (+ .json)
    → optional: product.prodinfo = html; product.save()
```

---

## 7. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Model returns non-JSON / truncated long intro | Low temperature; JSON-only instruction; max tokens high enough; retry; split long sections into 2 calls if needed |
| Overwriting good content | Skip-unless-`--force`; backup `prodinfo` to `test/output/backup/` before write |
| API key leak | Env only; never commit keys; ignore `test/output` if it ever embeds secrets (it should not) |
| Hallucinated papers/brands | Prompt: no real citations; generic “existing systems” language |
| HTML injection / awkward tags | Escape user/model text when building HTML; allow only tags we emit |
| 44 × long generations = cost/time | `--limit`, resume, cache; run overnight if needed |
| Live prod DB vs local sqlite | Script must document which `DATABASE_URL` / settings it uses; default local; production apply is explicit |

---

## 8. Acceptance criteria

- [x] `test/` exists with a **standalone** Python generator script using **`gemma4:cloud`** via Ollama Cloud.  
- [x] Targets = all products whose image field references **`promoimg.png`**.  
- [x] Generated body covers **all sections** in `project-details-structure.txt` with approximate word/point counts.  
- [x] Dry-run path writes inspectable artifacts under `test/output/` (once API key is set and generation is run).  
- [x] `--apply` updates `prodinfo` (implemented; run locally with key to populate DB).  
- [x] Re-run without `--force` does not destroy already-enriched pages.  
- [x] No API keys in git; plan/code comments document `OLLAMA_API_KEY`.  
- [ ] Manual check on at least 2 product detail pages after first Cloud batch (operator step — needs `OLLAMA_API_KEY`).

---

## 9. Suggested CLI shape

```text
# from repo root, with Django settings available
set OLLAMA_API_KEY=...
python test/generate_project_details_ollama.py --list
python test/generate_project_details_ollama.py --dry-run --limit 2
python test/generate_project_details_ollama.py --apply --update-tags
python test/generate_project_details_ollama.py --apply --id 57 --force --no-cache
```

---

## 10. Out of scope / follow-ups

- Replacing `promoimg.png` with real project images or AI image gen.  
- Showing promoimg products in homepage “Featured” (currently excluded by design).  
- Renaming `/productlist` or marketing URL `/products` (handled elsewhere).  
- Wiring generation into Django admin UI.  
- Changing `DEBUG` / production deploy settings.

---

## 11. Plan checklist (this document)

- [x] Analyze task (promoimg products + structure file + Ollama Cloud)  
- [x] Record findings, assumptions, dependencies  
- [x] Execution steps and acceptance criteria  
- [x] Save as `ai-space/tasks/task-8.md`  
- [x] **No code written** in this planning step  

---

## 12. Implementation notes (done)

### Files

| Path | Role |
|------|------|
| `test/generate_project_details_ollama.py` | CLI: list / dry-run / apply; Ollama Cloud `gemma4:cloud` |
| `test/project_details_html.py` | Pure helpers: JSON extract, normalize, HTML render, enrichment detect |
| `test/test_project_details_html.py` | Unit tests (12) — no network |
| `test/requirements-ollama.txt` | `ollama>=0.4.0` |
| `test/README.md` | Operator docs |
| `test/.gitignore` | Ignores `output/`, `.env` |

### Behaviour

- Queries all `ALL_PRODUCT_MODELS` for `mainimgbasetxt__icontains=promoimg.png` (**44** local rows).  
- Default model **`gemma4:cloud`**; host `https://ollama.com` when `OLLAMA_API_KEY` is set, else localhost.  
- Model returns JSON → `structure_to_html()` → Tailwind section HTML matching existing catalog style + fixed Report Contents / Deliverables blocks.  
- Enrichment marker: HTML comment `<!-- hmp-full-project-details:v1 -->` (seed templates that only list “Problem Statement” under Report Contents are **not** treated as enriched).  
- Optional `--update-tags` sets `prodtags` + `highlighttitle` from Keywords / Abstract.  
- Resume: reuses `test/output/<category>_<id>.json` unless `--no-cache`.  
- `--apply` backs up previous `prodinfo` under `test/output/backup/`.

### Verified

- `python test/test_project_details_html.py -v` → **12 OK**.  
- `python test/generate_project_details_ollama.py --list` → **44** promo targets, all `needs-gen` before first successful apply.  
- Live Cloud batch **not** run in this session (`OLLAMA_API_KEY` unset). Operator should:

  ```powershell
  $env:OLLAMA_API_KEY = "..."
  pip install -r test/requirements-ollama.txt
  python test/generate_project_details_ollama.py --dry-run --limit 2 -v
  python test/generate_project_details_ollama.py --apply --update-tags
  ```
