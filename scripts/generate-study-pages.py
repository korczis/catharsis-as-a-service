#!/usr/bin/env python3
"""A page per cited study, generated from the evidence data.

Every entry in data/references.toml gets one page per locale under content/studies/, carrying the
citation, the appraisal from data/sources.toml, the claims in data/claims.toml that rest on it and the
pages that cite it. The pages hold no prose of their own: they are a projection of the ledger, so a
study page can never drift from the data it is made of.

The output is generated, not authored: it is ignored by Git and written before every Zola build
(npm run build, scripts/dev.sh, scripts/preview.sh, scripts/validate.sh).

usage: generate-study-pages.py [--root <repo>] [--check]
"""

import argparse
import re
import shutil
import sys
import tomllib
from pathlib import Path

FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.S)
LANGS = ("en", "cs")
# Inside scripts/validate-content.py's DESCRIPTION_LENGTH, and short enough that a search result
# shows the whole of it rather than a truncated half-sentence.
DESCRIPTION = (50, 170)

SECTION = {
    "en": {
        "title": "Studies",
        "description": "Every study, book and classical text this site cites, each with its design, its appraised level of evidence, the claims that rest on it and the pages that cite it.",
        "kicker": "Evidence",
        "intro": "One page per cited work. The citation comes from the reference registry, the appraisal from the source ledger, and the claims and pages are the ones that actually rest on it. Nothing here is written by hand: if the ledger changes, these pages change with it.",
    },
    "cs": {
        "title": "Studie",
        "description": "Každá studie, kniha a klasický text, které web cituje, s designem, posouzenou úrovní důkazů, tvrzeními, jež se o ně opírají, a stránkami, které je citují.",
        "kicker": "Důkazy",
        "intro": "Jedna stránka na každou citovanou práci. Citace pochází z registru referencí, posouzení z evidenční knihy zdrojů a tvrzení i stránky jsou ty, které se o práci skutečně opírají. Nic zde není psáno ručně: když se evidence změní, změní se s ní i tyto stránky.",
    },
}


def quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def localized(value, lang):
    """sources.toml and claims.toml hold {en = ..., cs = ...} tables; references.toml uses _cs suffixes."""
    if isinstance(value, dict):
        return value.get(lang, value.get("en", ""))
    return value


def citation(ref, lang):
    title = ref.get(f"title_{lang}") or ref["title"]
    year = ref.get(f"year_{lang}") or ref["year"]
    return f"{ref['authors']} ({year}). {title}."


def describe(ref, source, lang):
    """A description that fits a search result: the citation, then as much of the appraisal as fits."""
    low, high = DESCRIPTION
    head = citation(ref, lang)
    appraisal = localized(source.get("appraisal", {}), lang)
    text = f"{head} {appraisal}".strip()
    if len(text) <= high:
        if len(text) >= low:
            return text
        return (text + " " + localized(source.get("population", {}), lang)).strip()[:high]
    cut = text[: high - 1]
    stop = cut.rfind(". ")
    if stop > low:
        return cut[: stop + 1]
    return cut[: cut.rfind(" ")].rstrip(",;:") + "…"


def content_pages(root):
    """Front matter of every authored page, so a study can list what cites it."""
    pages = {}
    for path in sorted((root / "content").rglob("*.md")):
        rel = path.relative_to(root / "content")
        if rel.parts[0] == "studies":
            continue
        match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
        if not match:
            continue
        try:
            meta = tomllib.loads(match.group(1))
        except tomllib.TOMLDecodeError:
            continue
        pages[str(rel)] = meta
    return pages


def citing_pages(root, pages):
    """Map reference id -> the language-neutral content paths that cite it.

    Front matter is not the only place a work is cited: a glossary term cites its sources in
    data/glossary.toml, and each term has a page of its own (scripts/generate-term-pages.py). Those pages
    are generated after this one, so they are derived from the glossary rather than read from disk.
    """
    citing = {}
    for rel, meta in pages.items():
        if ".cs.md" in rel:
            continue
        for ident in meta.get("extra", {}).get("references", []) or []:
            citing.setdefault(ident, []).append(rel)
    glossary = root / "data" / "glossary.toml"
    if glossary.exists():
        for term in tomllib.loads(glossary.read_text(encoding="utf-8"))["terms"]:
            for ident in term.get("references", []) or []:
                citing.setdefault(ident, []).append(f"terms/{term['id']}/index.md")
    return {ident: sorted(set(paths)) for ident, paths in citing.items()}


def page(ref, source, claims, cited_by, ident, lang):
    lines = [
        "+++",
        f"title = {quote(ref.get(f'title_{lang}') or ref['title'])}",
        f"description = {quote(describe(ref, source, lang))}",
        'template = "study.html"',
        f"slug = {quote(ident)}",
        "",
        "[extra]",
        f"reference = {quote(ident)}",
        f"citation = {quote(citation(ref, lang))}",
        f"level = {quote(source['level'])}",
        f"design = {quote(source['design'])}",
        f"kind = {quote(ref['kind'])}",
        f"claims = [{', '.join(quote(c) for c in claims)}]",
        f"cited_by = [{', '.join(quote(p) for p in cited_by)}]",
        "+++",
        "",
    ]
    return "\n".join(lines)


def section(lang, counts):
    """The section groups its pages by level; the counts are computed here because the templating
    language has no filter that can count a subset of pages."""
    text = SECTION[lang]
    levels = [level for level in ("A", "B", "C", "D", "E") if counts.get(level)]
    return "\n".join([
        "+++",
        f"title = {quote(text['title'])}",
        f"description = {quote(text['description'])}",
        'template = "studies.html"',
        'sort_by = "title"',
        "",
        "[extra]",
        f"kicker = {quote(text['kicker'])}",
        f"intro = {quote(text['intro'])}",
        f"levels = [{', '.join(quote(level) for level in levels)}]",
        "counts = { " + ", ".join(f"{level} = {counts[level]}" for level in levels) + " }",
        f"total = {sum(counts.values())}",
        "+++",
        "",
    ])


def render(root):
    """Return {relative path: file contents} for the whole generated section."""
    data = {
        name: tomllib.loads((root / "data" / f"{name}.toml").read_text(encoding="utf-8"))
        for name in ("references", "sources", "claims")
    }
    references = data["references"]["references"]
    sources = data["sources"]["sources"]
    claims = data["claims"]["claims"]
    pages = content_pages(root)
    citing = citing_pages(root, pages)

    by_reference = {}
    for claim in claims:
        for ident in claim.get("sources", []):
            by_reference.setdefault(ident, []).append(claim["id"])

    counts = {}
    for ident in references:
        level = sources[ident]["level"] if ident in sources else "E"
        counts[level] = counts.get(level, 0) + 1

    files = {}
    for lang in LANGS:
        suffix = "index.md" if lang == "en" else "index.cs.md"
        files["_index.md" if lang == "en" else "_index.cs.md"] = section(lang, counts)
        for ident, ref in references.items():
            source = sources.get(ident)
            if source is None:
                raise SystemExit(f"generate-study-pages: {ident} has no appraisal in data/sources.toml")
            files[f"{ident}/{suffix}"] = page(
                ref, source, by_reference.get(ident, []), citing.get(ident, []), ident, lang
            )
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--check", action="store_true", help="report what would change and write nothing")
    args = parser.parse_args()
    root = args.root.resolve()
    out = root / "content" / "studies"

    files = render(root)
    if args.check:
        current = {
            str(p.relative_to(out)): p.read_text(encoding="utf-8")
            for p in out.rglob("*.md")
        } if out.exists() else {}
        drift = sorted(set(files) ^ set(current)) + sorted(k for k in files.keys() & current.keys() if files[k] != current[k])
        print("STUDIES")
        print("────────────────────")
        print(f"pages ............. {len(files)}")
        print(f"out of date ....... {len(drift)}")
        for name in drift[:10]:
            print(f"error: {name} is out of date; run scripts/generate-study-pages.py")
        print()
        print("FAIL" if drift else "PASS")
        return 1 if drift else 0

    if out.exists():
        shutil.rmtree(out)
    for name, text in files.items():
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    print("STUDIES")
    print("────────────────────")
    print(f"studies ........... {(len(files) - 2) // len(LANGS)}")
    print(f"pages written ..... {len(files)}")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
