# Manual project-detail generation (ChatGPT)

Ollama Cloud credits exhausted — generate each project’s JSON with **ChatGPT**, save here, then apply to the DB.

## Field schema (target)

Same layout as live reference: **`/productinfo/hardware/33/`** (iBin)

| Order | Heading | JSON key |
|------:|---------|----------|
| 1 | Tech | `tech` |
| 2 | Abstract | `abstract` |
| 3 | Keywords | `keywords` (array) |
| 4 | Project Description | `project_description` |
| 5 | Project Features | `project_features` (array of short bullets) |
| 6 | Specifications | `hardware_components` + `software_components` |
| 7 | Report Contents | fixed by code (do not generate) |
| 8 | Applications | `applications` |
| 9 | Advantages | `advantages` |
| 10 | Limitations | `limitations` |
| 11 | Future Scope | `future_scope` |
| 12 | Conclusion | `conclusion` |

Also include: `product_name`, `prodid`, `category_slug`, `highlighttitle`.

See `_schema.example.json` and `_schema.keys.json`.

## Workflow

1. (Optional) Paste `_SYSTEM_PROMPT.md` into ChatGPT custom instructions.  
2. Open **`prompts/ideas-NN.prompt.md`** → copy the block under *Copy everything below this line*.  
3. ChatGPT replies with **raw JSON only**.  
4. Overwrite **`ideas-NN.json`** in this folder (delete `_todo` placeholder fields).  
5. Apply to database:

```powershell
# from repo root
python test/project-ideas/apply_ideas_json.py --dry-run
python test/project-ideas/apply_ideas_json.py --only 07
python test/project-ideas/apply_ideas_json.py
```

## Files

| Path | Role |
|------|------|
| `index.md` | Full list of 44 projects + status |
| `prompts/ideas-NN.prompt.md` | Ready-to-paste ChatGPT prompt |
| `ideas-NN.json` | Your filled JSON (placeholder until done) |
| `_manifest.json` | Maps NN → prodid / category |
| `apply_ideas_json.py` | Writes `prodinfo` HTML into Django DB |

## Tips

- Prefer **one project per ChatGPT chat** for quality.  
- If the model wraps JSON in \`\`\`json fences, strip the fences before saving.  
- Numbers already marked *already-enriched* in `index.md` were filled earlier via Ollama; you can skip them or re-generate with `--force` on apply.  
