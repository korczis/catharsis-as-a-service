#!/usr/bin/env python3
"""No scroll containers: the page scrolls, nothing inside it does (project.no-scroll-containers).

Scans the stylesheet sources and the templates for declarations and utility classes that give an
element a scrollbar of its own, and for minimum widths that would push a figure or table past its
column. Exceptions are listed here with a reason; there is no in-file opt-out marker.

The static check is the fast gate; tests/site.spec.js proves the rendered pages at three widths.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CAAS_ROOT", Path(__file__).resolve().parent.parent)).resolve()
STYLESHEETS = ["styles/app.css", "static/css/case-study.css", "static/css/interactive.css"]
TEMPLATES = "templates"

# overflow that creates a scroll container; `hidden`, `clip` and `visible` do not.
SCROLLING_DECLARATION = re.compile(r"overflow(?:-[xy])?\s*:\s*(auto|scroll)\b")
SCROLLING_UTILITY = re.compile(r"overflow-(?:x-|y-)?(?:auto|scroll)\b")
# A minimum width inside a figure or a table is what made them scroll before; both are laid out to
# the column now, so a new one is a regression rather than a choice.
MIN_WIDTH = re.compile(r"^\s*min-width\s*:\s*([0-9.]+)(rem|em|px|ch)\s*;", re.M)
MIN_WIDTH_SELECTORS = re.compile(r"\.(ill-|ledger-table|matrix-table|case-table|metrics|table-frame)")

# file -> (identifier, reason). A surface that is itself a viewport-sized panel scrolls as the page
# would; it is not content inside a page.
EXCEPTIONS = {
    "templates/partials/nav.html": (
        "overflow-y-auto",
        "the mobile navigation drawer is a full-height panel: its scroll is the page's own",
    ),
}


def relative(path):
    return str(path.relative_to(ROOT))


def check_stylesheets(errors):
    for name in STYLESHEETS:
        path = ROOT / name
        if not path.exists():
            errors.append(f"{name}: stylesheet is missing")
            continue
        blocks = path.read_text(encoding="utf-8")
        for number, line in enumerate(blocks.splitlines(), 1):
            if SCROLLING_DECLARATION.search(line):
                errors.append(f"{name}:{number}: scroll container — {line.strip()}")
        # A minimum width is only read against the selector it belongs to, so the check is per rule.
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", blocks):
            selector, body = rule.group(1), rule.group(2)
            if MIN_WIDTH_SELECTORS.search(selector) and MIN_WIDTH.search(body):
                value = MIN_WIDTH.search(body).group(0).strip()
                if not value.startswith("min-width: 0"):
                    number = blocks[: rule.start()].count("\n") + 1
                    errors.append(
                        f"{name}:{number}: {selector.strip().splitlines()[-1]} sets {value} — "
                        "a figure or table is laid out to its column, not scrolled"
                    )


def check_templates(errors):
    for path in sorted((ROOT / TEMPLATES).rglob("*.html")):
        name = relative(path)
        allowed = EXCEPTIONS.get(name, (None, None))[0]
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in SCROLLING_UTILITY.finditer(line):
                if match.group(0) == allowed:
                    continue
                errors.append(f"{name}:{number}: scroll container — class {match.group(0)}")


def main():
    errors = []
    check_stylesheets(errors)
    check_templates(errors)

    print("LAYOUT")
    print("────────────────────")
    print(f"stylesheets  {len(STYLESHEETS)}")
    print(f"templates    {len(list((ROOT / TEMPLATES).rglob('*.html')))}")
    for name, (identifier, reason) in sorted(EXCEPTIONS.items()):
        print(f"allowed      {name} ({identifier}): {reason}")
    print()
    for error in errors:
        print(f"error: {error}")
    print()
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
