#!/usr/bin/env python
"""
Load project-idea JSON (product-33 schema) into the HandMadeProjects catalog DB.

Default input: project-ideas/mechanical-ideas.json

Usage (from repo root):
  python project-ideas/idea-loaded.py
  python project-ideas/idea-loaded.py --file project-ideas/mechanical-ideas.json
  python project-ideas/idea-loaded.py --dry-run
  python project-ideas/idea-loaded.py --force
  python project-ideas/idea-loaded.py --force-category mechanical

JSON format: array of objects with keys like product_name, category_slug, tech,
abstract, keywords, project_description, project_features, hardware_components,
software_components, applications, advantages, limitations, future_scope,
conclusion, highlighttitle, (optional) mainimgbasetxt, documents, prodcost.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
IDEAS_DIR = Path(__file__).resolve().parent
TEST_DIR = REPO_ROOT / "test"
DEFAULT_FILE = IDEAS_DIR / "mechanical-ideas.json"
DEFAULT_IMG = (
    "https://raw.githubusercontent.com/AtharvaPawar456/HandMadeProjects/"
    "refs/heads/main/siteimages/promoimg.png"
)

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TEST_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handmadeprojects.settings")

import django  # noqa: E402

django.setup()

from mainapp.models import ProductCategory  # noqa: E402
from mainapp.product_catalog import get_product_model  # noqa: E402
from mainapp.product_categories_data import canonical_slug  # noqa: E402
from project_details_html import (  # noqa: E402
    keywords_to_prodtags,
    normalize_details,
    structure_to_html,
    validate_details,
)


def load_json_file(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, dict):
        # allow single object or {"ideas": [...]}
        if "ideas" in data and isinstance(data["ideas"], list):
            return data["ideas"]
        return [data]
    if not isinstance(data, list):
        raise SystemExit(f"Expected JSON array in {path}")
    return data


def ensure_category_row(slug: str) -> None:
    Model = get_product_model(slug)
    if Model is None:
        return
    ProductCategory.objects.get_or_create(
        slug=Model.category_slug,
        defaults={
            "name": Model.category_name,
            "legacy_slugs": "",
            "hashtags": "",
            "sort_order": 50,
            "is_active": True,
        },
    )


def idea_to_fields(idea: dict, *, force_category: str | None = None) -> dict:
    """Map idea JSON → model field dict (no save)."""
    details = normalize_details(idea, product_name=idea.get("product_name") or "")
    name = details.get("product_name") or idea.get("product_name") or ""
    if not name or name == "*":
        raise ValueError("missing product_name")

    slug_raw = force_category or idea.get("category_slug") or "mechanical"
    slug = canonical_slug(str(slug_raw).strip()) or "mechanical"
    Model = get_product_model(slug)
    if Model is None:
        raise ValueError(f"unknown category_slug: {slug_raw!r}")

    html = structure_to_html(details, product_name=name)
    tags = keywords_to_prodtags(details.get("keywords") or [])
    if not tags:
        # fallback from tech string
        tags = details.get("tech") or idea.get("prodtags") or "*"

    highlight = (details.get("highlighttitle") or idea.get("highlighttitle") or "").strip()
    if not highlight or highlight == "*":
        abstract = details.get("abstract") or ""
        first = abstract.split(". ")[0].strip()
        if first and not first.endswith("."):
            first += "."
        highlight = first[:500] if first else name

    mainimg = (idea.get("mainimgbasetxt") or idea.get("main_image") or "").strip()
    if not mainimg or mainimg == "*":
        mainimg = DEFAULT_IMG

    documents = (idea.get("documents") or "*").strip() or "*"
    gallery = (idea.get("gallery") or "*").strip() or "*"
    ytlinks = (idea.get("ytlinks") or "*").strip() or "*"
    prodcost = (idea.get("prodcost") or "*").strip() or "*"

    return {
        "Model": Model,
        "slug": slug,
        "fields": {
            "productname": name,
            "mainimgbasetxt": mainimg,
            "prodtags": tags if tags != "*" else (details.get("tech") or "*"),
            "prodcost": prodcost,
            "highlighttitle": highlight,
            "prodinfo": html,
            "gallery": gallery,
            "ytlinks": ytlinks,
            "documents": documents,
        },
        "warnings": validate_details(details),
    }


def upsert_idea(
    idea: dict,
    *,
    dry_run: bool,
    force: bool,
    force_category: str | None,
) -> str:
    mapped = idea_to_fields(idea, force_category=force_category)
    Model = mapped["Model"]
    fields = mapped["fields"]
    name = fields["productname"]
    slug = mapped["slug"]

    ensure_category_row(slug)
    existing = Model.objects.filter(productname=name).first()

    if existing and not force:
        # Skip if already has full detail HTML
        from project_details_html import is_enriched

        if is_enriched(existing.prodinfo) and len(existing.prodinfo or "") > 2000:
            return f"skip-exists id={existing.prodid} [{slug}] {name[:55]}"

    if dry_run:
        action = "would-update" if existing else "would-create"
        return (
            f"{action} [{slug}] {name[:55]} "
            f"prodinfo={len(fields['prodinfo'])}c warns={len(mapped['warnings'])}"
        )

    if existing:
        for k, v in fields.items():
            setattr(existing, k, v)
        existing.save()
        return f"updated id={existing.prodid} [{slug}] {name[:55]}"

    obj = Model.objects.create(**fields)
    return f"created id={obj.prodid} [{slug}] {name[:55]}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Load project idea JSON files into the catalog database."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=DEFAULT_FILE,
        help=f"JSON file (default: {DEFAULT_FILE})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse only; no DB writes")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing products with the same productname",
    )
    parser.add_argument(
        "--force-category",
        default=None,
        help="Force all ideas into this category slug (e.g. mechanical)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Load at most N ideas",
    )
    args = parser.parse_args(argv)

    path = args.file
    if not path.is_file():
        # allow relative to project-ideas/
        alt = IDEAS_DIR / path
        if alt.is_file():
            path = alt
        else:
            raise SystemExit(f"File not found: {args.file}")

    ideas = load_json_file(path)
    if args.limit is not None:
        ideas = ideas[: args.limit]

    print(f"Loading {len(ideas)} idea(s) from {path}")
    if args.force_category:
        print(f"Force category: {args.force_category}")
    if args.dry_run:
        print("DRY RUN — no database writes")

    stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
    for i, idea in enumerate(ideas, start=1):
        title = (idea.get("product_name") or "?")[:60]
        try:
            result = upsert_idea(
                idea,
                dry_run=args.dry_run,
                force=args.force,
                force_category=args.force_category,
            )
            print(f"[{i:02d}] {result}")
            if result.startswith("created") or result.startswith("would-create"):
                stats["created"] += 1
            elif result.startswith("updated") or result.startswith("would-update"):
                stats["updated"] += 1
            elif result.startswith("skip"):
                stats["skipped"] += 1
        except Exception as exc:
            stats["errors"] += 1
            print(f"[{i:02d}] ERROR {title}: {exc}", file=sys.stderr)

    print(
        "Done.",
        f"created/would-create={stats['created']}",
        f"updated/would-update={stats['updated']}",
        f"skipped={stats['skipped']}",
        f"errors={stats['errors']}",
    )
    return 1 if stats["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
