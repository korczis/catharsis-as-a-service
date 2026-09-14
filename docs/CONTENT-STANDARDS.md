# Content standards

The site is a popular-science publication with a medical responsibility. These standards are enforced where a
machine can decide, and by review where it cannot. The rules behind them are `project.no-neuro-overreach`,
`project.medical-claims` and `project.evidence-ledger` in `.ai/repo/rules/project/`.

## Register

- Detailed, precise and readable. Give the reasoning behind a statement, not only the statement.
- Report what was measured, in whom, with which design, then what it is consistent with, then what it cannot
  establish.
- No promotional tone, including in how the artwork is framed.
- English and Czech are equal editions with identical front-matter structure; Czech is written, not transliterated.

## Uncertainty vocabulary

Use these phrases consistently (they are defined on the methods page):

| Phrase | Use when |
|---|---|
| is consistent with | the observation fits an interpretation but does not single it out |
| is associated with | a correlation was found; direction and cause are open |
| suggests | evidence points one way but is limited in design or size |
| inferred with low confidence | a conclusion about one person or one moment from indirect signals |
| insufficient evidence | studies are too few, too small or too inconsistent |
| not measured | nobody recorded it, including on this site |
| unknown | it cannot be established from the available information |

## Prohibited phrasing

[scripts/validate-content.py](../scripts/validate-content.py) fails on these, case-insensitively, in content, data, templates, UI strings, the
README and documentation (this file is the only exemption, because it defines the list):

| English | Czech | Why |
|---|---|---|
| proves that | dokazuje, že | single studies and syntheses support, they do not prove |
| detects emotion / reads emotion | detekuje emoce / čte emoce | signals are recorded; emotions are inferred, with error |
| diagnose / diagnoses | diagnostikuje | the site assesses no one; clinical terms such as "diagnosed with PTSD" remain allowed |
| guarantee(s/d) | garantuje | outcomes for individuals cannot be promised |
| scientifically proven | vědecky prokázáno | not a scientific category |
| the brain does / decides / knows / wants / releases / tells | mozek dělá / ví / chce / rozhoduje / uvolňuje | attribute findings to measures: "activity in X was associated with Y" |

Rewrite the sentence; never add a file to the exemption list.

## Medical responsibility

- Every research note and advice entry renders the disclaimer; the landing page shows the clinical boundary.
- Advice entries have an evidence grade, at least three practice steps and at least two explicit limits.
- Structured data uses `Article` (library pages) and `CollectionPage` (listings), never `MedicalWebPage`.
- Nothing measures, profiles or assesses a visitor; interactive models run on invented inputs and say so.

## Art and evidence

The artwork's numbers are artistic. They carry the ARTISTIC label (`kind-artistic`), the simulation on the methods
page carries "Simulation · not biometric analysis", and concept screenshots carry "Concept screens · illustrative
data". Library pages carry EMPIRICAL (or TECHNICAL for the method note).

## Structure and front matter

- Research notes: `kicker`, `summary`, at least three `key_points`, `references` (registry ids), `figures`
  (`[]` when none), tags.
- Advice entries: `kicker`, `evidence_grade`, `evidence_label`, `recommendation`, `practice`, `limits`, `related`,
  `references`, tags.
- Every page and section: `description` of 50–320 characters.
- Every substantive claim: an entry in `data/claims.toml` (see [EVIDENCE.md](EVIDENCE.md)).
- Links to glossary terms use the page anchors (`../../glossary/#reappraisal`, Czech `../../slovnik/#reappraisal`).

## Commands

Every command mentioned in content, the README or `docs/` is registered in `data/commands.toml` and linked to its
entry, for example [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate).
Commands inside code blocks must be registered too.

## Checks

- [`python3 scripts/validate-content.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-content):
  front matter, descriptions, prohibited phrasing, command links.
- [`python3 scripts/validate-claims.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-claims):
  the evidence ledger and glossary.
- [`python3 scripts/check-references.py --online`](https://korczis.github.io/catharsis-as-a-service/commands/#check-references):
  the bibliography against Crossref.
