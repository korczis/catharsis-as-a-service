# Evidence ledger

Every substantive claim on the site is recorded, graded and dated. This document explains the model and the
workflow; the decision behind it is [ADR-0001](../.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md)
and the enforcing rule is `project.evidence-ledger` in `.ai/repo/rules/project/`.

Live views: [evidence ledger](https://korczis.github.io/catharsis-as-a-service/evidence/) ·
[status](https://korczis.github.io/catharsis-as-a-service/status/) ·
[methods](https://korczis.github.io/catharsis-as-a-service/methods/).

## Files

| File | Holds | Checked by |
|---|---|---|
| `data/references.toml` | Bibliography: authors, year, title, container, DOI | Crossref (online) and registry checks |
| `data/sources.toml` | Appraisal of every reference: design, level, population, appraisal, review dates | [scripts/validate-claims.py](../scripts/validate-claims.py) |
| `data/claims.toml` | Every public claim: type, level, confidence, sources, scope, caveat, pages, review dates | [scripts/validate-claims.py](../scripts/validate-claims.py) |
| `data/evidence_changelog.toml` | What changed in the ledger and why, newest first | [scripts/validate-claims.py](../scripts/validate-claims.py) |
| `data/glossary.toml` | Glossary terms with kind, cross references, links and sources | [scripts/validate-claims.py](../scripts/validate-claims.py) |

Bibliographic facts and editorial judgement are deliberately separate: Crossref can verify the first, only a
reviewer can verify the second.

## Vocabulary

**Evidence level** (of a source, and of a claim):

| Level | Meaning |
|---|---|
| A | Meta-analysis or systematic review of controlled studies |
| B | Randomized or controlled experiment(s) |
| C | Longitudinal, prospective or quasi-experimental study |
| D | Cross-sectional, correlational or qualitative study, narrative review, theory |
| E | Classical or historical text, expert opinion, project records, artistic material |

A meta-analysis of correlational studies is level D: the level describes the strongest design underneath,
not the label on the paper. A claim's level may never be stronger than the strongest of its sources, and a
claim without sources is level E.

**Confidence**: `HIGH`, `MODERATE`, `LOW`, `UNKNOWN`. A judgement of how well the claim *as worded* is
supported. Level and confidence are recorded separately: consistent level-D evidence can justify a modest
claim with high confidence; a level-A source with heterogeneous results may only justify moderate confidence.

**Claim type**: `empirical`, `theoretical`, `historical`, `clinical-boundary`, `technical`, `artistic`.
Artistic claims (the poster's telemetry, `problem_solved: false`) are labelled ARTISTIC wherever they appear.

## Review intervals

| Type | Maximum days between `last_reviewed` and `review_due` |
|---|---|
| clinical-boundary | 180 |
| empirical | 365 |
| theoretical, historical, technical, artistic | 730 |
| sources (classical texts, books, software, records) | 365 (730) |

When `review_due` passes, [scripts/validate-claims.py](../scripts/validate-claims.py) fails, which fails CI and blocks deployment. The
scheduled **Evidence freshness** workflow runs the same check and the Crossref check every Monday and opens or
updates an `evidence-update` issue on failure, so expiry is noticed even without a push.

## Reviewing a claim

1. Re-read the sources, and search for newer syntheses (for venting, the 2024 meta-analysis changed the wording).
2. Update the statement, scope, caveat, level and confidence in both languages. Weaken rather than stretch.
3. Set `last_reviewed` to today and `review_due` within the interval for the claim type.
4. Add a `data/evidence_changelog.toml` entry (`reviewed`, `revised`, `downgraded`, `upgraded` or `retracted`).
5. Run [`python3 scripts/validate-claims.py`](https://korczis.github.io/catharsis-as-a-service/commands/#validate-claims)
   and [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate), then push.

Moving a date without a review defeats the ledger; reviewers reject such changes.

## Adding a claim

- Give it a kebab-case `id`, list the English content files that make it in `used_in`, and cite appraised
  sources only. Every research note and advice entry must appear in at least one claim's `used_in`.
- New references go into `data/references.toml` with verified Crossref metadata and get an appraisal in
  `data/sources.toml` in the same change.
- Pages render claims from the ledger (claim cards on research, advice and methods pages); do not restate grades
  by hand.

## Reporting a problem

Readers use the **Evidence update** issue form (`.github/ISSUE_TEMPLATE/evidence-update.yml`), linked from the
evidence page. It asks for the claim id, the problem, and a supporting source.

## Using the ledger elsewhere

The ledger is exported with the content API (`claims.json`, `sources.json`, `glossary.json`,
`evidence_changelog.json`). The Rust client lists claims due for review:
[`cargo run -p caas-cli -- claims list --due-by 2027-03-31`](https://korczis.github.io/catharsis-as-a-service/commands/#caas-cli).
See [RUST-INTEGRATION.md](RUST-INTEGRATION.md).
