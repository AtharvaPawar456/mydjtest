"""One-shot: add missing dark: variants to template class attributes."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent / "mainapp" / "templates"

REPLACEMENTS = [
    ("text-slate-900", "dark:text-white"),
    ("text-slate-800", "dark:text-slate-100"),
    ("text-slate-700", "dark:text-slate-200"),
    ("text-slate-600", "dark:text-slate-300"),
    ("text-slate-500", "dark:text-slate-400"),
    ("text-slate-400", "dark:text-slate-500"),
    ("text-gray-900", "dark:text-white"),
    ("text-gray-800", "dark:text-slate-100"),
    ("text-gray-700", "dark:text-slate-200"),
    ("text-gray-600", "dark:text-slate-300"),
    ("text-gray-500", "dark:text-slate-400"),
    ("text-gray-400", "dark:text-slate-500"),
    ("bg-white", "dark:bg-slate-900"),
    ("bg-slate-50", "dark:bg-slate-900/60"),
    ("bg-slate-100", "dark:bg-slate-800"),
    ("bg-gray-50", "dark:bg-slate-900/60"),
    ("bg-gray-100", "dark:bg-slate-800"),
    ("border-slate-200", "dark:border-slate-700"),
    ("border-slate-100", "dark:border-slate-800"),
    ("border-slate-300", "dark:border-slate-600"),
    ("border-gray-200", "dark:border-slate-700"),
    ("border-gray-300", "dark:border-slate-600"),
    ("border-gray-100", "dark:border-slate-800"),
    ("bg-brand-50", "dark:bg-brand-900/40"),
    ("bg-emerald-50", "dark:bg-emerald-900/30"),
    ("bg-amber-50", "dark:bg-amber-900/30"),
    ("bg-orange-50", "dark:bg-orange-900/30"),
    ("bg-violet-50", "dark:bg-violet-900/30"),
    ("bg-pink-50", "dark:bg-pink-900/30"),
    ("bg-blue-50", "dark:bg-blue-900/30"),
    ("bg-sky-50", "dark:bg-sky-900/30"),
    ("bg-red-50", "dark:bg-red-900/30"),
    ("text-brand-700", "dark:text-brand-300"),
    ("text-brand-600", "dark:text-brand-400"),
    ("text-emerald-700", "dark:text-emerald-300"),
    ("text-emerald-800", "dark:text-emerald-300"),
    ("text-amber-700", "dark:text-amber-300"),
    ("text-amber-800", "dark:text-amber-300"),
    ("text-amber-900", "dark:text-amber-200"),
    ("text-orange-600", "dark:text-orange-300"),
    ("text-orange-700", "dark:text-orange-300"),
    ("text-violet-700", "dark:text-violet-300"),
    ("text-pink-600", "dark:text-pink-300"),
    ("text-blue-600", "dark:text-blue-300"),
    ("text-blue-700", "dark:text-blue-300"),
    ("text-indigo-600", "dark:text-indigo-300"),
    ("text-indigo-700", "dark:text-indigo-300"),
    ("text-red-700", "dark:text-red-300"),
    ("text-red-800", "dark:text-red-300"),
    ("border-brand-100", "dark:border-brand-800"),
    ("border-brand-200", "dark:border-brand-700"),
    ("border-emerald-200", "dark:border-emerald-800"),
    ("border-red-200", "dark:border-red-800"),
    ("hover:bg-slate-100", "dark:hover:bg-slate-800"),
    ("hover:bg-slate-200", "dark:hover:bg-slate-700"),
    ("hover:bg-brand-50", "dark:hover:bg-brand-900/40"),
    ("hover:text-brand-700", "dark:hover:text-brand-300"),
    ("hover:border-brand-300", "dark:hover:border-brand-500"),
    ("divide-slate-200", "dark:divide-slate-700"),
    ("ring-slate-200", "dark:ring-slate-700"),
    ("placeholder-gray-500", "dark:placeholder-slate-400"),
    ("placeholder-slate-400", "dark:placeholder-slate-500"),
]

SKIP_NAMES = {"500.html", "404.html"}

CLASS_ATTR_RE = re.compile(
    r"""(?:class\s*=\s*)(?P<q>["'])(?P<body>.*?)(?P=q)""",
    re.DOTALL | re.IGNORECASE,
)


def token_present(classes: str, token: str) -> bool:
    return re.search(rf"(?<![\w:-]){re.escape(token)}(?![\w-])", classes) is not None


def patch_class_string(classes: str) -> str:
    keep_white_btn = (
        token_present(classes, "bg-white")
        and (
            token_present(classes, "text-brand-700")
            or token_present(classes, "text-brand-600")
        )
        and token_present(classes, "rounded-full")
        and not token_present(classes, "border")
    )

    for light, dark in REPLACEMENTS:
        if not token_present(classes, light):
            continue
        if token_present(classes, dark):
            continue
        if light == "bg-white" and keep_white_btn:
            if not token_present(classes, "dark:bg-white"):
                classes = re.sub(
                    rf"(?<![\w:-]){re.escape(light)}(?![\w-])",
                    f"{light} dark:bg-white",
                    classes,
                    count=1,
                )
            continue
        classes = re.sub(
            rf"(?<![\w:-]){re.escape(light)}(?![\w-])",
            f"{light} {dark}",
            classes,
            count=1,
        )
    return classes


def main():
    changed_files = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name in SKIP_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        new_parts = []
        last = 0
        file_changed = False
        for m in CLASS_ATTR_RE.finditer(text):
            body = m.group("body")
            patched = patch_class_string(body)
            if patched != body:
                file_changed = True
            new_parts.append(text[last : m.start("body")])
            new_parts.append(patched)
            last = m.end("body")
        if not file_changed:
            continue
        new_parts.append(text[last:])
        path.write_text("".join(new_parts), encoding="utf-8")
        changed_files.append(str(path.relative_to(ROOT.parent.parent)))

    print(f"Updated {len(changed_files)} files")
    for f in changed_files:
        print(" -", f)


if __name__ == "__main__":
    main()
