"""
Pure helpers: project-details JSON → Tailwind HTML matching the production
catalog schema used by /productinfo/hardware/33/ (iBin reference page).

Also supports enrichment detection and robust JSON extraction.
No Django / Ollama imports (unit-testable offline).
"""
from __future__ import annotations

import json
import re
from html import escape
from typing import Any

# Unique marker injected into generated HTML. Must NOT appear in the short seed
# PRODINFO_TEMPLATE (which lists "Problem Statement" under Report Contents).
ENRICHED_MARKER = "hmp-full-project-details:v1"
ENRICHED_COMMENT = f"<!-- {ENRICHED_MARKER} -->"

# Field order and headings match product id=33 (iBin) prodinfo schema.
SECTION_ORDER = (
    "Tech",
    "Abstract",
    "Keywords",
    "Project Description",
    "Project Features",
    "Specifications",
    "Report Contents",
    "Applications",
    "Advantages",
    "Limitations",
    "Future Scope",
    "Conclusion",
)

# Fixed report-contents list (same spirit as product 33).
DEFAULT_REPORT_CONTENTS = [
    "Components List (BOM: Bill of Material)",
    "Block Diagram",
    "Flow Chart",
    "Components: Name, Images, Details",
    "Circuit Diagram",
    "Problem Statement",
    "Abstract",
    "Introduction",
    "Methodology",
    "Challenges and Solutions",
    "Performance Analysis",
    "Advantages",
    "Limitation",
    "Application",
    "Future Scope",
    "Conclusion",
    "Output Images",
    "Project Deliverables",
    "Project Hardware",
    "Project Report",
    "Project Simulation",
]

REQUIRED_STRING_KEYS = (
    "tech",
    "abstract",
    "project_description",
    "conclusion",
)

REQUIRED_LIST_KEYS = (
    "keywords",
    "project_features",
    "applications",
    "advantages",
    "limitations",
    "future_scope",
)


def is_enriched(prodinfo: str | None) -> bool:
    """True if prodinfo was produced by this Task 8 generator (or equivalent)."""
    if not prodinfo:
        return False
    text = prodinfo.strip()
    if not text or text == "*":
        return False
    if ENRICHED_MARKER in text:
        return True
    # Product-33-style full pages (without our comment) — several exclusive headings.
    exclusive = (
        "Project Features",
        "Specifications",
        "Future Scope",
        "Project Description",
    )
    hits = sum(1 for s in exclusive if s in text)
    return hits >= 3


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))


def _strip_code_fences(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json|JSON)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_json_object(raw: str) -> dict[str, Any]:
    """
    Parse model output into a dict. Handles markdown fences and leading/trailing prose
    by taking the outermost {...} slice when pure json.loads fails.
    """
    text = _strip_code_fences(raw)
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
        raise ValueError("JSON root must be an object")
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        data = json.loads(text[start : end + 1])
        if not isinstance(data, dict):
            raise ValueError("JSON root must be an object")
        return data


def _as_list(val: Any) -> list[str]:
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str):
        # Prefer line splits; fall back to commas for keyword-style strings.
        lines = [line.strip(" -•\t") for line in val.splitlines() if line.strip()]
        if len(lines) > 1:
            return lines
        return [p.strip() for p in re.split(r"[,;]+", val) if p.strip()]
    return [str(val).strip()] if str(val).strip() else []


def normalize_details(data: dict[str, Any], *, product_name: str = "") -> dict[str, Any]:
    """
    Coerce model JSON into the product-33 field schema.

    Accepts a few aliases so older / verbose model output still maps cleanly.
    """
    # Alias map: preferred key ← possible model keys
    aliases = {
        "tech": ("tech", "technologies", "technology"),
        "abstract": ("abstract",),
        "keywords": ("keywords", "tags"),
        "project_description": (
            "project_description",
            "description",
            "introduction",
            "objectives",
        ),
        "project_features": ("project_features", "features"),
        "hardware_components": ("hardware_components", "hardware"),
        "software_components": ("software_components", "software"),
        "applications": ("applications",),
        "advantages": ("advantages",),
        "limitations": ("limitations",),
        "future_scope": ("future_scope", "future"),
        "conclusion": ("conclusion",),
        "highlighttitle": ("highlighttitle", "highlight", "tagline"),
    }

    def pick(key: str, default: Any = "") -> Any:
        for name in aliases.get(key, (key,)):
            if name in data and data[name] not in (None, ""):
                return data[name]
        return default

    out: dict[str, Any] = {
        "product_name": str(data.get("product_name") or product_name or "").strip(),
    }

    tech = pick("tech", "")
    if isinstance(tech, list):
        tech = ", ".join(str(x).strip() for x in tech if str(x).strip())
    out["tech"] = str(tech).strip()

    out["abstract"] = str(pick("abstract", "") or "").strip()
    out["project_description"] = str(pick("project_description", "") or "").strip()
    out["conclusion"] = str(pick("conclusion", "") or "").strip()
    out["highlighttitle"] = str(pick("highlighttitle", "") or "").strip()

    out["keywords"] = _as_list(pick("keywords", []))
    out["applications"] = _as_list(pick("applications", []))
    out["advantages"] = _as_list(pick("advantages", []))
    out["limitations"] = _as_list(pick("limitations", []))
    out["future_scope"] = _as_list(pick("future_scope", []))

    # Features: list of strings OR list of {title, description}
    features_raw = pick("project_features", [])
    features: list[str] = []
    if isinstance(features_raw, str):
        features = _as_list(features_raw)
    elif isinstance(features_raw, list):
        for item in features_raw:
            if isinstance(item, dict):
                title = str(item.get("title") or item.get("name") or "").strip()
                desc = str(item.get("description") or item.get("detail") or "").strip()
                if title and desc:
                    features.append(f"{title}: {desc}" if len(desc) < 200 else title)
                elif title:
                    features.append(title)
                elif desc:
                    features.append(desc)
            elif str(item).strip():
                features.append(str(item).strip())
    out["project_features"] = features

    hw = pick("hardware_components", "")
    sw = pick("software_components", "")
    if isinstance(hw, list):
        hw = ", ".join(str(x).strip() for x in hw if str(x).strip())
    if isinstance(sw, list):
        sw = ", ".join(str(x).strip() for x in sw if str(x).strip())
    out["hardware_components"] = str(hw or "").strip()
    out["software_components"] = str(sw or "").strip()

    return out


def validate_details(data: dict[str, Any]) -> list[str]:
    """Return human-readable warnings (non-fatal) about missing / thin sections."""
    warnings: list[str] = []
    for key in REQUIRED_STRING_KEYS:
        if not data.get(key):
            warnings.append(f"missing string section: {key}")
        elif key in ("abstract", "project_description", "conclusion") and word_count(
            data[key]
        ) < 30:
            warnings.append(f"thin section ({word_count(data[key])} words): {key}")
    if not data.get("tech"):
        warnings.append("missing tech")
    if len(data.get("keywords") or []) < 8:
        warnings.append(f"few keywords: {len(data.get('keywords') or [])}")
    if len(data.get("project_features") or []) < 5:
        warnings.append("few project_features")
    if len(data.get("advantages") or []) < 4:
        warnings.append("few advantages")
    if len(data.get("limitations") or []) < 3:
        warnings.append("few limitations")
    if len(data.get("applications") or []) < 4:
        warnings.append("few applications")
    if len(data.get("future_scope") or []) < 3:
        warnings.append("few future_scope")
    if not data.get("hardware_components"):
        warnings.append("missing hardware_components")
    if not data.get("software_components"):
        warnings.append("missing software_components")
    return warnings


def _h2(title: str, *, first: bool = False) -> str:
    # Match product 33 classes closely (plus dark-mode helpers).
    mt = "" if first else " mt-6"
    return (
        f'<h2 class="text-lg font-bold border-b border-gray-300 '
        f'dark:border-slate-600 pb-1{mt}">{escape(title)}</h2>'
    )


def _esc(text: str) -> str:
    # Escape HTML specials but keep apostrophes readable (matches product 33 prose).
    return escape(text, quote=False)


def _p(text: str) -> str:
    return f'<p class="mt-2">{_esc(text)}</p>'


def _ul(items: list[str]) -> str:
    if not items:
        return '<p class="mt-2 text-gray-500 dark:text-slate-400">—</p>'
    lis = "\n".join(f"    <li>{_esc(item)}</li>" for item in items)
    return f'<ul class="list-disc pl-6 mt-2 space-y-1">\n{lis}\n  </ul>'


def _spec_li(label: str, value: str) -> str:
    return (
        f'    <li><span class="font-bold">{_esc(label)}:</span> '
        f"{_esc(value)}</li>"
    )


def structure_to_html(data: dict[str, Any], *, product_name: str = "") -> str:
    """
    Render normalized details using the product-33 field schema and HTML layout:

      Tech → Abstract → Keywords → Project Description → Project Features →
      Specifications → Report Contents → Applications → Advantages →
      Limitations → Future Scope → Conclusion
    """
    d = normalize_details(data, product_name=product_name)
    keywords_text = ", ".join(d["keywords"]) if d["keywords"] else "—"

    specs_items: list[str] = []
    if d.get("hardware_components"):
        specs_items.append(
            _spec_li("Hardware components", d["hardware_components"])
        )
    if d.get("software_components"):
        specs_items.append(
            _spec_li("Software components", d["software_components"])
        )
    if specs_items:
        specs_html = (
            '<ul class="list-disc pl-6 mt-2 space-y-1">\n'
            + "\n".join(specs_items)
            + "\n  </ul>"
        )
    else:
        specs_html = '<p class="mt-2 text-gray-500 dark:text-slate-400">—</p>'

    parts = [
        ENRICHED_COMMENT,
        '<div class="py-8 text-gray-800 dark:text-slate-100 font-sans bg-white dark:bg-transparent">',
        "",
        _h2("Tech", first=True),
        _p(d["tech"] or "—"),
        "",
        _h2("Abstract"),
        _p(d["abstract"] or "—"),
        "",
        _h2("Keywords"),
        _p(keywords_text),
        "",
        _h2("Project Description"),
        _p(d["project_description"] or "—"),
        "",
        _h2("Project Features"),
        _ul(d["project_features"]),
        "",
        _h2("Specifications"),
        specs_html,
        "",
        _h2("Report Contents"),
        _ul(DEFAULT_REPORT_CONTENTS),
        "",
        _h2("Applications"),
        _ul(d["applications"]),
        "",
        _h2("Advantages"),
        _ul(d["advantages"]),
        "",
        _h2("Limitations"),
        _ul(d["limitations"]),
        "",
        _h2("Future Scope"),
        _ul(d["future_scope"]),
        "",
        _h2("Conclusion"),
        _p(d["conclusion"] or "—"),
        "",
        "</div>",
    ]
    return "\n".join(parts) + "\n"


def keywords_to_prodtags(keywords: list[str], *, max_tags: int = 32) -> str:
    cleaned = [k.strip() for k in keywords if k and k.strip()]
    return ", ".join(cleaned[:max_tags])


def abstract_to_highlight(abstract: str, fallback: str = "") -> str:
    """Prefer explicit highlight; else first sentence of abstract."""
    if fallback and fallback.strip() and fallback.strip() != "*":
        return fallback.strip()[:500]
    text = (abstract or "").strip()
    if not text:
        return "*"
    first = text.split(". ")[0].strip()
    if not first.endswith("."):
        first += "."
    return first[:500]
