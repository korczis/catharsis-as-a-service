#!/usr/bin/env python3
"""Translation parity: content documents, front matter shape, UI dictionaries and template keys.

Strict by default. A document opts out only with `draft = true` or
`[extra] translation_required = false` in its default-language front matter.
Exits non-zero on any gap.
"""

import os
import re
import sys
import tomllib
from pathlib import Path

# CAAS_ROOT lets the test suite run the validator against a fixture repository.
ROOT = Path(os.environ.get("CAAS_ROOT", Path(__file__).resolve().parent.parent)).resolve()
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+", re.S)
TRANS_KEY = re.compile(r"""trans\(\s*key\s*=\s*["']([A-Za-z0-9_]+)["']""")


DYNAMIC_PREFIXES = ("kind_", "status_", "design_", "change_")

def load_config():
    with open(ROOT / "zola.toml", "rb") as handle:
        return tomllib.load(handle)


def front_matter(path):
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"missing TOML front matter: {path.relative_to(ROOT)}")
    return tomllib.loads(match.group(1))


def source_and_locale(path, locales, default):
    parts = path.name.split(".")
    if len(parts) == 3 and parts[1] in locales:
        return path.with_name(f"{parts[0]}.md"), parts[1]
    return path, default


def shape(value):
    """Structure without content: keys, list lengths and scalar types must match across locales."""
    if isinstance(value, dict):
        return {key: shape(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        return [shape(item) for item in value]
    return type(value).__name__


def main():
    config = load_config()
    default = config.get("default_language", "en")
    languages = config.get("languages", {})
    locales = [default] + sorted(code for code in languages if code != default)
    errors, warnings = [], []

    groups = {}
    for path in sorted(CONTENT.rglob("*.md")):
        source, locale = source_and_locale(path, locales, default)
        groups.setdefault(source, {})[locale] = path

    required = {code: 0 for code in locales}
    present = {code: 0 for code in locales}
    missing = orphaned = 0

    for source, files in sorted(groups.items()):
        rel = source.relative_to(ROOT)
        if default not in files:
            orphaned += 1
            errors.append(f"orphaned translation without a {default} source: {rel}")
            continue
        meta = front_matter(files[default])
        if meta.get("draft") or meta.get("extra", {}).get("translation_required") is False:
            continue
        reference = shape(meta.get("extra", {}))
        for code in locales:
            required[code] += 1
            if code not in files:
                missing += 1
                errors.append(f"missing {code} translation for {rel}")
                continue
            present[code] += 1
            if code == default:
                continue
            other = front_matter(files[code])
            other_rel = files[code].relative_to(ROOT)
            for field in ("title", "description"):
                if bool(meta.get(field)) != bool(other.get(field)):
                    errors.append(f"{other_rel}: '{field}' presence differs from {default}")
            if shape(other.get("extra", {})) != reference:
                errors.append(f"{other_rel}: [extra] structure differs from {default}")

    dictionaries = {default: config.get("translations", {})}
    for code in locales[1:]:
        dictionaries[code] = languages.get(code, {}).get("translations", {})
    all_keys = set().union(*(set(d) for d in dictionaries.values()))
    for code, dictionary in dictionaries.items():
        for key in sorted(all_keys - set(dictionary)):
            errors.append(f"UI string '{key}' missing for {code}")
        for key, value in sorted(dictionary.items()):
            if not str(value).strip():
                errors.append(f"UI string '{key}' is empty for {code}")

    used = {item["key"] for item in config.get("extra", {}).get("nav", [])}
    # Keys built from data values in templates (e.g. "kind_" ~ claim.claim_type) count as used.
    used.update(key for key in all_keys if key.startswith(DYNAMIC_PREFIXES))
    for template in TEMPLATES.rglob("*.html"):
        used.update(TRANS_KEY.findall(template.read_text(encoding="utf-8")))
    for key in sorted(used - all_keys):
        errors.append(f"template uses undefined UI string '{key}'")
    for key in sorted(all_keys - used):
        warnings.append(f"UI string '{key}' is defined but never used")

    print("I18N COVERAGE")
    print("────────────────────")
    for code in locales:
        pct = 100 if required[code] == 0 else round(100 * present[code] / required[code])
        print(f"{code:<6} {pct:>3}%   {present[code]}/{required[code]} documents")
    print(f"ui     {len(all_keys)} keys × {len(locales)} locales")
    print()
    print(f"missing: {missing}")
    print(f"orphaned: {orphaned}")
    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
