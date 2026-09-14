#!/usr/bin/env python3
"""A page per glossary term, generated from data/glossary.toml.

The glossary lists every term on one page; this gives each of them an address of its own, with the
definition, the pages that use the term, the studies behind it and the terms it is related to. Like the
studies section it is a projection of the data, not a document: it is written before every Zola build and
never committed.

usage: generate-term-pages.py [--root <repo>] [--check]
"""

import argparse
import re
import shutil
import sys
import tomllib
from pathlib import Path

FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.S)
LANGS = ("en", "cs")
# Inside scripts/validate-content.py's range, and short enough to survive a search result intact.
DESCRIPTION = (50, 170)

# A term and a study can carry the same name ("Affective computing"), so the term page states its kind
# in the <title> while the heading stays the term itself.
META_TITLE = {"en": "{term} · glossary term", "cs": "{term} · pojem ze slovníku"}

SECTION = {
    "en": {
        "title": "Terms",
        "description": "Every term in the glossary as a page of its own: what it means, where the site uses it, the studies behind it and the terms next to it.",
        "kicker": "Reference",
    },
    "cs": {
        "title": "Pojmy",
        "description": "Každý pojem ze slovníku jako samostatná stránka: co znamená, kde jej web používá, o jaké studie se opírá a s jakými pojmy sousedí.",
        "kicker": "Reference",
    },
}


def quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def describe(term, lang):
    """The first sentences of the definition, kept inside the description length rule."""
    low, high = DESCRIPTION
    text = term["definition"][lang].strip()
    if len(text) <= high:
        return text
    cut = text[: high - 1]
    stop = cut.rfind(". ")
    if stop > low:
        return cut[: stop + 1]
    return cut[: cut.rfind(" ")].rstrip(",;:") + "…"


def page(term, lang, used_by):
    return "\n".join([
        "+++",
        f"title = {quote(term['term'][lang])}",
        f"description = {quote(describe(term, lang))}",
        'template = "term.html"',
        f"slug = {quote(term['id'])}",
        "",
        "[extra]",
        f"meta_title = {quote(META_TITLE[lang].format(term=term['term'][lang]))}",
        f"term = {quote(term['id'])}",
        f"kind = {quote(term['kind'])}",
        f"definition = {quote(term['definition'][lang])}",
        f"see_also = [{', '.join(quote(t) for t in term.get('see_also', []))}]",
        f"used_by = [{', '.join(quote(p) for p in used_by)}]",
        f"references = [{', '.join(quote(r) for r in term.get('references', []))}]",
        "+++",
        "",
    ])


def section(lang, total):
    text = SECTION[lang]
    return "\n".join([
        "+++",
        f"title = {quote(text['title'])}",
        f"description = {quote(text['description'])}",
        'render = false',
        'sort_by = "title"',
        "",
        "[extra]",
        f"kicker = {quote(text['kicker'])}",
        f"total = {total}",
        "+++",
        "",
    ])


def existing_pages(root):
    """Content paths that exist, so a term never links to a page that was renamed away."""
    return {
        path.relative_to(root / "content").as_posix()
        for path in (root / "content").rglob("*.md")
        if path.relative_to(root / "content").parts[0] not in ("terms", "studies")
    }


def render(root):
    glossary = tomllib.loads((root / "data" / "glossary.toml").read_text(encoding="utf-8"))["terms"]
    known = existing_pages(root)
    files = {}
    for lang in LANGS:
        suffix = "index.md" if lang == "en" else "index.cs.md"
        files["_index.md" if lang == "en" else "_index.cs.md"] = section(lang, len(glossary))
        for term in glossary:
            used_by = [link for link in term.get("links", []) if link in known]
            files[f"{term['id']}/{suffix}"] = page(term, lang, used_by)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--check", action="store_true", help="report what would change and write nothing")
    args = parser.parse_args()
    root = args.root.resolve()
    out = root / "content" / "terms"

    files = render(root)
    if args.check:
        current = {
            str(p.relative_to(out)): p.read_text(encoding="utf-8") for p in out.rglob("*.md")
        } if out.exists() else {}
        drift = sorted(set(files) ^ set(current)) + sorted(
            k for k in files.keys() & current.keys() if files[k] != current[k]
        )
        print("TERMS")
        print("────────────────────")
        print(f"pages ............. {len(files)}")
        print(f"out of date ....... {len(drift)}")
        for name in drift[:10]:
            print(f"error: {name} is out of date; run scripts/generate-term-pages.py")
        print()
        print("FAIL" if drift else "PASS")
        return 1 if drift else 0

    if out.exists():
        shutil.rmtree(out)
    for name, text in files.items():
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    print("TERMS")
    print("────────────────────")
    print(f"terms ............. {(len(files) - 2) // len(LANGS)}")
    print(f"pages written ..... {len(files)}")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
