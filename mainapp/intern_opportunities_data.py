"""Parse internship opportunities from ai-space/ai-suggestion/intern-ops.txt.

In the file, the marker after the ID controls public visibility:
  |  → visible (is_visible=True)
  -  → hide    (is_visible=False)

Example:
  1 | Django Web Intern | Software | ...
  2 - Frontend UI Intern (Tailwind) | Software | ...
"""
from __future__ import annotations

import re
from pathlib import Path

INTERN_OPS_PATH = (
    Path(__file__).resolve().parent.parent / "ai-space" / "ai-suggestion" / "intern-ops.txt"
)

# id, then | (visible) or - (hide), then rest of the pipe-separated fields
_LINE_RE = re.compile(r"^(\d+)\s*([|-])\s*(.+)$")


def is_stipend_label(text: str) -> bool:
    """True = stipend (paid), False = unstipend (unpaid)."""
    t = (text or "").strip().lower()
    if not t:
        return False
    if any(
        k in t
        for k in (
            "unpaid",
            "unstipend",
            "no stipend",
            "without stipend",
            "certificate only",
        )
    ):
        return False
    if any(
        k in t
        for k in (
            "stipend",
            "paid",
            "performance-based",
            "performance based",
            "₹",
            "rs.",
            "inr",
            "honorarium",
        )
    ):
        return True
    return False


def parse_opportunity_line(line: str) -> dict | None:
    """
    Parse one data line into a dict suitable for InternOpportunity.

    Returns None for comments, blanks, or malformed rows.
    """
    line = (line or "").strip()
    if not line or line.startswith("#"):
        return None
    m = _LINE_RE.match(line)
    if not m:
        return None
    try:
        oid = int(m.group(1))
    except ValueError:
        return None
    is_visible = m.group(2) == "|"
    parts = [p.strip() for p in m.group(3).split("|")]
    if len(parts) < 7:
        return None
    stipend_text = parts[4]
    return {
        "opid": oid,
        "title": parts[0],
        "track": parts[1],
        "mode": parts[2],
        "duration": parts[3],
        "stipend": stipend_text,
        "is_stipend": is_stipend_label(stipend_text),
        "skills": parts[5],
        "description": parts[6],
        "is_visible": is_visible,
    }


def parse_opportunities_file(path: Path | None = None) -> list[dict]:
    """Load and parse all opportunity rows from intern-ops.txt."""
    path = path or INTERN_OPS_PATH
    if not path.exists():
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        row = parse_opportunity_line(line)
        if row:
            items.append(row)
    return items


def load_opportunities(visible_only: bool = True) -> list[dict]:
    """
    Load opportunities as dicts (legacy helper).

    Prefer InternOpportunity.objects in views; this remains for seed/tests
    and as a file-based fallback when the table is empty.
    """
    items = parse_opportunities_file()
    if visible_only:
        items = [o for o in items if o.get("is_visible", True)]
    # Map opid → id for templates that expect op.id
    for o in items:
        o["id"] = o["opid"]
    return items
