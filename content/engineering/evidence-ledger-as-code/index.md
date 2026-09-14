+++
title = "The evidence ledger as code: claims, sources and review dates as validated data"
description = "How every public claim on the site is recorded as data with a type, an evidence level, a confidence, sources and a review date; how validators and a weekly workflow enforce it; and how pages render grades from the ledger instead of restating them."
date = 2026-09-14
weight = 3

[taxonomies]
tags = ["engineering", "evidence", "validation", "data model"]

[extra]
kicker = "Engineering 03"
kind = "technical"
summary = "A reference that resolves in Crossref shows that a paper exists, not that it supports the sentence citing it, nor that the sentence is still current. The site therefore keeps three files apart: a bibliography checked against Crossref, an appraisal of every source, and a ledger of every substantive claim with its grade and review dates. A validator fails the build when a claim is graded above its sources, when a review interval is too long, when a page makes no recorded claim, or when a date has passed. Pages render the grades from the ledger."
key_points = [
  "Bibliographic facts, editorial appraisal and public claims live in separate TOML files, because they change for different reasons and only the first can be checked by a machine.",
  "The validator encodes policy: a claim is never stronger than its best source, clinical-boundary claims are re-reviewed within 180 days, and an expired date fails the build.",
  "Templates, the status page, the JSON API and the Rust client read the same ledger, so a grade is written once and cannot disagree with itself across pages.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## The problem a bibliography does not solve

The first versions of the library cited sources in the usual way: a list of references per page, each with a DOI, and a validator that compared every DOI, title and year with Crossref. That catches invented or mistyped references. It does not answer the questions a careful reader of a psychology site actually has:

- Does the cited study support this sentence, or a nearby one?
- How strong is the support compared with the claim on the next page?
- Who was studied, and does the sentence stay within that population?
- When did anyone last check that the sentence still reflects the literature?

These are editorial judgements, and they age. The decision record that introduced the ledger gives a concrete example: a 2024 meta-analysis on arousal and anger changed how the site's statement about venting should be worded. A claim that nobody revisits does not become visibly wrong; it just stops being true. The design goal was to make that ageing visible and to make the build fail on it.

The decision was recorded in Majordomus at 12:26 UTC on 14 September 2026 and written up as [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md), "Evidence ledger with dated review for every public claim". It shipped in commit [4cbb6fb](https://github.com/korczis/catharsis-as-a-service/commit/4cbb6fb84a94734d2a79ba0e12826d81b36830af) and release [v0.4.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.4.0).

## Three files, three reasons to change

| File | Holds | Changes when | Checked by |
|---|---|---|---|
| [data/references.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/references.toml) | authors, year, title, container, DOI or URL | a citation is added or corrected | Crossref, offline and online |
| [data/sources.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/sources.toml) | design, level A–E, population, appraisal in both languages, review dates | a source is re-read or re-graded | the ledger validator |
| [data/claims.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/claims.toml) | statement, type, level, confidence, sources, scope, caveat, pages, review dates | the literature or the wording changes | the ledger validator |

A fourth file, [data/evidence_changelog.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/evidence_changelog.toml), records what changed, newest first. The ADR explains why appraisal is not a field in the bibliography: that "mixes facts Crossref can verify with judgements it cannot, and a single file would change for two unrelated reasons."

A claim entry looks like this (abridged from the ledger):

```toml
[[claims]]
id = "expressive-writing-coherence"
claim_type = "empirical"
evidence_level = "B"
confidence = "MODERATE"
sources = ["pennebaker-beall-1986", "pennebaker-1997"]
used_in = ["research/what-is-catharsis/index.md", "research/crying-and-sharing/index.md",
           "advice/write-to-make-sense/index.md"]
last_reviewed = 2026-09-14
review_due = 2027-09-14
```

The omitted fields are the ones readers see: `statement`, `scope` and `caveat`, each an inline table with `en` and `cs` values. Here the caveat says that effects vary across studies, that short-term distress often rises after writing, and that "the 1986 abstract could not be re-verified". That last sentence is typical of the ledger's purpose. It does not hide a weak point in the evidence; it records it next to the claim.

## Vocabulary: level and confidence are different things

The ledger uses two scales, and keeping them apart was deliberate.

- **Evidence level** (A to E) describes the design of the best available support. Level A is reserved for syntheses of controlled studies; syntheses of correlational studies are graded by the design of the studies they pool, which is why some meta-analyses sit at D.
- **Confidence** (HIGH, MODERATE, LOW, UNKNOWN) describes how certain the site is that the statement, as worded and scoped, is supported. A historical statement about Aristotle can be level E and HIGH confidence; a laboratory finding can be level B and MODERATE because the studies disagree.

The changelog has its own small vocabulary: `added`, `revised`, `downgraded`, `upgraded`, `retracted` and `reviewed`. A downgrade or a retraction is therefore a visible, dated event with a summary in both languages, not a silent edit to a number, and it lists the ids of the claims it touched.

**Claim types** set the review policy: `empirical`, `theoretical`, `historical`, `clinical-boundary`, `technical` and `artistic`. The artwork's invented telemetry is recorded as an `artistic` claim, so the ledger is also where the site states which of its own numbers are not measurements.

## What the validator enforces

[`python3 scripts/validate-claims.py`](../../commands/#validate-claims) is 255 lines of standard-library Python. Its header lists the failures, and each corresponds to a way the ledger could quietly lose its meaning:

- unknown vocabulary (a level, confidence, type or design outside the lists) and missing translations;
- dangling ids and paths: a claim citing a source that has no appraisal, or a `used_in` page that does not exist;
- a claim graded stronger than its best source;
- a review interval longer than policy allows;
- a research note, theory essay or advice entry that no claim covers;
- any entry whose review date has passed.

The intervals are data in the script, not prose in a document:

```python
CLAIM_INTERVALS = {
    "clinical-boundary": 180, "empirical": 365, "theoretical": 730,
    "historical": 730, "technical": 730, "artistic": 730,
}
SOURCE_INTERVALS = {"classical": 730, "book": 730, "software": 730, "record": 730}
SOURCE_INTERVAL_DEFAULT = 365
```

Two design choices keep this honest. First, the build can fail on a date alone. The ADR names that as a consequence, not a bug: "moving a date requires a review, recorded in the changelog." Second, the date is injectable. The script accepts `--today`, and the test suite uses it to show that the repository's own ledger expires:

```python
def test_repository_ledger_expires_without_review():
    result = run([PY, "scripts/validate-claims.py", "--today", "2031-01-01"])
    assert result.returncode == 1
    assert "(stale)" in result.stdout
```

The other tests in [tests/python/test_evidence.py](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/python/test_evidence.py) build a minimal ledger in a temporary directory and break it one way at a time: a level A claim on a level C source must fail with "stronger than its best source (C)"; a clinical-boundary claim with a one-year interval must fail with "the maximum is 180"; a research note that no claim covers must fail. A validator that has never been seen to fail is not evidence of anything, so every rule has a test that makes it fail.

## A weekly check that does not wait for a push

A ledger that is only validated on push expires silently whenever nobody pushes. [evidence-freshness.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/evidence-freshness.yml) runs every Monday at 06:17 UTC, independent of commits:

```yaml
- name: Claims, sources and glossary are consistent and within their review dates
  run: python3 scripts/validate-claims.py --warn-days 30 | tee claims.txt
- name: References still resolve in Crossref with matching titles and years
  if: always()
  run: python3 scripts/check-references.py --online | tee references.txt
```

When either step fails, the workflow opens an issue labelled `evidence-update`, or comments on the open one, with the error lines and instructions that end: "Dates move only after a review." The workflow was run once by hand on the day it was added ([run 34846806810](https://github.com/korczis/catharsis-as-a-service/actions/runs/34846806810), 38 seconds, passed). The same Crossref comparison, run by [`python3 scripts/check-references.py --online`](../../commands/#check-references), is also a CI job, and it produced the first pipeline failure of the day; see [Testing a static site](@/engineering/testing-a-static-site/index.md).

## Pages render grades; they do not restate them

The rule in the evidence component's header is short: "Pages never restate a claim's grade by hand; they render it from the ledger." The essay template computes the page's content path and asks for every claim whose `used_in` names it:

{% raw -%}
```text
{%- set ledger = load_data(path="data/claims.toml") -%}
{%- set_global found = [] -%}
{%- for c in ledger.claims %}{% if path in c.used_in %}{% set_global found = [...found, c] %}{% endif %}{% endfor -%}
```
{%- endraw %}

Each claim renders as a card with a kind label, a level badge and a confidence badge, the statement, scope and caveat in the page's language, the review dates, and a button that opens the appraised sources. The button is an Alpine disclosure; without JavaScript the panel stays open, and a browser test checks both states. The [evidence page](@/evidence/index.md) lists the whole ledger, and the [status page](@/status/index.md) computes counts, the most recent review and the next reviews due at build time. Its template says: "Nothing here is typed by hand."

Because the ledger is data, it is also exported. The JSON API includes `claims.json`, `sources.json`, `glossary.json` and `evidence_changelog.json`, and the Rust crate re-checks two invariants independently of the Python validator: every reference has an appraisal, and no claim is graded above its best source. The CLI can list claims due before a date with [`cargo run -p caas-cli`](../../commands/#caas-cli), which is how another application could refuse to show a stale claim.

## What it cost and what it does not do

At [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) the ledger held 50 claims, 58 appraised sources and 54 glossary terms, all written in both languages. The ADR is explicit about the price: "Every new substantive claim costs a ledger entry in both languages; content without one fails CI." The parallel content agents described in [Parallel agents, one working tree](@/engineering/parallel-agents-one-tree/index.md) delivered their ledger entries (references, appraisals, claims, glossary terms and changelog lines) as proposal files, which had to validate before their pages could merge.

The validator cannot judge whether an appraisal is right. It can check that a level exists, that it does not exceed the sources, and that someone committed to a review date. Whether a study really supports a sentence remains reviewer-owned, and the project rule [project.evidence-ledger](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/evidence-ledger.v1.md) says so in its verification section. The grading scale is coarse and partly a judgement. The ledger does not make the site's claims correct. It makes their strength, scope and age inspectable, and it makes neglect fail the build instead of going unnoticed.
