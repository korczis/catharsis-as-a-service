#!/usr/bin/env python3
"""Reference registry checks.

Offline (default, part of scripts/validate.sh):
  - every entry in data/references.toml has the required fields with valid formats
  - every id cited by content front matter exists in the registry
  - every research note and advice entry cites at least one reference

Online (--online, CI job "References (Crossref)"):
  - every DOI resolves in Crossref, and the registered title and year match Crossref's record

usage: check-references.py [--online] [--root <repo>]
"""

import argparse
import difflib
import json
import re
import sys
import time
import tomllib
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

REQUIRED = ("kind", "authors", "year", "title", "container", "volume", "issue", "pages", "publisher", "doi", "url")
KINDS = {"journal-article", "systematic-review", "book", "classical", "software", "record"}
DOI = re.compile(r"^10\.\d{4,9}/\S+$")
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+", re.S)
CITING_SECTIONS = ("research", "advice")
TITLE_SIMILARITY = 0.9


def load_registry(root):
    with open(root / "data" / "references.toml", "rb") as handle:
        return tomllib.load(handle).get("references", {})


def cited_documents(root):
    for section in CITING_SECTIONS:
        for path in sorted((root / "content" / section).glob("*/index*.md")):
            match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
            meta = tomllib.loads(match.group(1)) if match else {}
            yield path, meta.get("extra", {}).get("references", [])


def normalise(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def check_offline(root):
    errors, warnings = [], []
    registry = load_registry(root)
    for ident, entry in registry.items():
        for field in REQUIRED:
            if field not in entry:
                errors.append(f"{ident}: missing field '{field}'")
        if entry.get("kind") not in KINDS:
            errors.append(f"{ident}: kind '{entry.get('kind')}' is not one of {sorted(KINDS)}")
        for field in ("authors", "year", "title"):
            if not str(entry.get(field, "")).strip():
                errors.append(f"{ident}: '{field}' is empty")
        doi = entry.get("doi", "")
        if doi and not DOI.match(doi):
            errors.append(f"{ident}: DOI '{doi}' is malformed")
        url = entry.get("url", "")
        if url and not url.startswith("https://"):
            errors.append(f"{ident}: url must use https")
        if entry.get("kind") in {"journal-article", "systematic-review"} and not doi:
            errors.append(f"{ident}: a {entry.get('kind')} needs a DOI")

    used = set()
    documents = 0
    for path, ids in cited_documents(root):
        documents += 1
        rel = path.relative_to(root)
        if not ids:
            errors.append(f"{rel}: cites no references")
        for ident in ids:
            used.add(ident)
            if ident not in registry:
                errors.append(f"{rel}: cites unknown reference '{ident}'")
    for ident in sorted(set(registry) - used):
        warnings.append(f"reference '{ident}' is registered but never cited")
    return registry, documents, errors, warnings


def crossref(doi, attempts=3):
    request = urllib.request.Request(
        f"https://api.crossref.org/works/{doi}",
        headers={"User-Agent": "catharsis-as-a-service reference check (https://github.com/korczis/catharsis-as-a-service)"},
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)["message"]
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            if attempt == attempts:
                raise
        except urllib.error.URLError:
            if attempt == attempts:
                raise
        time.sleep(2 * attempt)
    return None


def check_online(registry):
    errors = []
    checked = 0
    for ident, entry in sorted(registry.items()):
        doi = entry.get("doi", "")
        if not doi:
            continue
        checked += 1
        record = crossref(doi)
        if record is None:
            errors.append(f"{ident}: DOI {doi} is not known to Crossref")
            continue
        # Publishers deposit subtitles inconsistently: separately, inside the title, or not at all.
        # Compare the full registered title and its main title against Crossref's title with and
        # without the subtitle, and keep the best match.
        title = " ".join(record.get("title") or [""])
        subtitle = " ".join(record.get("subtitle") or [])
        remote_forms = {normalise(title), normalise(f"{title} {subtitle}")}
        registered_forms = {normalise(entry["title"]), normalise(entry["title"].split(":")[0])}
        similarity, remote = max(
            (difflib.SequenceMatcher(None, local, text).ratio(), text)
            for local in registered_forms
            for text in remote_forms
        )
        year = str((record.get("issued", {}).get("date-parts") or [[None]])[0][0])
        status = "ok"
        if similarity < TITLE_SIMILARITY:
            errors.append(f"{ident}: title differs from Crossref ({similarity:.2f}): {remote!r}")
            status = "title"
        if year != str(entry["year"]):
            errors.append(f"{ident}: year {entry['year']} differs from Crossref {year}")
            status = "year"
        print(f"  {status:<5} {ident:<32} {doi}")
        time.sleep(0.2)
    return checked, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--online", action="store_true", help="verify DOIs, titles and years against Crossref")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()

    registry, documents, errors, warnings = check_offline(root)
    print("REFERENCES")
    print("────────────────────")
    print(f"registered ........ {len(registry)}")
    print(f"citing documents .. {documents}")
    if args.online:
        checked, online_errors = check_online(registry)
        errors.extend(online_errors)
        print(f"crossref checked .. {checked}")
    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
