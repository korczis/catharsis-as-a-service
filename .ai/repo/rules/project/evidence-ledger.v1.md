---
id: project.evidence-ledger
version: 1
kind: rule
title: Every public claim is in the evidence ledger and within its review date
description: Claims are recorded with type, evidence level, confidence, sources, pages and review dates; stale or inconsistent entries fail the build.
statement: A substantive claim may be published only when data/claims.toml records it with sources appraised in data/sources.toml, an evidence level no stronger than its best source, and a review date that has not passed.
status: active
class: blocking
depends_on: [project.verified-deployment@1]
tags: [content, evidence, verification]
---

# Rationale

A reference that resolves in Crossref shows that a paper exists, not that it supports the sentence citing
it, nor that the sentence is still current. Grading and dating each claim makes the strength of the site's
statements inspectable and makes neglect visible: an unreviewed claim expires instead of silently ageing.

# Required behaviour

- `data/sources.toml` appraises every entry in `data/references.toml` (design, level A–E, population,
  appraisal in both languages, review dates).
- `data/claims.toml` lists every substantive claim with `claim_type`, `evidence_level`, `confidence`,
  `sources`, `used_in`, `last_reviewed` and `review_due`. Every research note and advice entry appears in
  some claim's `used_in`.
- Maximum review intervals: clinical-boundary 180 days, empirical 365 days, theoretical, historical,
  technical and artistic 730 days; sources 365 days (730 for classical texts, books, software and records).
- A claim's level is never stronger than the strongest level among its sources; a claim without sources is
  level E.
- Changes to claims are recorded in `data/evidence_changelog.toml`, newest first.
- Artistic material is typed `artistic` and labelled as such on the page.

# Failure behaviour

`scripts/validate-claims.py` fails `scripts/validate.sh` and therefore CI and deployment. The weekly
`Evidence freshness` workflow runs the same check with Crossref and opens an `evidence-update` issue when it
fails. Review the claim against current literature, update the dates and the changelog; never move a date
forward without a review.

# Verification

Automated: the `claims` step of `scripts/validate.sh`, `.github/workflows/evidence-freshness.yml`,
`tests/python/test_validators.py`. Reviewer-owned: whether the appraisal and confidence are justified.
