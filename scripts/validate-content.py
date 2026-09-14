#!/usr/bin/env python3
"""Content standards and the command registry.

Content standards:
  - banned promotional phrasing (the site is scholarly, not a campaign)
  - required front matter for research notes and advice entries, including evidence grades
  - SEO: every page and section has a description of useful length
  - related links in advice entries point at existing content

Command registry (data/commands.toml):
  - every command mentioned in content, README.md or docs/ is registered
  - every command mentioned inline in prose links to its registry entry (#<id>)
  - commands inside code blocks must be registered

usage: validate-content.py [--root <repo>]
"""

import argparse
import re
import sys
import tomllib
from pathlib import Path

FRONT_MATTER = re.compile(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n?(.*)\Z", re.S)
BANNED = ("festival poster", "festivalový plakát", "festivalovy plakat")
# Medical and neuroscientific overreach (.ai/repo/rules/project/no-neuro-overreach.v1.md and
# medical-claims.v1.md). Matched case-insensitively in content, data, templates, UI strings and docs.
PROHIBITED = (
    (r"\bproves? that\b", "proves that"),
    (r"\bdetect(?:s|ed|ing)? emotions?\b", "detects emotion"),
    (r"\bread(?:s|ing)? emotions?\b", "reads emotion"),
    (r"\bdiagnos(?:e|es)\b", "diagnoses"),
    (r"\bguarantee(?:s|d)?\b", "guarantees"),
    (r"\bscientifically proven\b", "scientifically proven"),
    (r"\bthe brain (?:does|decides|knows|wants|releases|tells|thinks|feels)\b", "the brain does X"),
    (r"\bdokazuj(?:e|í),? že\b", "dokazuje, že"),
    (r"\bdetekuj\w* emoc", "detekuje emoce"),
    (r"\bčt(?:e|ou) emoc", "čte emoce"),
    (r"\bdiagnostikuj\w*", "diagnostikuje"),
    (r"\bgarantuj\w*", "garantuje"),
    (r"\bvědecky prokázan\w*", "vědecky prokázáno"),
    (r"\bmozek (?:dělá|ví|chce|rozhoduje|uvolňuje|cítí|říká)\b", "mozek dělá X"),
)
PROHIBITED_SCAN = ("content/**/*.md", "data/*.toml", "templates/**/*.html", "zola.toml", "README.md", "docs/**/*.md")
# Documents that define the prohibited list have to quote it.
PROHIBITED_EXEMPT = {"docs/CONTENT-STANDARDS.md"}


def check_prohibited(root, errors):
    patterns = [(re.compile(pattern, re.I), label) for pattern, label in PROHIBITED]
    scanned = 0
    for glob in PROHIBITED_SCAN:
        for path in sorted(root.glob(glob)):
            rel = path.relative_to(root).as_posix()
            if rel in PROHIBITED_EXEMPT:
                continue
            scanned += 1
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for pattern, label in patterns:
                    if pattern.search(line):
                        errors.append(f"{rel}:{number}: prohibited phrasing '{label}' ({pattern.search(line).group(0)!r})")
    return scanned
EVIDENCE_GRADES = {"meta-analytic", "replicated-experimental", "experimental", "observational", "theoretical"}
COMMAND_PREFIXES = ("npm ", "npx ", "zola ", "majordomus ", "gh ", "cargo ", "git ", "python3 ", "scripts/", ".venv/bin/")
DESCRIPTION_LENGTH = (50, 320)
LINKED_CODE = re.compile(r"\[`([^`]+)`\]\(([^)\s]+)\)")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.S | re.M)


def looks_like_command(text):
    return text == "npm test" or text.startswith(COMMAND_PREFIXES)


def load_registry(root):
    with open(root / "data" / "commands.toml", "rb") as handle:
        commands = tomllib.load(handle).get("commands", [])
    return sorted(commands, key=lambda entry: len(entry["match"]), reverse=True)


def match_command(text, registry):
    for entry in registry:
        if text == entry["match"] or text.startswith(entry["match"] + " ") or text.startswith(entry["match"]):
            return entry
    return None


def split(path):
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return None, path.read_text(encoding="utf-8")
    return tomllib.loads(match.group(1)), match.group(2)


def check_commands(rel, body, registry, errors, counters):
    without_fences = FENCE.sub("", body)
    for block in FENCE.findall(body):
        for line in block.splitlines():
            command = re.sub(r"\s+#.*$", "", line.strip()).removeprefix("$ ").strip()
            if looks_like_command(command):
                counters["code"] += 1
                if not match_command(command, registry):
                    errors.append(f"{rel}: command in code block is not registered: {command}")
    for text, target in LINKED_CODE.findall(without_fences):
        if not looks_like_command(text):
            continue
        counters["linked"] += 1
        entry = match_command(text, registry)
        if not entry:
            errors.append(f"{rel}: linked command is not registered: {text}")
        elif not target.endswith(f"#{entry['id']}"):
            errors.append(f"{rel}: `{text}` must link to the registry anchor #{entry['id']}, found {target}")
    for text in INLINE_CODE.findall(LINKED_CODE.sub("", without_fences)):
        if looks_like_command(text):
            errors.append(f"{rel}: command `{text}` is mentioned without a link to its registry entry")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    root = parser.parse_args().root.resolve()
    errors = []
    registry = load_registry(root)
    ids = [entry["id"] for entry in registry]
    for ident in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"data/commands.toml: duplicate id '{ident}'")
    counters = {"documents": 0, "research": 0, "advice": 0, "code": 0, "linked": 0}

    content = sorted((root / "content").rglob("*.md"))
    documentation = [root / "README.md", *sorted((root / "docs").rglob("*.md"))] if (root / "docs").exists() else [root / "README.md"]

    for path in content + [p for p in documentation if p.exists()]:
        rel = path.relative_to(root)
        meta, body = split(path)
        text = path.read_text(encoding="utf-8")
        for phrase in BANNED:
            if phrase in text.lower():
                errors.append(f"{rel}: contains banned promotional phrasing '{phrase}'")
        check_commands(rel, body, registry, errors, counters)
        if meta is None:
            continue

        counters["documents"] += 1
        description = meta.get("description", "")
        low, high = DESCRIPTION_LENGTH
        if not low <= len(description) <= high:
            errors.append(f"{rel}: description has {len(description)} characters, expected {low}–{high}")
        extra = meta.get("extra", {})
        tags = meta.get("taxonomies", {}).get("tags", [])
        parts = rel.parts

        if len(parts) >= 3 and parts[1] == "research" and path.name != "_index.md" and not path.name.startswith("_index."):
            counters["research"] += 1
            for key in ("kicker", "summary"):
                if not extra.get(key):
                    errors.append(f"{rel}: research note needs extra.{key}")
            if len(extra.get("key_points", [])) < 3:
                errors.append(f"{rel}: research note needs at least 3 key points")
            if not extra.get("references"):
                errors.append(f"{rel}: research note needs references")
            if "figures" not in extra:
                errors.append(f"{rel}: research note needs extra.figures (use [] when there are none)")
            if not tags:
                errors.append(f"{rel}: research note needs tags")

        if len(parts) >= 3 and parts[1] == "advice" and not path.name.startswith("_index"):
            counters["advice"] += 1
            if extra.get("evidence_grade") not in EVIDENCE_GRADES:
                errors.append(f"{rel}: evidence_grade must be one of {sorted(EVIDENCE_GRADES)}")
            for key in ("kicker", "evidence_label", "recommendation"):
                if not extra.get(key):
                    errors.append(f"{rel}: advice entry needs extra.{key}")
            if len(extra.get("practice", [])) < 3:
                errors.append(f"{rel}: advice entry needs at least 3 practice steps")
            if len(extra.get("limits", [])) < 2:
                errors.append(f"{rel}: advice entry needs at least 2 limits")
            if not extra.get("references"):
                errors.append(f"{rel}: advice entry needs references")
            if not tags:
                errors.append(f"{rel}: advice entry needs tags")
            for related in extra.get("related", []):
                if not (root / "content" / related).exists():
                    errors.append(f"{rel}: related content '{related}' does not exist")
            if not extra.get("related"):
                errors.append(f"{rel}: advice entry needs at least one related research note")

    scanned = check_prohibited(root, errors)

    print("CONTENT")
    print("────────────────────")
    print(f"phrase-linted ..... {scanned} files")
    print(f"documents ......... {counters['documents']}")
    print(f"research notes .... {counters['research']}")
    print(f"advice entries .... {counters['advice']}")
    print(f"commands linked ... {counters['linked']}")
    print(f"commands in code .. {counters['code']}")
    print(f"registry entries .. {len(registry)}")
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
