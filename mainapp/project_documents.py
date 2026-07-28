"""
Parse product.documents field into view/download-ready items.

Storage format (same spirit as gallery/ytlinks):
  - "*" or empty → no documents
  - semicolon-separated entries
  - each entry is either a bare URL or "Label|URL"

Supported types (by extension): ppt, pptx, pdf, doc, docx, xls, xlsx, odt, odp, csv, txt, zip, rar
"""
from __future__ import annotations

import os
from urllib.parse import quote, unquote, urlparse

# extension → (short type label, can embed in-browser reasonably)
DOC_TYPE_META = {
    "pdf": ("PDF", True),
    "ppt": ("PowerPoint", True),
    "pptx": ("PowerPoint", True),
    "doc": ("Word", True),
    "docx": ("Word", True),
    "xls": ("Excel", True),
    "xlsx": ("Excel", True),
    "odt": ("OpenDocument", True),
    "odp": ("OpenDocument", True),
    "csv": ("CSV", False),
    "txt": ("Text", True),
    "rtf": ("RTF", False),
    "zip": ("ZIP archive", False),
    "rar": ("RAR archive", False),
    "7z": ("7z archive", False),
}


def _extension_from_url(url: str) -> str:
    path = unquote(urlparse(url).path or "")
    _, ext = os.path.splitext(path)
    return ext.lstrip(".").lower()


def _filename_from_url(url: str) -> str:
    path = unquote(urlparse(url).path or "")
    name = os.path.basename(path.rstrip("/"))
    return name or "document"


def _view_url(url: str, ext: str) -> str | None:
    """
    Return a browser viewer URL for Office/PDF when possible.
    PDF opens natively; Office files use Microsoft Office Online viewer
    (works for publicly reachable https URLs such as raw.githubusercontent.com).
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return None
    if ext == "pdf" or ext == "txt":
        return url  # browser-native
    if ext in ("ppt", "pptx", "doc", "docx", "xls", "xlsx", "odt", "odp"):
        return f"https://view.officeapps.live.com/op/view.aspx?src={quote(url, safe='')}"
    return None


def parse_documents(raw: str | None) -> list[dict]:
    """
    Parse documents field → list of dicts:
      label, url, filename, ext, type_label, view_url (or None), download_url
    """
    if not raw:
        return []
    text = raw.strip()
    if not text or text == "*":
        return []

    items: list[dict] = []
    # Allow ; or newlines as separators
    chunks = []
    for part in text.replace("\r", "\n").split("\n"):
        for piece in part.split(";"):
            piece = piece.strip()
            if piece and piece != "*":
                chunks.append(piece)

    for i, chunk in enumerate(chunks, start=1):
        label = ""
        url = chunk
        if "|" in chunk and not chunk.lower().startswith("http"):
            # Label|URL  (label first)
            left, right = chunk.split("|", 1)
            if right.strip().startswith("http"):
                label = left.strip()
                url = right.strip()
        elif "|" in chunk:
            # URL|Label  (less common)
            left, right = chunk.split("|", 1)
            if left.strip().startswith("http"):
                url = left.strip()
                label = right.strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            continue

        ext = _extension_from_url(url)
        filename = _filename_from_url(url)
        type_label, _ = DOC_TYPE_META.get(ext, (ext.upper() or "File", False))
        if not label:
            # Prefer human filename without extension
            base = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").strip()
            label = base or f"Document {i}"

        items.append(
            {
                "label": label,
                "url": url,
                "filename": filename,
                "ext": ext,
                "type_label": type_label,
                "view_url": _view_url(url, ext),
                "download_url": url,
            }
        )
    return items
