# Task 8 — Project detail generation (Ollama Cloud)

Standalone tooling to fill **full project details** for catalog products that still use the shared placeholder image:

`https://raw.githubusercontent.com/AtharvaPawar456/HandMadeProjects/refs/heads/main/siteimages/promoimg.png`

**Field schema** matches the live reference page  
`/productinfo/hardware/33/` (iBin): Tech → Abstract → Keywords → Project Description → Project Features → Specifications → Report Contents → Applications → Advantages → Limitations → Future Scope → Conclusion.

Word-depth guidance still draws from `project-details-structure.txt` (abstract / description length, etc.).

## Setup

```bash
pip install -r test/requirements-ollama.txt
```

**Auth (pick one):**

1. **Cloud API (recommended)**  
   Create a key at https://ollama.com/settings/keys then:

   ```powershell
   $env:OLLAMA_API_KEY = "your_key_here"
   ```

2. **Local Ollama + cloud model**  
   `ollama signin` then `ollama pull gemma4:cloud`  
   Run with `--host http://localhost:11434` (no API key required if signed in).

Default model: **`gemma4:cloud`**.

## Commands (repo root)

```powershell
# Inventory
python test/generate_project_details_ollama.py --list

# Generate 2 products to test/output only
python test/generate_project_details_ollama.py --dry-run --limit 2

# Generate all missing (skip already enriched) and write DB
python test/generate_project_details_ollama.py --apply --update-tags

# Force one product
python test/generate_project_details_ollama.py --apply --id 57 --force --no-cache
```

## Artifacts

| Path | Meaning |
|------|---------|
| `test/output/<category>_<id>.json` | Normalized model JSON (resume cache) |
| `test/output/<category>_<id>.html` | Final `prodinfo` HTML |
| `test/output/raw/<category>_<id>.txt` | Raw model reply |
| `test/output/backup/...` | Previous `prodinfo` before each `--apply` |

## Unit tests (no API key)

```powershell
python -m unittest test.test_project_details_html -v
```

Or from `test/`:

```powershell
cd test
python test_project_details_html.py -v
```

## Notes

- Default without flags is **`--dry-run`** (no DB writes).  
- Already-enriched pages (HTML contains `hmp-full-project-details:v1`, or ≥3 exclusive full-detail section titles) are skipped unless `--force`. Short seed templates that only list “Problem Statement” under Report Contents are **not** treated as enriched.  
- API keys must never be committed.  
