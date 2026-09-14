+++
title = "Testing a static site: validators, negative tests, browsers and contracts"
description = "The layers of checks between a commit and a release: an ordered validation script, Python validators that are tested to fail, Playwright on a subpath preview and on production, Rust contract tests, and a command registry whose every entry is executed."
date = 2026-09-14
weight = 4

[taxonomies]
tags = ["engineering", "testing", "playwright", "validation"]

[extra]
kicker = "Engineering 04"
kind = "technical"
summary = "A static site has no server to break, so it is tempting to test it lightly. This one publishes graded claims in two languages under a repository subpath, and most of its failure modes are silent: a missing translation, a stale claim, a broken anchor, an asset URL that works locally and not in production. This article describes the checks that catch them, the principle that every validator must be seen to fail, and the three failures the pipeline recorded on the day the site was built."
key_points = [
  "Validation runs as twelve ordered stages from cheapest to most expensive, and the same script gates local work, CI and deployment.",
  "Every Python validator has tests that feed it a deliberately broken fixture and assert the exact error, so a validator that silently passes everything would fail its own suite.",
  "The browser suite runs twice per release: on a local build served under the production subpath before deployment, and on the live URL after it."
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## What can go wrong in a static site

The site in this repository has no database and no application server, and still has many ways to be wrong in production without any error message:

- the Czech edition of a page is missing, or has a different front-matter shape than the English one;
- a UI string exists in one dictionary and not the other, so a template renders an empty label;
- a claim on a page has passed its review date;
- a reference cites a DOI whose title no longer matches;
- an in-page anchor or an asset URL is broken, often only under the `/catharsis-as-a-service/` subpath;
- structured data does not parse, or describes a page as a medical resource;
- a command mentioned in documentation does not exist, or exists but no test runs it;
- the deployment succeeded, but the CDN still serves the previous build.

Each item on that list has a check in the repository. This article walks through the checks from the fastest to the slowest, then through the failures they recorded. The pipeline that runs them is described in [How the site was built](@/engineering/how-the-site-was-built/index.md).

## Stage 1: one ordered validation script

[`npm run validate`](../../commands/#npm-run-validate) runs [scripts/validate.sh](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate.sh). Every step is wrapped in the same function, which records PASS or FAIL, prints a summary table and stops at the first failure:

```bash
step() {
  local name="$1"
  shift
  printf '\n── %s: %s\n' "$name" "$*"
  if "$@"; then
    RESULTS+=("$name|PASS")
  else
    RESULTS+=("$name|FAIL")
    report
    printf '\nRESULT %s FAIL\n' "$(dots RESULT)"
    exit 1
  fi
}
```

The stages are, in order: toolchain (the Zola version must equal `.zola-version`), assets, JavaScript syntax, translations, content standards, references, the evidence ledger, social previews, the Zola check, the Zola build, the API export, and the HTML checks on the generated site. The order is deliberate. The translation check takes well under a second and catches the most common authoring error, so it runs before a build that takes much longer.

The script has no options to skip a stage. The project rule on deployment says "Validation is never bypassed to make CI pass: no `|| true` around a mandatory check, no `--no-verify`", and the CI job runs the same entry point as a developer does.

## Stage 2: Python validators that are tested to fail

The validators are small standard-library Python scripts, each with one responsibility:

| Validator | Catches |
|---|---|
| [validate-i18n.py](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate-i18n.py) | missing translations of content files, front-matter shape mismatches, UI keys used in templates but not defined |
| [`python3 scripts/validate-content.py`](../../commands/#validate-content) | missing research-note fields, description length, prohibited phrasing, unregistered or unlinked commands |
| [`python3 scripts/check-references.py --online`](../../commands/#check-references) | unknown citations, articles without a DOI; online, title and year mismatches with Crossref |
| [`python3 scripts/validate-claims.py`](../../commands/#validate-claims) | the evidence ledger rules described in [The evidence ledger as code](@/engineering/evidence-ledger-as-code/index.md) |
| [`python3 scripts/render-social.py`](../../commands/#render-social) with `--check` | a page without a preview image, a stale image, an orphaned image |
| [validate-html.py](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate-html.py) | duplicate ids, missing alt text, heading jumps, broken first-party references and anchors, invalid JSON-LD, medical schema types, incomplete preview metadata |

A validator is only useful if it fails when it should, and a validator that passes on the repository proves nothing about that. The test module's docstring states the rule: "Validators must pass on the repository and fail on the defects they exist to catch." Almost every validator therefore has two kinds of test in [tests/python](https://github.com/korczis/catharsis-as-a-service/tree/main/tests/python): one that runs it on the real repository and expects success, and several that build a minimal broken fixture in a temporary directory and assert the specific message:

```python
def test_content_rejects_wrong_registry_anchor(tmp_path):
    root = _content_fixture(tmp_path, "Run [`npm run validate`](../commands/#npm-test).\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "must link to the registry anchor #npm-run-validate" in result.stdout
```

The fixture approach requires every validator to accept a `--root` argument or a `CAAS_ROOT` environment variable, a small design constraint that falls out of wanting negative tests. The ledger validator also accepts `--today`, which lets a test show that the repository's own claims expire in 2031 without a review.

[`npm run test:python`](../../commands/#npm-run-test-python) runs the suite in a project virtual environment. At [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) it had 40 tests.

## Stage 3: the command registry is executed

Documentation that lists commands tends to rot, so every command the site, the README or the docs mention is recorded in [data/commands.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/commands.toml) with a `verified_by` list naming the CI jobs or pytest functions that run it. The content validator refuses a command in prose that does not link to its entry. [tests/python/test_commands.py](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/python/test_commands.py) closes the loop in the other direction: it parses the workflow files and the test modules, and fails if a `verified_by` name does not exist.

```python
for reference in entry["verified_by"]:
    kind, _, name = reference.partition(":")
    if kind == "ci" and name not in jobs:
        problems.append(f"{entry['id']}: CI job '{name}' does not exist (known: {sorted(jobs)})")
    elif kind == "pytest" and name not in tests:
        problems.append(f"{entry['id']}: pytest '{name}' does not exist")
```

The same module runs commands for real: the commit linter on a good and a bad message, the release script in dry-run mode, a production build, the development server (polled until it answers), `--help` for every Majordomus subcommand, and a read of the pipeline history through the GitHub CLI. Tests that need an external tool skip locally when the tool is missing, but CI sets `CAAS_REQUIRE_TOOLS=1`, and then a missing tool fails instead of skipping. Without that switch, a registry entry could be "verified" by a test that never ran.

Every link to a command in this article points at that registry. You are reading the result of the check that enforces it.

## Stage 4: Playwright on the production subpath

[`npm test`](../../commands/#npm-test) runs the browser suite in [tests/site.spec.js](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/site.spec.js). With no `BASE_URL`, Playwright starts the preview server itself, so the suite runs against the production build served under the same subpath as GitHub Pages:

```js
const LOCAL_URL = 'http://127.0.0.1:4173/catharsis-as-a-service/';
const baseURL = process.env.BASE_URL || LOCAL_URL;
```

Several test blocks are loops over locales, viewports and pages, so the number of executed tests is larger than the number of blocks. The suite checks what only a browser can see: pages render at every configured viewport without horizontal overflow; every page is self-canonical with correct `hreflang` alternates; the Flowbite modal traps focus and the drawer closes; claim panels open their sources with JavaScript and stay open without it; the glossary is anchored; the detection simulation on the methods page stays labelled as a simulation; print styles turn the artifact into a paper document; library pages are `Article` and never `MedicalWebPage`.

A browser test is also the only reliable test of "readable without JavaScript". One block creates a context with JavaScript disabled and checks that content, navigation and claim sources remain available.

The suite grew with the site: 30 tests at [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0), 72 passing at v0.5.0 according to the handover written when it shipped, and 84 in the production run for commit [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163).

## Stage 5: the same suite against production

After deployment, the `Verify production` job waits until the live site's footer contains the SHA of the commit being deployed, then runs [`npm run smoke`](../../commands/#npm-run-smoke) and [`npm run test:production`](../../commands/#npm-run-test-production). The smoke script requests every entry point, feed, preview image and first-party asset and compares status codes and `lang` attributes; the browser suite then runs unchanged against the live URL.

Running the same tests twice is not redundant. The preview is a Python HTTP server on a Linux runner; production is GitHub Pages behind a CDN, with its own headers, caching and redirects. The third failure below passed on the preview and failed on production.

## Stage 6: Rust contract tests

The JSON API is tested from a second language. [crates/caas-content/tests/contract.rs](https://github.com/korczis/catharsis-as-a-service/blob/main/crates/caas-content/tests/contract.rs) runs the exporter into a temporary directory, or reads `CAAS_API_DIR` when CI sets it to the export of the commit under test, and asserts that the typed library loads and has no integrity problems:

```rust
#[test]
fn the_exported_library_has_no_integrity_problems() {
    let problems = library().problems();
    assert!(
        problems.is_empty(),
        "integrity problems:\n{}",
        problems.join("\n")
    );
}
```

The CLI crate has its own tests that run the `caas` binary. [`cargo test --workspace`](../../commands/#cargo-test), [`cargo clippy`](../../commands/#cargo-clippy) with warnings as errors and [`cargo fmt`](../../commands/#cargo-fmt) run in the CI job `Rust`. At v0.5.0 the workspace had 21 Rust tests.

## What the checks caught on the first day

The records show three failures that matter, and each stopped at a different layer.

**A flaky print test, caught locally.** A checkpoint written at 11:09 UTC records "E2E was 36/37: print test read computed style once". A preview probe showed that the print styles did apply, so the defect was in the test, which read the computed style a single time instead of waiting for it. The test was changed to poll. Nothing was pushed with the failure.

**A Crossref title mismatch, caught in CI before deployment.** Commit [51dde0b](https://github.com/korczis/catharsis-as-a-service/commit/51dde0bb4dba09c35fb4c0a835d764a497f3c5a3) added the research library. In [run 34842607207](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842607207) the `References (Crossref)` job failed at 12:17:36 UTC with:

```text
error: lieberman-2007: title differs from Crossref (0.42): 'putting feelings into words'
```

The reference was correct; the comparison was not. The error shows that Crossref returned only the main title, while the registry held the full title with its subtitle, and the validator compared the two as they were. Deploy, verify and release were skipped. The fix, [94d734c](https://github.com/korczis/catharsis-as-a-service/commit/94d734c78ffed85a02a447051992a2acac51926d), compares the registered title and its main part against Crossref's title with and without the subtitle and keeps the best match. It was committed at 12:20:54 UTC, and [v0.3.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.3.0) was published at 12:24:28, 6 minutes 52 seconds after the failing job ended.

**A browser difference, caught in production before release.** Commit d2b3c47 added in-place previews for the concept screens. All seven CI jobs passed, including the full browser suite on the preview, and the site deployed. In [run 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250), `Verify production` then failed one of 84 tests, "concept screen preview: modified clicks keep the link to the original PNG", with a timeout while waiting for a new tab after a Ctrl or Meta click; Playwright's retry failed the same way. The `Release` job was skipped. The follow-up commit, [93fd07f](https://github.com/korczis/catharsis-as-a-service/commit/93fd07f), explains the cause: "on the Linux runner a Ctrl+click tab stayed on about:blank". It changes the test to check what the page controls (modified and middle clicks are not cancelled and do not open the dialog) rather than how a particular browser opens tabs. The next pipeline, [run 34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153), passed all ten jobs, and [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) was published at 15:43:36 UTC, 20 minutes 12 seconds after the failing verification ended.

The third case is worth dwelling on. The site was briefly live with a commit that had not passed verification, because deployment has to happen before production can be tested. The rule the project follows is about claims, not about bytes on a CDN: without a passing verify job there is no release, and nothing is reported as deployed.

## What these tests do not cover

None of these checks judge whether a sentence about psychology is right, whether an appraisal is fair, or whether the Czech reads naturally; those remain review tasks, and the handover from v0.5.0 lists a terminology review as open. The suite does not measure performance budgets, and accessibility is checked through specific behaviours (focus trapping, labels, alt text, heading order) rather than a full audit. The pipeline also has a structural blind spot: a defect that appears only on GitHub Pages is found after the site is live. The mitigation is that verification is automatic, it runs within minutes, and nothing is released until it passes.
