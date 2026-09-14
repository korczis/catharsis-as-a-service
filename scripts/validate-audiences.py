#!/usr/bin/env python3
"""Audience and lens checks.

  data/audiences.toml   the lenses, the audiences that map onto them, and the epistemic
                        vocabulary every model and figure classifies its parts with

Fails on unknown vocabulary, a missing translation, a dangling id or path, a lens no audience
reaches, a disclosure slot no lens declares, and a default lens that does not exist. The file
is canonical: templates read it for the selector, `?view=` takes its lens ids, and
scripts/validate-models.py rejects a model that names an audience or an epistemic class this
file does not define, so a drift here is a drift everywhere.

usage: validate-audiences.py [--root <repo>]
"""

import os
import re
import sys
import tomllib
from pathlib import Path

LANGUAGES = ("en", "cs")
IDENT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# The disclosure slots a lens may unfold. A component renders exactly these names, so a lens
# that invented one would declare a slot nothing shows; the check is what keeps the two lists
# from drifting apart in opposite directions.
SLOTS = {
    "question", "demonstration", "plain_language", "key_limitation", "mechanism", "assumptions",
    "parameters", "parameter_source", "population", "evidence_level", "citations", "limits",
    "review_date", "gaps", "disclaimer", "ethics", "model_id", "schema", "implementation",
    "tests", "seed", "json", "provenance", "observed", "derived", "inferred", "assumed",
    "illustrative", "unknown", "alternatives", "confidence",
}
# The six words the epistemic vocabulary must define, no more and no fewer: models, figures and
# the detection sandbox classify every part they show with one of them.
EPISTEMIC_KINDS = ("observed", "derived", "inferred", "assumed", "illustrative", "unknown")


def translated(errors, where, entry, field):
    value = entry.get(field)
    if not isinstance(value, dict):
        errors.append(f"{where}: '{field}' needs en and cs values")
        return
    for language in LANGUAGES:
        if not str(value.get(language, "")).strip():
            errors.append(f"{where}: '{field}.{language}' is empty")


def translated_list(errors, where, entry, field, minimum=1):
    items = entry.get(field)
    if not isinstance(items, list) or len(items) < minimum:
        errors.append(f"{where}: '{field}' needs at least {minimum} entr(ies)")
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{where}: '{field}[{index}]' needs en and cs values")
            continue
        for language in LANGUAGES:
            if not str(item.get(language, "")).strip():
                errors.append(f"{where}: '{field}[{index}].{language}' is empty")


def main():
    root = Path(os.environ.get("CAAS_ROOT", Path(__file__).resolve().parent.parent)).resolve()
    if "--root" in sys.argv:
        root = Path(sys.argv[sys.argv.index("--root") + 1]).resolve()
    path = root / "data" / "audiences.toml"
    errors, warnings = [], []

    if not path.exists():
        print("data/audiences.toml is missing", file=sys.stderr)
        return 1
    with open(path, "rb") as handle:
        try:
            doc = tomllib.load(handle)
        except tomllib.TOMLDecodeError as error:
            print(f"data/audiences.toml does not parse: {error}", file=sys.stderr)
            return 1

    lenses = doc.get("lenses", [])
    audiences = doc.get("audiences", [])
    kinds = doc.get("epistemic_kinds", [])
    lens_ids, audience_ids = [], []

    for index, lens in enumerate(lenses):
        where = f"lens[{index}]"
        ident = lens.get("id", "")
        if not IDENT.match(str(ident)):
            errors.append(f"{where}: id '{ident}' is not kebab-case")
        else:
            where = f"lens {ident}"
            if ident in lens_ids:
                errors.append(f"{where}: duplicate id")
            lens_ids.append(ident)
        for field in ("label", "summary", "question"):
            translated(errors, where, lens, field)
        reveals = lens.get("reveals", [])
        if not isinstance(reveals, list) or not reveals:
            errors.append(f"{where}: 'reveals' names no disclosure slot")
        else:
            for slot in reveals:
                if slot not in SLOTS:
                    errors.append(f"{where}: reveals '{slot}', which no component renders")
        entry = lens.get("entry", "")
        if not entry:
            errors.append(f"{where}: 'entry' names no starting point")
        elif not (root / "content" / entry).exists():
            errors.append(f"{where}: entry content/{entry} does not exist")

    default = doc.get("default_lens", "")
    if default not in lens_ids:
        errors.append(f"default_lens '{default}' is not one of the lenses: {lens_ids}")

    reached = set()
    for index, audience in enumerate(audiences):
        where = f"audience[{index}]"
        ident = audience.get("id", "")
        if not IDENT.match(str(ident)):
            errors.append(f"{where}: id '{ident}' is not kebab-case")
        else:
            where = f"audience {ident}"
            if ident in audience_ids:
                errors.append(f"{where}: duplicate id")
            audience_ids.append(ident)
        lens = audience.get("lens", "")
        if lens not in lens_ids:
            errors.append(f"{where}: lens '{lens}' is not one of {lens_ids}")
        else:
            reached.add(lens)
        for field in ("label", "description", "never"):
            translated(errors, where, audience, field)
        translated_list(errors, where, audience, "questions", minimum=2)
        entry = audience.get("entry", "")
        if not entry:
            errors.append(f"{where}: 'entry' names no starting point")
        elif not (root / "content" / entry).exists():
            errors.append(f"{where}: entry content/{entry} does not exist")

    for lens in lens_ids:
        if lens not in reached:
            errors.append(f"lens {lens}: no audience maps to it, so nothing explains who it is for")

    seen_kinds = []
    for index, kind in enumerate(kinds):
        where = f"epistemic_kind[{index}]"
        ident = kind.get("id", "")
        where = f"epistemic kind {ident}" if ident else where
        seen_kinds.append(ident)
        for field in ("label", "definition"):
            translated(errors, where, kind, field)
    if tuple(seen_kinds) != EPISTEMIC_KINDS:
        errors.append(
            "the epistemic vocabulary must define exactly "
            f"{list(EPISTEMIC_KINDS)}, in that order; it defines {seen_kinds}"
        )

    print("AUDIENCES")
    print("────────────────────")
    print(f"lenses ............ {len(lens_ids)}")
    print(f"audiences ......... {len(audience_ids)}")
    print(f"epistemic kinds ... {len(seen_kinds)}")
    print(f"default lens ...... {default}")
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
