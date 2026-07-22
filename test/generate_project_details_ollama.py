#!/usr/bin/env python
"""
Task 8: Generate full project details for products that still use promoimg.png.

Uses Ollama Cloud model gemma4:cloud (default). Standalone script under test/.

Examples (from repo root):
  set OLLAMA_API_KEY=...
  python test/generate_project_details_ollama.py --list
  python test/generate_project_details_ollama.py --dry-run --limit 2
  python test/generate_project_details_ollama.py --apply
  python test/generate_project_details_ollama.py --apply --id 57 --force

Auth:
  - Preferred: OLLAMA_API_KEY + host https://ollama.com (Cloud API)
  - Fallback: local Ollama signed-in (omit key; host http://localhost:11434)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# --- paths / Django bootstrap -------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = TEST_DIR / "output"
RAW_DIR = OUTPUT_DIR / "raw"
BACKUP_DIR = OUTPUT_DIR / "backup"
STRUCTURE_FILE = REPO_ROOT / "project-details-structure.txt"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TEST_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handmadeprojects.settings")

import django  # noqa: E402

django.setup()

from mainapp.product_catalog import ALL_PRODUCT_MODELS, find_product_by_id  # noqa: E402

from project_details_html import (  # noqa: E402
    abstract_to_highlight,
    extract_json_object,
    is_enriched,
    keywords_to_prodtags,
    normalize_details,
    structure_to_html,
    validate_details,
    word_count,
)

DEFAULT_MODEL = "gemma4:cloud"
PROMO_NEEDLE = "promoimg.png"
DEFAULT_SLEEP = 1.5

# Production catalog field schema (reference: /productinfo/hardware/33/ iBin page).
REFERENCE_SCHEMA_NOTE = """
Field schema reference (match live catalog pages such as productinfo/hardware/33/):
  Tech | Abstract | Keywords | Project Description | Project Features |
  Specifications (Hardware components + Software components) | Report Contents (fixed) |
  Applications | Advantages | Limitations | Future Scope | Conclusion
"""

SYSTEM_PROMPT = f"""You are a technical catalog writer for HandMadeProjects (final-year / diploma
IoT, embedded, hardware, and software projects). Write formal, precise, original content.

{REFERENCE_SCHEMA_NOTE}

Rules:
- Return ONLY a single JSON object (no markdown fences, no commentary).
- Do NOT invent fake paper titles, DOI, brand endorsements, or obscure part SKUs.
- Stay realistic for a student lab project (Arduino/ESP32-class unless the title implies otherwise).
- Project Features must be short bullet lines (like a product sheet), not long essays.
- Content must be specific to the given project title and existing context, not generic filler.
- Keywords should be comma-suitable technical tags (12–20 terms).
"""


def load_structure_text() -> str:
    """Depth guide from project-details-structure.txt (word budgets); field names follow product 33."""
    depth = ""
    if STRUCTURE_FILE.is_file():
        depth = STRUCTURE_FILE.read_text(encoding="utf-8").strip()
    return f"""{REFERENCE_SCHEMA_NOTE}

Content depth guidance (fold academic depth into the catalog fields above):
- Abstract: ~120–150 words (compact overview of objective, approach, tech, outcome)
- Project Description: ~200–350 words (problem, goals, approach, societal value — merges problem statement, motivation, objectives)
- Conclusion: ~120–180 words (outcomes, limitations trade-off, future impact)
- Project Features: 8–12 short bullet lines
- Advantages: 5–8 short points; Limitations: 4–6; Applications: 5–8; Future Scope: 4–6
- Tech / Specifications: realistic component lists for a student build

Extra academic depth reference (optional inspiration only — do NOT invent separate top-level keys for these unless mapped into the schema):
{depth or '(none)'}
"""


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def iter_promo_products():
    """Yield product instances whose main image references promoimg.png."""
    for Model in ALL_PRODUCT_MODELS:
        qs = (
            Model.objects.filter(mainimgbasetxt__icontains=PROMO_NEEDLE)
            .only(
                "prodid",
                "productname",
                "mainimgbasetxt",
                "prodtags",
                "prodcost",
                "highlighttitle",
                "prodinfo",
                "gallery",
                "ytlinks",
                "timestamp",
            )
            .order_by("prodid")
        )
        for obj in qs:
            yield obj


def product_context(obj) -> dict:
    plain = strip_html(obj.prodinfo or "")
    return {
        "prodid": obj.prodid,
        "category_slug": getattr(obj, "category_slug", "") or "",
        "productname": obj.productname or "",
        "prodtags": obj.prodtags or "",
        "highlighttitle": obj.highlighttitle or "",
        "existing_prodinfo_plain": plain[:2500],
        "prodinfo_len": len(obj.prodinfo or ""),
        "enriched": is_enriched(obj.prodinfo),
    }


def build_user_prompt(ctx: dict, structure_text: str) -> str:
    # Schema mirrors /productinfo/hardware/33/ field layout.
    schema = {
        "product_name": "string — full project title",
        "highlighttitle": "string — one-sentence product highlight (max ~40 words)",
        "tech": "string — comma-separated technologies / modules (like product page Tech section)",
        "abstract": "string — 120 to 150 words",
        "keywords": ["12 to 20 technical keyword terms"],
        "project_description": "string — 200 to 350 words covering problem, objectives, approach",
        "project_features": [
            "short bullet feature line 1",
            "short bullet feature line 2",
            "... total 8 to 12 concise bullets",
        ],
        "hardware_components": "string — comma-separated major hardware parts",
        "software_components": "string — comma-separated tools/platforms (e.g. Arduino IDE, cloud)",
        "applications": ["5 to 8 short application scenarios"],
        "advantages": ["5 to 8 short points"],
        "limitations": ["4 to 6 realistic constraints"],
        "future_scope": ["4 to 6 upgrade / extension ideas"],
        "conclusion": "string — 120 to 180 words",
    }
    return f"""Generate complete project details for this HandMadeProjects catalog entry.
Use the SAME field names and content style as the live reference page
http://127.0.0.1:8000/productinfo/hardware/33/ (Tech, Abstract, Keywords,
Project Description, Project Features, Specifications, Applications, Advantages,
Limitations, Future Scope, Conclusion).

PROJECT TITLE: {ctx['productname']}
CATEGORY: {ctx['category_slug'] or 'unknown'}
EXISTING TAGS: {ctx['prodtags'] or '(none)'}
EXISTING HIGHLIGHT: {ctx['highlighttitle'] or '(none)'}
EXISTING SHORT DESCRIPTION (plain text from current page, may be brief):
{ctx['existing_prodinfo_plain'] or '(none)'}

STRUCTURE / DEPTH GUIDE:
{structure_text}

Return JSON with exactly this shape (values filled in):
{json.dumps(schema, indent=2)}
"""


def make_ollama_client(host: str | None, api_key: str | None):
    try:
        from ollama import Client
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: install with  pip install ollama\n"
            f"({exc})"
        ) from exc

    key = api_key if api_key is not None else os.environ.get("OLLAMA_API_KEY")
    # Default: Cloud when key present, else local Ollama
    if host:
        resolved_host = host
    elif key:
        resolved_host = "https://ollama.com"
    else:
        resolved_host = "http://localhost:11434"

    headers = {}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    if resolved_host.rstrip("/").endswith("ollama.com") and not key:
        print(
            "WARNING: host is ollama.com but OLLAMA_API_KEY is unset. "
            "Set the key or use --host http://localhost:11434 after `ollama signin`.",
            file=sys.stderr,
        )

    return Client(host=resolved_host, headers=headers or None), resolved_host


def chat_json(client, model: str, system: str, user: str, *, temperature: float = 0.4) -> str:
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        stream=False,
        options={"temperature": temperature},
    )
    # ollama-python may return object or dict depending on version
    if isinstance(response, dict):
        return response.get("message", {}).get("content", "") or ""
    message = getattr(response, "message", None)
    if message is None:
        return ""
    if isinstance(message, dict):
        return message.get("content", "") or ""
    return getattr(message, "content", "") or ""


def stem_for(obj) -> str:
    slug = getattr(obj, "category_slug", None) or "project"
    return f"{slug}_{obj.prodid}"


def save_artifacts(stem: str, *, raw: str, details: dict, html: str) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{stem}.txt").write_text(raw, encoding="utf-8")
    (OUTPUT_DIR / f"{stem}.json").write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / f"{stem}.html").write_text(html, encoding="utf-8")


def load_cached_details(stem: str) -> dict | None:
    path = OUTPUT_DIR / f"{stem}.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (json.JSONDecodeError, OSError):
        return None


def generate_for_product(
    client,
    obj,
    *,
    model: str,
    structure_text: str,
    use_cache: bool,
    temperature: float,
) -> tuple[dict, str, str]:
    """
    Returns (normalized_details, html, raw_model_text).
    raw_model_text is empty when loaded purely from cache.
    """
    stem = stem_for(obj)
    if use_cache:
        cached = load_cached_details(stem)
        if cached:
            details = normalize_details(cached, product_name=obj.productname or "")
            html = structure_to_html(details, product_name=obj.productname or "")
            return details, html, ""

    ctx = product_context(obj)
    user = build_user_prompt(ctx, structure_text)
    raw = chat_json(client, model, SYSTEM_PROMPT, user, temperature=temperature)
    try:
        parsed = extract_json_object(raw)
    except (json.JSONDecodeError, ValueError):
        # one retry with stricter reminder
        raw = chat_json(
            client,
            model,
            SYSTEM_PROMPT + "\nIMPORTANT: Reply with pure JSON only. No markdown.",
            user + "\n\nYour previous reply was not valid JSON. Return pure JSON only.",
            temperature=min(temperature, 0.3),
        )
        parsed = extract_json_object(raw)

    details = normalize_details(parsed, product_name=obj.productname or "")
    html = structure_to_html(details, product_name=obj.productname or "")
    save_artifacts(stem, raw=raw, details=details, html=html)
    return details, html, raw


def apply_to_db(obj, details: dict, html: str, *, update_tags: bool) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stem = stem_for(obj)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIR / f"{stem}_{stamp}.html"
    backup_path.write_text(obj.prodinfo or "", encoding="utf-8")

    obj.prodinfo = html
    if update_tags:
        tags = keywords_to_prodtags(details.get("keywords") or [])
        if tags:
            obj.prodtags = tags
        hi = abstract_to_highlight(
            details.get("abstract") or "",
            fallback=details.get("highlighttitle") or "",
        )
        if hi and hi != "*":
            obj.highlighttitle = hi
    obj.save()


def cmd_list(products, *, verbose: bool = False) -> int:
    print(f"Promo-image products: {len(products)}")
    for obj in products:
        ctx = product_context(obj)
        flag = "ENRICHED" if ctx["enriched"] else "needs-gen"
        line = (
            f"  [{ctx['category_slug']}] id={ctx['prodid']:>4}  "
            f"prodinfo_len={ctx['prodinfo_len']:>5}  {flag}  {ctx['productname'][:70]}"
        )
        print(line)
        if verbose and ctx["existing_prodinfo_plain"]:
            print(f"      preview: {ctx['existing_prodinfo_plain'][:120]}...")
    return 0


def filter_products(products, args):
    out = list(products)
    if args.id is not None:
        out = [p for p in out if p.prodid == args.id]
        if not out:
            # allow --id on any product even if not promo (force re-gen path)
            found = find_product_by_id(args.id)
            if found is None:
                raise SystemExit(f"No product with prodid={args.id}")
            if PROMO_NEEDLE.lower() not in (found.mainimgbasetxt or "").lower():
                print(
                    f"NOTE: id={args.id} does not use promoimg.png; generating anyway.",
                    file=sys.stderr,
                )
            out = [found]
    if args.limit is not None and args.limit >= 0:
        out = out[: args.limit]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate full project details for promoimg.png catalog products via Ollama Cloud."
    )
    parser.add_argument("--list", action="store_true", help="List target products and exit")
    parser.add_argument("--dry-run", action="store_true", help="Generate files under test/output only (default if neither --apply nor --list)")
    parser.add_argument("--apply", action="store_true", help="Write prodinfo (and optional tags) to the database")
    parser.add_argument("--force", action="store_true", help="Regenerate/overwrite even if already enriched")
    parser.add_argument("--id", type=int, default=None, help="Only process this prodid")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N products")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--host",
        default=None,
        help="Ollama host (default: https://ollama.com if OLLAMA_API_KEY set, else localhost)",
    )
    parser.add_argument("--api-key", default=None, help="Override OLLAMA_API_KEY")
    parser.add_argument("--sleep", type=float, default=DEFAULT_SLEEP, help="Seconds between API calls")
    parser.add_argument("--no-cache", action="store_true", help="Ignore existing test/output/*.json")
    parser.add_argument("--update-tags", action="store_true", help="Also set prodtags + highlighttitle from JSON")
    parser.add_argument("--temperature", type=float, default=0.4)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    products = list(iter_promo_products())

    if args.list:
        return cmd_list(products, verbose=args.verbose)

    if not args.apply and not args.dry_run:
        # safe default
        args.dry_run = True
        print("Neither --apply nor --dry-run specified; defaulting to --dry-run.", file=sys.stderr)

    targets = filter_products(products, args)
    if not targets:
        print("No matching products.")
        return 0

    structure_text = load_structure_text()
    client, host = make_ollama_client(args.host, args.api_key)
    print(f"Model={args.model}  host={host}  targets={len(targets)}  apply={args.apply}")

    stats = {"generated": 0, "cached": 0, "skipped": 0, "applied": 0, "errors": 0}

    for i, obj in enumerate(targets):
        ctx = product_context(obj)
        label = f"[{ctx['category_slug']}/{obj.prodid}] {ctx['productname'][:60]}"

        if ctx["enriched"] and not args.force:
            print(f"SKIP (enriched) {label}")
            stats["skipped"] += 1
            continue

        stem = stem_for(obj)
        try:
            use_cache = not args.no_cache and not args.force
            # if force, still allow cache only when --no-cache is false AND user wants re-html?
            # Plan: --force means re-call model unless cache exists and we want to save money...
            # Prefer: --force + cache hit still uses cache unless --no-cache.
            details, html, raw = generate_for_product(
                client,
                obj,
                model=args.model,
                structure_text=structure_text,
                use_cache=use_cache,
                temperature=args.temperature,
            )
            if raw:
                stats["generated"] += 1
                print(
                    f"GEN  {label}  "
                    f"(abstract≈{word_count(details.get('abstract',''))}w, "
                    f"features={len(details.get('project_features') or [])})"
                )
                if args.sleep > 0 and i < len(targets) - 1:
                    time.sleep(args.sleep)
            else:
                stats["cached"] += 1
                print(f"CACHE {label}")

            warns = validate_details(details)
            if warns and args.verbose:
                for w in warns:
                    print(f"      warn: {w}")

            if args.apply:
                apply_to_db(obj, details, html, update_tags=args.update_tags)
                stats["applied"] += 1
                print(f"APPLY {label} → prodinfo ({len(html)} chars)  artifacts={stem}.*")
            else:
                print(f"DRY  {label} → test/output/{stem}.html")

        except Exception as exc:
            stats["errors"] += 1
            print(f"ERROR {label}: {exc}", file=sys.stderr)
            if args.verbose:
                import traceback

                traceback.print_exc()

    print(
        "Done.",
        f"generated={stats['generated']}",
        f"cached={stats['cached']}",
        f"skipped={stats['skipped']}",
        f"applied={stats['applied']}",
        f"errors={stats['errors']}",
    )
    return 1 if stats["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
