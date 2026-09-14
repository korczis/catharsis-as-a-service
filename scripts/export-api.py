#!/usr/bin/env python3
"""Export the content library as a versioned JSON API for other applications.

The contract is documented in docs/RUST-INTEGRATION.md and implemented on the Rust side by
crates/caas-content. Output is deterministic: no timestamps, stable ordering.

usage: export-api.py --out <dir> [--base-url <url>] [--root <repo>]
writes <dir>/api/v1/index.json, references.json, commands.json,
       research.<lang>.json and advice.<lang>.json for every configured language
"""

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

API_VERSION = 1
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+", re.S)


def front_matter(path):
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    return tomllib.loads(match.group(1)) if match else {}


def documents(root, section, language, default):
    suffix = "index.md" if language == default else f"index.{language}.md"
    items = []
    for path in sorted((root / "content" / section).glob(f"*/{suffix}")):
        meta = front_matter(path)
        items.append((meta.get("weight", 0), path.parent.name, meta))
    return sorted(items, key=lambda item: (item[0], item[1]))


def url(base, language, default, *parts):
    prefix = "" if language == default else f"{language}/"
    return f"{base}/{prefix}{'/'.join(parts)}/"


def export(root, out, base_url):
    config = tomllib.loads((root / "zola.toml").read_text(encoding="utf-8"))
    base = (base_url or config["base_url"]).rstrip("/")
    default = config["default_language"]
    languages = config["extra"]["locales"]
    api = out / "api" / "v1"
    api.mkdir(parents=True, exist_ok=True)

    collections = {"research": {}, "advice": {}}
    for language in languages:
        research = []
        for _, slug, meta in documents(root, "research", language, default):
            extra = meta.get("extra", {})
            research.append({
                "slug": slug,
                "url": url(base, language, default, "research", slug),
                "title": meta["title"],
                "description": meta["description"],
                "date": str(meta.get("date", "")),
                "kicker": extra["kicker"],
                "summary": extra["summary"],
                "key_points": extra["key_points"],
                "tags": meta.get("taxonomies", {}).get("tags", []),
                "references": extra["references"],
            })
        advice = []
        for _, slug, meta in documents(root, "advice", language, default):
            extra = meta.get("extra", {})
            advice.append({
                "slug": slug,
                "url": url(base, language, default, "advice", slug),
                "title": meta["title"],
                "description": meta["description"],
                "kicker": extra["kicker"],
                "evidence_grade": extra["evidence_grade"],
                "evidence_label": extra["evidence_label"],
                "recommendation": extra["recommendation"],
                "practice": extra["practice"],
                "limits": extra["limits"],
                "related": [Path(path).parent.name for path in extra["related"]],
                "tags": meta.get("taxonomies", {}).get("tags", []),
                "references": extra["references"],
            })
        for name, items in (("research", research), ("advice", advice)):
            filename = f"{name}.{language}.json"
            write(api / filename, items)
            collections[name][language] = filename

    references = tomllib.loads((root / "data" / "references.toml").read_text(encoding="utf-8"))["references"]
    write(api / "references.json", dict(sorted(references.items())))

    registry = tomllib.loads((root / "data" / "commands.toml").read_text(encoding="utf-8"))
    commands = [
        {key: entry[key] for key in ("id", "group", "command", "summary", "source", "verified_by")}
        for entry in registry["commands"]
    ]
    write(api / "commands.json", commands)

    index = {
        "api_version": API_VERSION,
        "site": base,
        "default_language": default,
        "languages": languages,
        "collections": collections,
        "references": "references.json",
        "commands": "commands.json",
        "endpoint": {"method": "POST", "path": "/v1/catharsis", "status": 200, "problem_solved": False},
    }
    write(api / "index.json", index)
    return api, index


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True, help="directory that receives api/v1/")
    parser.add_argument("--base-url", help="site base URL for absolute links (default: base_url in zola.toml)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    api, index = export(args.root.resolve(), args.out.resolve(), args.base_url)
    files = sorted(p.name for p in api.glob("*.json"))
    print(f"api v{index['api_version']}: {len(files)} files in {api}")
    for name in files:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
