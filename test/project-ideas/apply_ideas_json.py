#!/usr/bin/env python
"""
Apply completed ideas-NN.json files into product.prodinfo (product-33 HTML schema).

Usage (from repo root):
  python test/project-ideas/apply_ideas_json.py
  python test/project-ideas/apply_ideas_json.py --only 07
  python test/project-ideas/apply_ideas_json.py --dry-run
  python test/project-ideas/apply_ideas_json.py --force   # overwrite even if already enriched
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IDEAS_DIR = Path(__file__).resolve().parent
TEST_DIR = REPO_ROOT / "test"
BACKUP_DIR = TEST_DIR / "output" / "backup"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TEST_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handmadeprojects.settings")

import django  # noqa: E402

django.setup()

from mainapp.product_catalog import find_product_by_id  # noqa: E402
from project_details_html import (  # noqa: E402
    abstract_to_highlight,
    is_enriched,
    keywords_to_prodtags,
    normalize_details,
    structure_to_html,
    validate_details,
)


def load_manifest() -> list[dict]:
    path = IDEAS_DIR / "_manifest.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    # Fallback: scan ideas-*.json
    items = []
    for f in sorted(IDEAS_DIR.glob("ideas-*.json")):
        if f.name.startswith("ideas-_"):
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("_todo"):
            continue
        items.append(
            {
                "n": int(f.stem.split("-")[1]),
                "file": f.name,
                "prodid": data.get("prodid"),
                "category_slug": data.get("category_slug"),
                "productname": data.get("product_name"),
            }
        )
    return items


def is_complete(data: dict) -> bool:
    if data.get("_todo"):
        return False
    required = ("tech", "abstract", "project_description", "conclusion", "project_features")
    return all(data.get(k) for k in required)


def apply_one(path: Path, *, dry_run: bool, force: bool, update_tags: bool) -> str:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not is_complete(data):
        return "skip-incomplete"

    prodid = data.get("prodid")
    if prodid is None:
        return "skip-no-prodid"

    obj = find_product_by_id(int(prodid))
    if obj is None:
        return f"error-missing-db-id-{prodid}"

    if is_enriched(obj.prodinfo) and not force:
        return "skip-enriched"

    details = normalize_details(data, product_name=obj.productname or "")
    # Prefer identity from DB if model drifted
    details["product_name"] = obj.productname or details.get("product_name") or ""
    warns = validate_details(details)
    html = structure_to_html(details, product_name=obj.productname or "")

    if dry_run:
        return f"dry-ok warns={len(warns)} html_chars={len(html)}"

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUP_DIR / f"{obj.category_slug}_{obj.prodid}_ideas_{stamp}.html"
    backup.write_text(obj.prodinfo or "", encoding="utf-8")

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
    return f"applied warns={len(warns)} html_chars={len(html)}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply ideas-NN.json into product prodinfo")
    parser.add_argument("--only", type=str, default=None, help="Only idea number, e.g. 07 or 7")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--update-tags", action="store_true", default=True)
    parser.add_argument("--no-update-tags", action="store_true")
    args = parser.parse_args(argv)
    update_tags = not args.no_update_tags

    only_n = None
    if args.only is not None:
        only_n = int(args.only)

    manifest = load_manifest()
    stats = {"applied": 0, "skipped": 0, "errors": 0}

    for item in manifest:
        n = int(item["n"])
        if only_n is not None and n != only_n:
            continue
        path = IDEAS_DIR / item["file"]
        if not path.is_file():
            print(f"[{n:02d}] MISSING {path.name}")
            stats["errors"] += 1
            continue
        try:
            result = apply_one(path, dry_run=args.dry_run, force=args.force, update_tags=update_tags)
        except Exception as exc:
            print(f"[{n:02d}] ERROR {path.name}: {exc}")
            stats["errors"] += 1
            continue

        label = f"[{n:02d}] prodid={item.get('prodid')} {item.get('productname', '')[:50]}"
        if result.startswith("applied") or result.startswith("dry-ok"):
            print(f"{label} → {result}")
            stats["applied"] += 1
        elif result.startswith("skip"):
            print(f"{label} → {result}")
            stats["skipped"] += 1
        else:
            print(f"{label} → {result}")
            stats["errors"] += 1

    print(
        f"Done. applied/dry={stats['applied']} skipped={stats['skipped']} errors={stats['errors']}"
    )
    return 1 if stats["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
