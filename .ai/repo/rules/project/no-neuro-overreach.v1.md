---
id: project.no-neuro-overreach
version: 1
kind: rule
title: No neuroscientific or measurement overreach
description: Text never claims that a signal, a model or a brain region reveals what a person feels, and never presents correlational neuroscience as mechanism.
statement: Every statement about physiology, the brain or measurement separates what was recorded from what was inferred, attributes findings to measures and studies, and uses the site's uncertainty vocabulary.
status: active
class: blocking
depends_on: [project.evidence-ledger@1]
tags: [content, science, measurement]
---

# Rationale

Popular writing about emotion routinely turns an association into a mechanism ("the brain releases")
and a sensor reading into a mental state ("detects emotion"). Both are false as stated. Meta-analytic
evidence shows no consistent autonomic or facial "fingerprint" for emotion categories, so any such
sentence misleads readers about what technology and science can know about them. This site exists to
make that distinction visible; its own text has to model it.

# Required behaviour

- Distinguish signal, feature, inference and context (see the methods page). Say what was recorded, then
  what it is consistent with, then what it cannot establish.
- Attribute neural findings to measures and designs: "activity in X was associated with Y in imaging
  studies", not "X causes Y" or "the brain does Y".
- Use the uncertainty vocabulary: "is consistent with", "is associated with", "suggests",
  "inferred with low confidence", "insufficient evidence", "not measured", "unknown".
- Anything that looks like data but is not measured is labelled ARTISTIC or SIMULATION where it appears.
- The prohibited phrases listed in `docs/CONTENT-STANDARDS.md` do not appear in content, data, templates,
  UI strings, the README or documentation (other than the standard that defines them).

# Failure behaviour

`scripts/validate-content.py` fails the build with the file, line and matched phrase. Rewrite the sentence
so that it describes the measure and the uncertainty; do not add the file to the exemption list.

# Verification

Automated: the `content` step of `scripts/validate.sh` (prohibited phrase linter) and
`tests/python/test_validators.py`. Reviewer-owned: wording that avoids the list but still overreaches.
