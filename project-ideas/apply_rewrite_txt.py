#!/usr/bin/env python
"""
Apply a rewritten concept .txt file to a product in the DB.

Expected plain-text layout (see re-write-ideas/p77.txt):
  Line 1: Product name
  About This Project  → highlight / short summary
  Tech / Abstract / Keywords / Project Description / Project Features
  Specifications → Hardware Components / Software Components
  Applications / Advantages / Limitations / Future Scope / Conclusion
  (Report Contents / Project Deliverables ignored — site injects fixed lists)

Usage (repo root):
  python project-ideas/apply_rewrite_txt.py --file project-ideas/re-write-ideas/p77.txt --id 77 --category hardware
  python project-ideas/apply_rewrite_txt.py --file project-ideas/re-write-ideas/p77.txt --id 77 --dry-run
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = REPO_ROOT / "test"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TEST_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handmadeprojects.settings")

import django  # noqa: E402

django.setup()

from mainapp.product_catalog import get_product, get_product_model  # noqa: E402
from project_details_html import (  # noqa: E402
    keywords_to_prodtags,
    normalize_details,
    structure_to_html,
    validate_details,
)

# Section headers as they appear in rewrite files (order-independent match)
SECTION_ALIASES = {
    "about this project": "highlighttitle",
    "about": "highlighttitle",
    "tech": "tech",
    "technologies": "tech",
    "abstract": "abstract",
    "keywords": "keywords",
    "project description": "project_description",
    "description": "project_description",
    "project features": "project_features",
    "features": "project_features",
    "specifications": "_specs_block",
    "hardware components": "hardware_components",
    "hardware": "hardware_components",
    "software components": "software_components",
    "software": "software_components",
    "applications": "applications",
    "advantages": "advantages",
    "limitations": "limitations",
    "future scope": "future_scope",
    "conclusion": "conclusion",
    "report contents": "_skip",
    "project deliverables": "_skip",
}


def _norm_header(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip().lower())


def parse_rewrite_txt(text: str) -> dict:
    """Parse rewrite plain text into product-details schema dict."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # Drop empty leading lines
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        raise ValueError("empty rewrite file")

    product_name = lines[0].strip()
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for raw in lines[1:]:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            if current and current not in ("_skip",):
                sections.setdefault(current, []).append("")
            continue

        key = SECTION_ALIASES.get(_norm_header(stripped))
        if key is not None:
            current = key
            sections.setdefault(current, [])
            continue

        if current is None:
            # orphan lines before first section → treat as highlight
            current = "highlighttitle"
            sections.setdefault(current, [])
        if current == "_skip":
            continue
        sections.setdefault(current, []).append(stripped)

    def join_para(key: str) -> str:
        parts = sections.get(key) or []
        # collapse blank runs
        out: list[str] = []
        for p in parts:
            if not p:
                if out and out[-1] != "":
                    out.append("")
                continue
            out.append(p)
        # paragraphs joined with space if single-line blocks, else double newline
        text_body = "\n".join(out).strip()
        # normalize multi-blank
        text_body = re.sub(r"\n{3,}", "\n\n", text_body)
        # if mostly single newlines (feature lists use join_list instead)
        return text_body

    def join_list(key: str) -> list[str]:
        items = []
        for p in sections.get(key) or []:
            p = p.strip().lstrip("-•* ").strip()
            if p:
                items.append(p)
        return items

    def join_comma_or_list(key: str) -> list[str]:
        raw_text = join_para(key)
        if not raw_text:
            return []
        # Keywords often one line comma-separated
        if "\n" not in raw_text and ("," in raw_text):
            return [x.strip() for x in raw_text.split(",") if x.strip()]
        return join_list(key)

    def join_inline(key: str) -> str:
        """Join list/para into comma-separated single line (tech, hardware)."""
        items = join_list(key)
        if items:
            # if already one line with commas, keep
            if len(items) == 1 and "," in items[0]:
                return items[0]
            return ", ".join(items)
        return join_para(key).replace("\n", " ").strip()

    # Specs block may contain nested "Hardware Components" lines before we see headers
    # If hardware/software only appear as subheads inside specs, re-parse specs body
    specs = join_para("_specs_block")
    if specs and not (sections.get("hardware_components") or sections.get("software_components")):
        hw, sw = [], []
        mode = None
        for line in specs.splitlines():
            h = _norm_header(line)
            if h in ("hardware components", "hardware"):
                mode = "hw"
                continue
            if h in ("software components", "software"):
                mode = "sw"
                continue
            if not line.strip():
                continue
            if mode == "hw":
                hw.append(line.strip())
            elif mode == "sw":
                sw.append(line.strip())
        if hw:
            sections["hardware_components"] = hw
        if sw:
            sections["software_components"] = sw

    highlight = join_para("highlighttitle")
    # first non-empty paragraph only for highlighttitle field
    if highlight:
        highlight = re.split(r"\n\s*\n", highlight)[0].replace("\n", " ").strip()

    data = {
        "product_name": product_name,
        "highlighttitle": highlight,
        "tech": join_inline("tech"),
        "abstract": join_para("abstract").replace("\n\n", "\n").replace("\n", " ").strip()
        if join_para("abstract").count("\n") < 3
        else join_para("abstract"),
        "keywords": join_comma_or_list("keywords"),
        "project_description": join_para("project_description"),
        "project_features": join_list("project_features"),
        "hardware_components": join_inline("hardware_components"),
        "software_components": join_inline("software_components"),
        "applications": join_list("applications"),
        "advantages": join_list("advantages"),
        "limitations": join_list("limitations"),
        "future_scope": join_list("future_scope"),
        "conclusion": join_para("conclusion"),
    }
    # Prefer multi-paragraph abstract/description/conclusion as joined paragraphs
    for k in ("abstract", "project_description", "conclusion"):
        if data[k]:
            # keep paragraph breaks
            data[k] = re.sub(r"[ \t]+\n", "\n", data[k])
            data[k] = re.sub(r"\n{3,}", "\n\n", data[k]).strip()
            # single newlines inside a para → space
            paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", data[k]) if p.strip()]
            data[k] = "\n\n".join(paras)

    return data


def apply_to_product(
    *,
    path: Path,
    prod_id: int,
    category: str,
    dry_run: bool = False,
    force_name: bool = True,
) -> str:
    text = path.read_text(encoding="utf-8")
    parsed = parse_rewrite_txt(text)
    details = normalize_details(parsed, product_name=parsed["product_name"])
    html = structure_to_html(details, product_name=details["product_name"])
    warns = validate_details(details)

    product = get_product(category, prod_id)
    if product is None:
        Model = get_product_model(category)
        raise SystemExit(
            f"Product not found: {category}/{prod_id} "
            f"(model={getattr(Model, '__name__', None)})"
        )

    tags = keywords_to_prodtags(details.get("keywords") or [])
    highlight = (details.get("highlighttitle") or parsed.get("highlighttitle") or "").strip()
    if not highlight:
        ab = details.get("abstract") or ""
        highlight = (ab.split(". ")[0] + ("." if ab else "")).strip()[:500]

    summary = (
        f"{category}/{prod_id} → {details['product_name'][:60]} | "
        f"prodinfo={len(html)}c tags={len(tags.split(',')) if tags else 0} "
        f"warns={len(warns)}"
    )
    if dry_run:
        return f"DRY {summary}"

    if force_name and details["product_name"]:
        product.productname = details["product_name"]
    product.highlighttitle = highlight or product.highlighttitle
    if tags:
        product.prodtags = tags
    product.prodinfo = html
    product.save()
    return f"UPDATED {summary}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Apply rewrite .txt to a product")
    p.add_argument("--file", "-f", type=Path, required=True)
    p.add_argument("--id", type=int, required=True, help="prodid")
    p.add_argument("--category", "-c", default="hardware")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--keep-name", action="store_true", help="Do not overwrite productname")
    args = p.parse_args(argv)

    path = args.file
    if not path.is_file():
        alt = REPO_ROOT / path
        if alt.is_file():
            path = alt
        else:
            raise SystemExit(f"File not found: {args.file}")

    msg = apply_to_product(
        path=path,
        prod_id=args.id,
        category=args.category,
        dry_run=args.dry_run,
        force_name=not args.keep_name,
    )
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
