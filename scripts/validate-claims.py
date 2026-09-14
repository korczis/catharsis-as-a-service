#!/usr/bin/env python3
"""Evidence ledger checks.

  data/sources.toml             appraisal of every reference in data/references.toml
  data/claims.toml              every public claim: type, level, confidence, sources, pages, review dates
  data/evidence_changelog.toml  dated changes to the ledger, newest first
  data/glossary.toml            glossary terms: kind, cross references, links and sources

Fails on unknown vocabulary, missing translations, dangling ids or paths, a claim graded stronger
than its best source, a review interval longer than policy allows, a research note or advice entry
that no claim covers, and any entry whose review date has passed. Warns when a review falls due
within --warn-days.

usage: validate-claims.py [--today YYYY-MM-DD] [--warn-days N] [--root <repo>]
       CAAS_TODAY=YYYY-MM-DD overrides the date as well (used by the test suite)
"""

import argparse
import datetime as dt
import os
import re
import sys
import tomllib
from pathlib import Path

LANGUAGES = ("en", "cs")
LEVELS = ("A", "B", "C", "D", "E")
CONFIDENCE = ("HIGH", "MODERATE", "LOW", "UNKNOWN")
CLAIM_TYPES = ("empirical", "theoretical", "historical", "clinical-boundary", "technical", "artistic")
DESIGNS = {
    "meta-analysis", "systematic-review", "review", "experiment", "longitudinal", "cross-sectional",
    "qualitative", "theory", "classical", "book", "software", "record",
}
TERM_KINDS = {"empirical", "theoretical", "clinical", "technical", "artistic", "historical"}
CHANGE_KINDS = {"added", "revised", "downgraded", "upgraded", "retracted", "reviewed"}
# Maximum number of days between last_reviewed and review_due.
CLAIM_INTERVALS = {
    "clinical-boundary": 180, "empirical": 365, "theoretical": 730,
    "historical": 730, "technical": 730, "artistic": 730,
}
SOURCE_INTERVALS = {"classical": 730, "book": 730, "software": 730, "record": 730}
SOURCE_INTERVAL_DEFAULT = 365
COVERED_SECTIONS = ("research", "advice")
IDENT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(root, name, errors):
    path = root / "data" / name
    if not path.exists():
        errors.append(f"data/{name} is missing")
        return {}
    with open(path, "rb") as handle:
        try:
            return tomllib.load(handle)
        except tomllib.TOMLDecodeError as error:
            errors.append(f"data/{name} does not parse: {error}")
            return {}


def translated(errors, where, entry, field):
    value = entry.get(field)
    if not isinstance(value, dict):
        errors.append(f"{where}: '{field}' needs en and cs values")
        return
    for language in LANGUAGES:
        if not str(value.get(language, "")).strip():
            errors.append(f"{where}: '{field}.{language}' is empty")


def is_date(value):
    return isinstance(value, dt.date) and not isinstance(value, dt.datetime)


def review_dates(errors, warnings, where, entry, interval, today, warn_days, schedule):
    reviewed, due = entry.get("last_reviewed"), entry.get("review_due")
    if not (is_date(reviewed) and is_date(due)):
        errors.append(f"{where}: last_reviewed and review_due must be TOML dates")
        return
    if reviewed > today:
        errors.append(f"{where}: last_reviewed {reviewed} is in the future")
    if due < reviewed:
        errors.append(f"{where}: review_due {due} is before last_reviewed {reviewed}")
    elif (due - reviewed).days > interval:
        errors.append(f"{where}: review interval is {(due - reviewed).days} days, the maximum is {interval}")
    if due < today:
        errors.append(f"{where}: review was due on {due} (stale)")
    elif (due - today).days <= warn_days:
        warnings.append(f"{where}: review falls due on {due}")
    schedule.append((due, where))


def check_sources(root, references, sources, today, warn_days, errors, warnings, schedule):
    for ident in sorted(set(references) - set(sources)):
        errors.append(f"sources: reference '{ident}' has no appraisal")
    for ident in sorted(set(sources) - set(references)):
        errors.append(f"sources: '{ident}' is not in data/references.toml")
    for ident, entry in sources.items():
        where = f"sources.{ident}"
        design = entry.get("design")
        if design not in DESIGNS:
            errors.append(f"{where}: design '{design}' is not one of {sorted(DESIGNS)}")
        if entry.get("level") not in LEVELS:
            errors.append(f"{where}: level must be one of {list(LEVELS)}")
        translated(errors, where, entry, "population")
        translated(errors, where, entry, "appraisal")
        interval = SOURCE_INTERVALS.get(design, SOURCE_INTERVAL_DEFAULT)
        review_dates(errors, warnings, where, entry, interval, today, warn_days, schedule)


def check_claims(root, claims, sources, today, warn_days, errors, warnings, schedule):
    seen = set()
    covered = set()
    for index, claim in enumerate(claims):
        ident = claim.get("id", "")
        where = f"claims.{ident or index}"
        if not IDENT.match(ident):
            errors.append(f"{where}: id must be kebab-case")
        if ident in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(ident)
        for field in ("statement", "scope", "caveat"):
            translated(errors, where, claim, field)
        claim_type = claim.get("claim_type")
        if claim_type not in CLAIM_TYPES:
            errors.append(f"{where}: claim_type '{claim_type}' is not one of {list(CLAIM_TYPES)}")
        level = claim.get("evidence_level")
        if level not in LEVELS:
            errors.append(f"{where}: evidence_level must be one of {list(LEVELS)}")
        if claim.get("confidence") not in CONFIDENCE:
            errors.append(f"{where}: confidence must be one of {list(CONFIDENCE)}")

        cited = claim.get("sources", [])
        for source in cited:
            if source not in sources:
                errors.append(f"{where}: source '{source}' is not appraised in data/sources.toml")
        levels = [sources[s]["level"] for s in cited if s in sources and sources[s].get("level") in LEVELS]
        if level in LEVELS:
            best = min(levels, key=LEVELS.index) if levels else "E"
            if LEVELS.index(level) < LEVELS.index(best):
                errors.append(f"{where}: evidence_level {level} is stronger than its best source ({best})")

        used_in = claim.get("used_in", [])
        if not used_in:
            errors.append(f"{where}: used_in names no page")
        for path in used_in:
            if not (root / "content" / path).exists():
                errors.append(f"{where}: used_in page content/{path} does not exist")
            covered.add(path)
        interval = CLAIM_INTERVALS.get(claim_type, min(CLAIM_INTERVALS.values()))
        review_dates(errors, warnings, where, claim, interval, today, warn_days, schedule)

    for section in COVERED_SECTIONS:
        for page in sorted((root / "content" / section).glob("*/index.md")):
            rel = page.relative_to(root / "content").as_posix()
            if rel not in covered:
                errors.append(f"claims: content/{rel} makes claims but no ledger entry lists it in used_in")
    return seen


def check_changelog(entries, claim_ids, today, errors):
    previous = None
    for index, entry in enumerate(entries):
        where = f"evidence_changelog[{index}]"
        date = entry.get("date")
        if not is_date(date):
            errors.append(f"{where}: date must be a TOML date")
            continue
        if date > today:
            errors.append(f"{where}: date {date} is in the future")
        if previous and date > previous:
            errors.append(f"{where}: entries must be ordered newest first")
        previous = date
        if entry.get("kind") not in CHANGE_KINDS:
            errors.append(f"{where}: kind must be one of {sorted(CHANGE_KINDS)}")
        translated(errors, where, entry, "summary")
        for ident in entry.get("claims", []):
            if ident not in claim_ids:
                errors.append(f"{where}: claim '{ident}' does not exist")


def check_glossary(root, terms, references, errors):
    ids = [term.get("id", "") for term in terms]
    for index, term in enumerate(terms):
        ident = term.get("id", "")
        where = f"glossary.{ident or index}"
        if not IDENT.match(ident):
            errors.append(f"{where}: id must be kebab-case")
        if ids.count(ident) > 1:
            errors.append(f"{where}: duplicate id")
        translated(errors, where, term, "term")
        translated(errors, where, term, "definition")
        if term.get("kind") not in TERM_KINDS:
            errors.append(f"{where}: kind must be one of {sorted(TERM_KINDS)}")
        for other in term.get("see_also", []):
            if other not in ids:
                errors.append(f"{where}: see_also '{other}' is not a term")
            if other == ident:
                errors.append(f"{where}: see_also refers to itself")
        for path in term.get("links", []):
            if not (root / "content" / path).exists():
                errors.append(f"{where}: link content/{path} does not exist")
        for reference in term.get("references", []):
            if reference not in references:
                errors.append(f"{where}: reference '{reference}' is not registered")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--today", help="evaluate review dates as of this date (default: today, UTC)")
    parser.add_argument("--warn-days", type=int, default=30, help="warn when a review falls due within N days")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    today_text = args.today or os.environ.get("CAAS_TODAY")
    today = dt.date.fromisoformat(today_text) if today_text else dt.datetime.now(dt.timezone.utc).date()

    errors, warnings, schedule = [], [], []
    references = load(root, "references.toml", errors).get("references", {})
    sources = load(root, "sources.toml", errors).get("sources", {})
    claims = load(root, "claims.toml", errors).get("claims", [])
    changelog = load(root, "evidence_changelog.toml", errors).get("entries", [])
    terms = load(root, "glossary.toml", errors).get("terms", [])

    check_sources(root, references, sources, today, args.warn_days, errors, warnings, schedule)
    claim_ids = check_claims(root, claims, sources, today, args.warn_days, errors, warnings, schedule)
    check_changelog(changelog, claim_ids, today, errors)
    check_glossary(root, terms, references, errors)

    def tally(field, values):
        return " · ".join(f"{value} {sum(1 for c in claims if c.get(field) == value)}" for value in values)

    print("EVIDENCE")
    print("────────────────────")
    print(f"as of ............. {today}")
    print(f"sources ........... {len(sources)}")
    print(f"claims ............ {len(claims)}")
    print(f"  by level ........ {tally('evidence_level', LEVELS)}")
    print(f"  by confidence ... {tally('confidence', CONFIDENCE)}")
    print(f"  by type ......... {tally('claim_type', CLAIM_TYPES)}")
    print(f"changelog ......... {len(changelog)}")
    print(f"glossary terms .... {len(terms)}")
    if schedule:
        due, where = min(schedule)
        print(f"next review ....... {due} ({where})")
    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
