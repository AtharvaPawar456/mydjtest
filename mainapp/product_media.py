"""
Helpers for product gallery / components / carousel media fields.

Storage: semicolon- or newline-separated entries.
Each entry is a bare URL or "Label|URL".
"""
from __future__ import annotations

import os
import re
from urllib.parse import unquote, urlparse

VIDEO_EXTS = (".mp4", ".webm", ".mov", ".m4v")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg", ".avif")
BLOCK_DIAGRAM_HINTS = ("block", "diagram", "schematic", "circuit", "blockdiagram")


def _split_raw(raw: str | None) -> list[str]:
    if not raw:
        return []
    text = raw.strip()
    if not text or text == "*":
        return []
    chunks: list[str] = []
    for part in text.replace("\r", "\n").split("\n"):
        for piece in part.split(";"):
            piece = piece.strip()
            if piece and piece != "*":
                chunks.append(piece)
    return chunks


def _parse_entry(chunk: str) -> tuple[str, str]:
    """Return (label, url_or_src)."""
    label = ""
    src = chunk
    if "|" in chunk:
        left, right = chunk.split("|", 1)
        left, right = left.strip(), right.strip()
        if right.startswith("http") or right.startswith("data:"):
            label, src = left, right
        elif left.startswith("http") or left.startswith("data:"):
            src, label = left, right
    return label, src


def _is_video(src: str) -> bool:
    path = unquote(urlparse(src).path if src.startswith("http") else src).lower()
    return any(path.endswith(ext) for ext in VIDEO_EXTS)


def _is_image_src(src: str) -> bool:
    if src.startswith("data:image"):
        return True
    if _is_video(src):
        return False
    path = unquote(urlparse(src).path if "://" in src else src).lower()
    if any(path.endswith(ext) for ext in IMAGE_EXTS):
        return True
    # Remote URLs without clear extension still treated as images for gallery
    if src.startswith("http://") or src.startswith("https://"):
        return True
    # bare base64 blob (legacy)
    if not src.startswith("http") and len(src) > 40:
        return True
    return False


def _display_src(src: str) -> str:
    if src.startswith("http") or src.startswith("data:"):
        return src
    # legacy base64 without data: prefix
    return f"data:image/png;base64,{src}"


def _filename(src: str) -> str:
    if src.startswith("data:"):
        return "image.png"
    path = unquote(urlparse(src).path or "")
    name = os.path.basename(path.rstrip("/"))
    return name or "file"


def parse_media_list(raw: str | None) -> list[dict]:
    """
    Parse gallery/components field → list of media dicts:
      label, src, display_src, is_video, is_image, filename
    """
    items: list[dict] = []
    for i, chunk in enumerate(_split_raw(raw), start=1):
        label, src = _parse_entry(chunk)
        if not src:
            continue
        is_video = _is_video(src)
        is_image = (not is_video) and _is_image_src(src)
        filename = _filename(src)
        if not label:
            base = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").strip()
            label = base or f"Item {i}"
        items.append(
            {
                "label": label,
                "src": src,
                "display_src": _display_src(src) if not is_video else src,
                "is_video": is_video,
                "is_image": is_image or (not is_video),
                "filename": filename,
            }
        )
    return items


def build_carousel_images(mainimg: str | None, gallery_items: list[dict]) -> list[dict]:
    """Main thumbnail first, then unique gallery images (no videos)."""
    slides: list[dict] = []
    seen: set[str] = set()

    def add(src: str, label: str, filename: str = "") -> None:
        if not src or src == "*":
            return
        key = src.strip()
        if key in seen:
            return
        seen.add(key)
        slides.append(
            {
                "src": key,
                "display_src": _display_src(key),
                "label": label,
                "filename": filename or _filename(key),
                "is_video": False,
                "is_image": True,
            }
        )

    main = (mainimg or "").strip()
    if main and main != "*":
        add(main, "Project thumbnail", _filename(main))

    for item in gallery_items:
        if item.get("is_video"):
            continue
        add(item["src"], item.get("label") or "Gallery", item.get("filename") or "")

    return slides


def find_block_diagram_url(gallery_items: list[dict], mainimg: str | None = None) -> str | None:
    """
    Prefer gallery (or main) asset whose filename/label suggests a block diagram.
    Fallback: None (UI hides the button).
    """
    candidates = list(gallery_items)
    if mainimg and mainimg not in ("*", "", None):
        candidates = [
            {
                "src": mainimg,
                "label": "main",
                "filename": _filename(mainimg),
                "is_video": False,
            }
        ] + candidates

    for item in candidates:
        if item.get("is_video"):
            continue
        hay = f"{item.get('label', '')} {item.get('filename', '')} {item.get('src', '')}".lower()
        if any(h in hay for h in BLOCK_DIAGRAM_HINTS):
            return item.get("display_src") or _display_src(item["src"])
    return None
