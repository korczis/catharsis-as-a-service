---
id: project.no-scroll-containers
version: 1
kind: rule
title: The page scrolls; nothing inside it does
description: No element of the site carries a scrollbar of its own — figures, tables and code are laid out to the column they sit in, at every width.
statement: A published page has exactly one scrolling surface, the page itself; content that does not fit its column is re-laid out for that width rather than given an inner scroll region, and the body never scrolls sideways.
status: active
class: blocking
depends_on: [project.zola-source-of-truth@1]
tags: [design, accessibility, templates]
---

# Rationale

An inner scroll region hides content behind a gesture the reader has no reason to expect: on a phone a
figure that scrolls sideways looks like a figure that has been cut off, and a scrollbar drawn across a
drawing or a table is an admission that the layout was never made for that width. Scaling a drawing until
its labels are unreadable is the same failure by another route. A width that a layout cannot serve is a
layout decision waiting to be made — stack the row, label the cells, hide the labels the key already
carries — not a scrollbar to be delegated to the reader.

# Required behaviour

- No stylesheet under `styles/` or `static/css/` declares `overflow`, `overflow-x` or `overflow-y` as
  `auto` or `scroll`; no template carries the equivalent utility class. `hidden`, `clip` and `visible`
  are unaffected.
- No figure, table or code block sets a minimum width that exceeds its column; drawings scale with
  `width: 100%` inside their `viewBox`.
- Below 40rem every figure kind has a narrow treatment that keeps its type readable: curves hide the
  series labels inside the plot and show the key below, a pipeline is replaced by its stack. The
  treatments are specified in [`docs/FIGURES.md`](../../../../docs/FIGURES.md).
- Tables stack below 60rem: one record per row, each cell labelled from its column header through
  `data-label`, the header row visually hidden and still read.
- Code and preformatted text wrap (`white-space: pre-wrap`, `overflow-wrap: anywhere`).
- The single exception is a surface that is itself a full-height panel — the mobile navigation drawer —
  whose scroll stands in for the page's own. Exceptions are listed in `scripts/validate-layout.py` with
  a reason; there is no in-file opt-out marker.

# Failure behaviour

`scripts/validate-layout.py` fails `scripts/validate.sh`, and therefore CI and deployment, on a scroll
declaration, a scrolling utility class or a minimum width inside a figure or table selector. The rendered
pages are checked by `tests/site.spec.js` (`nothing inside the page scrolls`), which walks every element
of seven representative pages at 390, 768 and 1440 px and fails on any element that can scroll.
