#!/usr/bin/env python3
"""Per-page social preview images: one 1200×630 JPEG for every content page in every language.

Images are rendered from artwork/og.html with Google Chrome and converted with ImageMagick into
static/og/<content path>.jpg (content/research/x/index.cs.md → static/og/research/x/index.cs.jpg).
static/og/manifest.json records a hash of every input of each image (title, label, kicker, line,
language and the template itself). --check needs no browser: it fails when a page has no image,
when an image is stale, or when an image belongs to no page. CI runs --check; rendering is local.

usage: render-social.py [--check] [--force] [--jobs N] [--root <repo>]
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.parse
from pathlib import Path

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+", re.S)
SIZE = "1200,630"
JPEG_QUALITY = "84"
LABELS = {
    "en": {
        "": "Artwork and library", "research": "Research", "theory": "Theory", "advice": "Advice",
        "methods": "Methods", "models": "Interactive models", "evidence": "Evidence", "glossary": "Glossary",
        "status": "Status", "about": "About", "guides": "Guides", "commands": "Commands",
        "artifacts": "Artifacts", "search": "Search", "engineering": "Engineering", "case-study": "Case study",
    },
    "cs": {
        "": "Dílo a knihovna", "research": "Výzkum", "theory": "Teorie", "advice": "Rady",
        "methods": "Metody", "models": "Interaktivní modely", "evidence": "Důkazy", "glossary": "Slovník",
        "status": "Stav", "about": "O projektu", "guides": "Návody", "commands": "Příkazy",
        "artifacts": "Artefakty", "search": "Hledat", "engineering": "Technika", "case-study": "Případová studie",
    },
}
LINES = {"en": "relief detected ≠ cause resolved", "cs": "úleva zaznamenána ≠ příčina vyřešena"}


def language_of(path, default):
    parts = path.name.split(".")
    return parts[1] if len(parts) == 3 else default


def pages(root):
    config = tomllib.loads((root / "zola.toml").read_text(encoding="utf-8"))
    default = config["default_language"]
    template_hash = hashlib.sha256((root / "artwork" / "og.html").read_bytes()).hexdigest()
    for path in sorted((root / "content").rglob("*.md")):
        match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
        if not match:
            continue
        meta = tomllib.loads(match.group(1))
        rel = path.relative_to(root / "content")
        language = language_of(path, default)
        section = rel.parts[0] if len(rel.parts) > 1 else ""
        labels = LABELS.get(language, LABELS["en"])
        fields = {
            "title": meta.get("title", ""),
            "label": labels.get(section, labels[""]),
            "kicker": meta.get("extra", {}).get("kicker", ""),
            "line": LINES.get(language, LINES["en"]),
            "lang": language,
        }
        digest = hashlib.sha256(json.dumps({**fields, "template": template_hash}, sort_keys=True).encode()).hexdigest()
        yield rel.as_posix(), rel.with_suffix(".jpg").as_posix(), fields, digest


def render(root, output, fields):
    target = root / "static" / "og" / output
    target.parent.mkdir(parents=True, exist_ok=True)
    source = (root / "artwork" / "og.html").as_uri() + "?" + urllib.parse.urlencode(fields)
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "og.png"
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={SIZE}",
             "--force-device-scale-factor=1", "--virtual-time-budget=6000", f"--screenshot={png}", source],
            check=True, capture_output=True, timeout=120,
        )
        subprocess.run(
            ["magick", str(png), "-strip", "-interlace", "Plane", "-sampling-factor", "4:2:0",
             "-quality", JPEG_QUALITY, str(target)],
            check=True, capture_output=True, timeout=60,
        )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verify images and manifest without rendering")
    parser.add_argument("--force", action="store_true", help="re-render every image")
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / "static" / "og" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    expected = list(pages(root))
    wanted = {output for _, output, _, _ in expected}
    errors = []
    stale = []
    for rel, output, fields, digest in expected:
        missing = not (root / "static" / "og" / output).exists()
        if args.force or missing or manifest.get(output) != digest:
            stale.append((rel, output, fields, digest, "missing" if missing else "stale"))
    orphans = sorted(set(manifest) - wanted)
    orphans += sorted(
        p.relative_to(root / "static" / "og").as_posix()
        for p in (root / "static" / "og").rglob("*.jpg")
        if p.relative_to(root / "static" / "og").as_posix() not in wanted
    ) if (root / "static" / "og").exists() else []
    orphans = sorted(set(orphans))

    print("SOCIAL PREVIEWS")
    print("────────────────────")
    print(f"pages ............. {len(expected)}")

    if args.check:
        for rel, output, _, _, reason in stale:
            errors.append(f"content/{rel}: social preview static/og/{output} is {reason} (run scripts/render-social.py)")
        for output in orphans:
            errors.append(f"static/og/{output} belongs to no content page")
        print(f"up to date ........ {len(expected) - len(stale)}")
        for error in errors:
            print(f"error: {error}")
        print()
        print("FAIL" if errors else "PASS")
        return 1 if errors else 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(render, root, output, fields): (output, digest) for _, output, fields, digest, _ in stale}
        for future in concurrent.futures.as_completed(futures):
            output, digest = futures[future]
            try:
                future.result()
                manifest[output] = digest
                print(f"  rendered {output}")
            except (subprocess.SubprocessError, OSError) as error:
                errors.append(f"{output}: {error}")
    for output in orphans:
        manifest.pop(output, None)
        (root / "static" / "og" / output).unlink(missing_ok=True)
        print(f"  removed  {output}")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(dict(sorted(manifest.items())), indent=2) + "\n", encoding="utf-8")
    print(f"rendered .......... {len(stale) - len(errors)}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
