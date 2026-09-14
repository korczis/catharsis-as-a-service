---
schema: adr/v1
id: adr-0001
kind: adr
title: Evidence ledger with dated review for every public claim
status: proposed
date: 2026-09-14
tags:
  - evidence
  - content
provenance:
  origin: authored
---

# 1. Evidence ledger with dated review for every public claim

## Context

The site publishes psychological, physiological and clinical statements to a general audience next to an
artwork whose telemetry is deliberately unmeasured. Until now, evidence was expressed in two ways: a
reference registry verified against Crossref, and a free-text evidence grade on advice entries. Neither
records whether a sentence is still supported, how strong its support is compared with other sentences,
who or what it applies to, or when anyone last checked it. Research moves (the 2024 meta-analysis on
arousal and anger changed how the venting claim should be worded), and an unchecked claim ages silently.

## Decision

Keep bibliographic facts and editorial judgement in separate, validated files:

- `data/references.toml` stays the bibliography, verified against Crossref.
- `data/sources.toml` appraises every reference: design, evidence level A–E, population, appraisal in both
  languages, `last_reviewed`, `review_due`.
- `data/claims.toml` records every substantive public claim: type (empirical, theoretical, historical,
  clinical-boundary, technical, artistic), evidence level, confidence (HIGH, MODERATE, LOW, UNKNOWN),
  sources, scope, caveat, the pages that make it, and review dates.
- `data/evidence_changelog.toml` records changes to the ledger, newest first.
- `scripts/validate-claims.py` fails the build on unknown vocabulary, a claim graded above its best source,
  a review interval longer than policy (180 days clinical-boundary, 365 empirical, 730 otherwise), a
  research note or advice entry no claim covers, or any passed review date. A weekly workflow repeats the
  check with Crossref and opens an `evidence-update` issue.
- Pages render grades from the ledger (claim cards, the evidence page, `/status/`) rather than restating them.

## Alternatives rejected

- **Free-text evidence notes on each page.** Readable, but not comparable across pages, not checkable, and
  with no expiry.
- **Appraisal fields inside `data/references.toml`.** Mixes facts Crossref can verify with judgements it
  cannot, and a single file would change for two unrelated reasons.
- **No expiry, periodic manual audits.** Relies on memory; the failure mode is invisible.

## Consequences

- Every new substantive claim costs a ledger entry in both languages; content without one fails CI.
- A build can fail on a date alone. That is intended: moving a date requires a review, recorded in the
  changelog.
- The grading scale is coarse and partly a judgement (for example, meta-analyses of correlational studies
  are graded D). Confidence is recorded separately so that level and certainty are not conflated.
- The content API exports the ledger, so other applications (the Rust client) can refuse stale claims.
