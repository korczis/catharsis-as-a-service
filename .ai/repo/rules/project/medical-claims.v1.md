---
id: project.medical-claims
version: 1
kind: rule
title: Medical claim policy
description: The site educates about published evidence; it never gives individual diagnosis, treatment or guarantees, and it always shows the clinical boundary.
statement: Health-related text states group-level findings with their limits, never promises outcomes, never assesses an individual, and every research note and advice entry carries the clinical disclaimer.
status: active
class: blocking
depends_on: [project.evidence-ledger@1, project.no-neuro-overreach@1]
tags: [content, medical, safety]
---

# Rationale

Readers come to a page about catharsis because something hurts. Advice that sounds like treatment, or a
number that sounds like an assessment, can delay care. Evidence about groups does not tell a reader what
will happen to them.

# Required behaviour

- Report findings at the level they were obtained (samples, designs, outcomes) with effect direction and,
  where verified, size; never "guaranteed", "scientifically proven" or "cures".
- Advice entries carry an evidence grade, practice steps and at least two explicit limits.
- Claims of type `clinical-boundary` in `data/claims.toml` are reviewed at least every 180 days.
- Every research note and advice entry renders the disclaimer (educational content; when to contact a
  professional or emergency services). The landing page shows the clinical boundary block.
- Structured data marks pages as `Article` or `CreativeWork`, never `MedicalWebPage`: the site is not a
  medical resource.
- Nothing on the site measures, profiles or assesses a visitor.

# Failure behaviour

A missing disclaimer, a `MedicalWebPage` node or a stale clinical-boundary claim fails validation or the
end-to-end tests. Fix the content; do not relax the check.

# Verification

Automated: `scripts/validate-claims.py` (review intervals and staleness), `scripts/validate-content.py`
(prohibited phrases, advice limits), `scripts/validate-html.py` (structured data types) and
`tests/site.spec.js`. Reviewer-owned: the medical accuracy of wording.
