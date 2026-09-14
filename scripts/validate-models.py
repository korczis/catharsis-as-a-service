#!/usr/bin/env python3
"""The interactive model registry: every model states what it rests on, what was invented and where it breaks.

Validates data/models.toml against docs/MODELS.md: required fields in both languages, claims and sources
that resolve in the ledger, audiences, lenses and epistemic kinds that resolve in data/audiences.toml, an
epistemic class for every part of the model, at least two assumptions and two limits, at least one rule
and one test, an implementation module that exists and exports its entry point, and prediction = false.

The registry is optional while it is being written: with no data/models.toml this reports nothing to check
and passes.

usage: validate-models.py [--root <repo>]
"""

import argparse
import sys
import tomllib
from pathlib import Path

KINDS = {"simulation", "comparison", "sandbox"}
EPISTEMIC_PARTS = ("inputs", "mechanism", "parameters", "output")
EPISTEMIC_CLASSES = {"observed", "derived", "inferred", "assumed", "illustrative", "unknown"}
LANGS = ("en", "cs")
REQUIRED_LENS = "essential"
MINIMUM = 2  # assumptions and limits


def load(path):
    return tomllib.loads(path.read_text(encoding="utf-8"))


def localized(value, where, field, errors):
    if not isinstance(value, dict):
        errors.append(f"{where}: {field} must be a table with en and cs")
        return
    for lang in LANGS:
        if not str(value.get(lang, "")).strip():
            errors.append(f"{where}: {field} is missing its {lang} text")


def check_epistemics(model, where, errors, classes):
    epistemics = model.get("epistemics")
    if not isinstance(epistemics, dict):
        errors.append(f"{where}: needs an [epistemics] table classifying {', '.join(EPISTEMIC_PARTS)}")
        return
    for part in EPISTEMIC_PARTS:
        value = epistemics.get(part)
        if value is None:
            errors.append(f"{where}: epistemics.{part} is missing")
        elif value not in classes:
            errors.append(f"{where}: epistemics.{part} is '{value}', not one of {sorted(classes)}")


def check_implementation(model, where, root, errors):
    implementation = model.get("implementation")
    if not isinstance(implementation, dict):
        errors.append(f"{where}: needs an [implementation] table naming its module, entry point and tests")
        return
    module = implementation.get("module", "")
    entry = implementation.get("entry", "")
    tests = implementation.get("tests", [])
    if not module:
        errors.append(f"{where}: implementation.module is missing")
    elif not (root / module).exists():
        errors.append(f"{where}: implementation.module does not exist: {module}")
    elif entry and entry not in (root / module).read_text(encoding="utf-8"):
        errors.append(f"{where}: implementation.entry '{entry}' does not appear in {module}")
    if not entry:
        errors.append(f"{where}: implementation.entry is missing")
    if not tests:
        errors.append(f"{where}: implementation.tests names no test; a model without one is a drawing")
    for test in tests:
        if not (root / test).exists():
            errors.append(f"{where}: implementation test does not exist: {test}")


def check_rules(model, where, errors, claim_ids):
    rules = model.get("rules", [])
    if not rules:
        errors.append(f"{where}: needs at least one rule; the behaviour has to be written down, not only coded")
    for number, rule in enumerate(rules, start=1):
        at = f"{where} rule {number}"
        if not rule.get("id"):
            errors.append(f"{at}: needs an id")
        localized(rule.get("statement"), at, "statement", errors)
        if not str(rule.get("formula", "")).strip():
            errors.append(f"{at}: needs a formula, as text")
        claim = rule.get("claim", None)
        if claim is None:
            errors.append(f"{at}: needs claim = \"…\", or \"\" when it is a drawing convention")
        elif claim and claim_ids and claim not in claim_ids:
            errors.append(f"{at}: names a claim that is not in the ledger: {claim}")


def check_url_state(model, where, errors):
    for number, param in enumerate(model.get("url_state", []), start=1):
        at = f"{where} url_state {number}"
        if not param.get("name"):
            errors.append(f"{at}: needs a name")
        for key in ("min", "max", "default"):
            if not isinstance(param.get(key), (int, float)) or isinstance(param.get(key), bool):
                errors.append(f"{at}: {key} must be a number")
        if isinstance(param.get("min"), (int, float)) and isinstance(param.get("max"), (int, float)):
            if param["min"] >= param["max"]:
                errors.append(f"{at}: min must be below max")
            elif not param["min"] <= param.get("default", param["min"]) <= param["max"]:
                errors.append(f"{at}: default lies outside min–max")


def check_model(model, root, errors, claim_ids, reference_ids, audiences, lenses, classes):
    ident = model.get("id", "")
    where = f"data/models.toml: model '{ident or '?'}'"
    if not ident:
        errors.append("data/models.toml: a model has no id")
    if model.get("kind") not in KINDS:
        errors.append(f"{where}: kind must be one of {sorted(KINDS)}")
    for field in ("title", "question", "aria"):
        localized(model.get(field), where, field, errors)

    if model.get("prediction", None) is not False:
        errors.append(f"{where}: prediction must be false; this site models arguments, not people")

    claims = model.get("claims", [])
    if not claims:
        errors.append(f"{where}: names no claims; a model that argues from evidence says which claims it rests on")
    for claim in claims:
        if claim_ids and claim not in claim_ids:
            errors.append(f"{where}: names a claim that is not in the ledger: {claim}")
    for source in model.get("sources", []):
        if reference_ids and source not in reference_ids:
            errors.append(f"{where}: names a source that is not in the reference registry: {source}")
    for audience in model.get("audiences", []):
        if audiences and audience not in audiences:
            errors.append(f"{where}: names an audience that is not in data/audiences.toml: {audience}")

    for field in ("assumptions", "limits"):
        entries = model.get(field, [])
        if len(entries) < MINIMUM:
            errors.append(f"{where}: needs at least {MINIMUM} {field}, found {len(entries)}")
        for number, entry in enumerate(entries, start=1):
            localized(entry, f"{where} {field[:-1]} {number}", field[:-1], errors)

    explanations = model.get("explanations", {})
    if REQUIRED_LENS not in explanations:
        errors.append(f"{where}: needs explanations.{REQUIRED_LENS}; every model is explained to a first reader")
    for lens, text in explanations.items():
        if lenses and lens not in lenses:
            errors.append(f"{where}: explanations.{lens} is not a lens in data/audiences.toml")
        localized(text, f"{where} explanations.{lens}", "explanation", errors)

    check_epistemics(model, where, errors, classes)
    check_implementation(model, where, root, errors)
    check_rules(model, where, errors, claim_ids)
    check_url_state(model, where, errors)


def ids_from(path, key, field="id"):
    if not path.exists():
        return frozenset()
    data = load(path)
    entries = data.get(key, [])
    if isinstance(entries, dict):
        return frozenset(entries)
    return frozenset(entry[field] for entry in entries if field in entry)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    root = parser.parse_args().root.resolve()
    registry = root / "data" / "models.toml"
    errors = []

    print("MODELS")
    print("────────────────────")
    if not registry.exists():
        print("registry .......... absent")
        print()
        print("PASS")
        return 0

    data = load(registry)
    models = data.get("models", [])
    claim_ids = ids_from(root / "data" / "claims.toml", "claims")
    reference_ids = ids_from(root / "data" / "references.toml", "references")
    audience_path = root / "data" / "audiences.toml"
    audiences = ids_from(audience_path, "audiences")
    lenses = ids_from(audience_path, "lenses")
    # Once data/audiences.toml exists its vocabulary is the only one: a silent fallback to the built-in
    # classes would hide the day the two drift apart.
    if audience_path.exists():
        classes = ids_from(audience_path, "epistemic_kinds")
        if not classes:
            errors.append("data/audiences.toml: declares no [[epistemic_kinds]], so no model can be classified")
    else:
        classes = EPISTEMIC_CLASSES

    seen = set()
    for model in models:
        ident = model.get("id")
        if ident in seen:
            errors.append(f"data/models.toml: duplicate model id '{ident}'")
        seen.add(ident)
        check_model(model, root, errors, claim_ids, reference_ids, audiences, lenses, classes)

    print(f"models ............ {len(models)}")
    print(f"audiences ......... {'declared' if audiences else 'not declared yet'}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
