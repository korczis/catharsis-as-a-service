+++
title = "Time accounting: what the records measure, what an estimate suggests, and why they cannot be compared directly"
description = "An honest account of time for a site built in one day by a supervised AI agent: measured elapsed times from Git, the pipeline and the Majordomus ledger; a labelled bottom-up estimate of the same scope for a human team; and the reasons this is not a controlled comparison."
date = 2026-09-14
weight = 7

[taxonomies]
tags = ["engineering", "time", "estimation", "software delivery"]

[extra]
kicker = "Engineering 07"
kind = "technical"
summary = "The site reached its first verified release 51 minutes and 36 seconds after the repository was created, and its fifth, the scope estimated here, 3 hours 13 minutes and 4 seconds after. Eight pipeline runs used 33 minutes of wall-clock time; two failed and were recovered in 6 minutes 52 seconds and 20 minutes 12 seconds. A transparent bottom-up estimate puts the same scope, built by a human team to the same checks, at roughly 345 to 730 person-hours. The two numbers measure different things, there is no control condition, and the person's own time was not recorded. The article presents both, with their assumptions, and states what a real measurement would need."
key_points = [
  "Measured: repository created 09:54:06 UTC; v0.1.0 at 10:45:42; v0.5.0 at 13:07:10; v0.6.0 at 15:43:36. Push to verified release took between 2 min 40 s and 5 min 03 s in the six successful runs.",
  "Estimated, and labelled as such: 345–730 person-hours for the v0.5.0 scope, built from fourteen work items with stated assumptions and a 10–20% coordination overhead.",
  "No speed-up factor is claimed: elapsed agent time and human effort are different units, the quality bars differ, the human direction time is unrecorded, and a single case has no control."
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## The question and the trap

People who hear that a site like this was built in a day ask how much time that saved. It is a fair question, and an easy one to answer badly. The bad answer takes the hours on the clock, compares them with a guess of how long "a team" would take, divides, and publishes the ratio. That ratio compares a measurement with an opinion, mixes elapsed time with effort, and ignores that the two products might not be equally good.

This article separates three things and keeps them separate:

1. **Measurements** from records: the Git history, the GitHub API (repository, releases, workflow runs and their jobs) and the Majordomus ledger. Every number is linked or reproducible.
2. **An estimate**, explicitly labelled, of the effort the same scope would take a human team, built bottom-up so that every assumption can be disputed line by line.
3. **The reasons the two cannot be combined** into one factor, and what a real measurement would require.

The research note [Method: building an evidence-gated artifact with Majordomus](@/research/method-majordomus/index.md) covers the first release in detail, and the [case study](../../case-study/) shows the full timeline interactively. This article covers the whole day as recorded at 15:47 UTC.

## Part A: what the records measure

### Milestones

All times are UTC on 14 September 2026.

| Time | Event | Source |
|---|---|---|
| 09:45 | Working session begins (poster rebuild) | local file timestamps, as reported in the method note; not independently verifiable |
| 09:54:06 | Repository created on GitHub | GitHub API `created_at` |
| 10:26:23 | Majordomus initialised; first supervised task | Majordomus ledger |
| 10:45:42 | [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0): bilingual site, CI/CD, live verification | release list |
| 11:13:28 | [v0.2.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.2.0): boilerplate practices, previews, structured data | release list |
| 12:24:28 | [v0.3.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.3.0): research library, advice, command registry, Rust API | release list |
| 12:58:21 | [v0.4.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.4.0): evidence ledger, methods, glossary, status | release list |
| 13:07:10 | [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0): ledger in the API, Rust client, documentation | release list |
| 13:08:34 | Task closed as completed; no supervised task is recorded until 14:54:07 | Majordomus ledger |
| 15:43:36 | [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0): screen previews, a fix, expanded research note | release list |

Derived durations:

- repository creation to first verified release: **51 min 36 s**;
- repository creation to v0.5.0: **3 h 13 min 04 s**;
- repository creation to v0.6.0: **5 h 49 min 30 s**, a window that includes 1 h 45 min 33 s with no supervised task recorded.

Ten commits, six releases, four recorded decisions and one proposed ADR fall in that window.

### Supervised task time

The Majordomus ledger, readable with [`majordomus history`](../../commands/#majordomus-history), records when each task started and finished. Up to v0.5.0, five tasks account for **2 h 38 min 38 s**. The three tasks that ended as partial and were restarted (scope errors, described in [Supervised AI delivery](@/engineering/supervised-ai-delivery/index.md)) account for 32 min 29 s of that. Task time is when the agent was working under a declared task. It does not show how much of that time the person spent reading, deciding or typing.

### Pipeline runs

Each push to `main` starts the Pages workflow. The table lists every run that day, with wall-clock time from creation to completion, the sum of the durations of the jobs that ran (jobs run in parallel, so this is larger), and the time from the run's creation to the published release. The data can be listed with [`gh run list`](../../commands/#gh-run-list).

| Run | Commit | Result | Wall clock | Job time | Push to release |
|---|---|---|---|---|---|
| [34834554169](https://github.com/korczis/catharsis-as-a-service/actions/runs/34834554169) | 9bc6897 | success | 2:43 | 3:02 | 2:40 (v0.1.0) |
| [34836842423](https://github.com/korczis/catharsis-as-a-service/actions/runs/34836842423) | 54a31a2 | success | 3:06 | 3:24 | 3:02 (v0.2.0) |
| [34842607207](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842607207) | 51dde0b | failure: references | 1:29 | 3:03 | none |
| [34842946706](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842946706) | 94d734c | success | 3:25 | 4:57 | 3:21 (v0.3.0) |
| [34845982889](https://github.com/korczis/catharsis-as-a-service/actions/runs/34845982889) | 4cbb6fb | success | 4:17 | 6:01 | 4:14 (v0.4.0) |
| [34846771284](https://github.com/korczis/catharsis-as-a-service/actions/runs/34846771284) | f2890f4 | success | 5:02 | 6:46 | 4:59 (v0.5.0) |
| [34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250) | d2b3c47 | failure: verify production | 8:01 | 8:44 | none |
| [34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153) | 2125f1e | success | 5:07 | 6:15 | 5:03 (v0.6.0) |
| **Total** | | 6 passed, 2 failed | **33:10** | **42:12** | |

The pipeline grew from seven jobs to ten when the Python, Rust and Crossref jobs were added with the research library, and the browser suite grew from 30 to 85 tests, so later runs are longer. The weekly evidence workflow was also run once by hand (38 seconds).

### Failures and recovery

| Failure | Detected | Fix committed | Verified release | Detection to release |
|---|---|---|---|---|
| Crossref title comparison ([details](@/engineering/testing-a-static-site/index.md)) | 12:17:36 | 12:20:54 | 12:24:28 (v0.3.0) | 6 min 52 s |
| Modified-click test on production | 15:23:24 | 15:37:52 | 15:43:36 (v0.6.0) | 20 min 12 s |

Neither failure reached a release. The second left an unverified commit on the live site for about twenty minutes, because production can only be tested after deployment.

### What the measurements do not include

- Planning, thinking and prompt writing before the first recorded file.
- The person's time. No record shows when the person was reading, deciding or away; the only bound is the window itself.
- Time after the records were read: the review items the v0.5.0 handover leaves open (accepting ADR-0001, reviewing flagged Czech glossary terms), and any rework they cause.
- Model usage and its cost, which are not part of the repository's records.

## Part B: an estimate for a human team

**This section is an estimate, not a measurement.** It asks how many person-hours an experienced team (a web developer, a technical writer with a psychology background, a Czech editor, and part-time DevOps and Rust engineers) would need to produce the scope of [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0), to the same automated checks, starting from a finished poster. v0.5.0 is used because its scope can be measured from the tagged tree and it closed a supervised task; later work is excluded from both sides.

The scope column was measured from the repository at commit [f2890f4](https://github.com/korczis/catharsis-as-a-service/commit/f2890f4fa20f0f92db790477b1460c2e774bbe44). Word counts exclude front matter. The hour ranges are the author's judgement, and the assumptions say where each comes from. Readers who disagree with a rate can recompute that row.

| # | Work item | Scope at v0.5.0 (measured) | Assumption behind the range | Low (h) | High (h) |
|---|---|---|---|---|---|
| 1 | English content with sources read | 32 English files, about 19,300 words; 10 research notes, 10 advice entries | 150–300 words per hour including reading abstracts and checking wording against sources | 65 | 130 |
| 2 | Czech edition | 32 Czech files, about 17,100 words | 250–375 words per hour for professional adaptation with psychological terminology | 45 | 70 |
| 3 | Source appraisals | 58 references, each graded with a bilingual appraisal | 0.5–1 h per source: locate abstract, classify design, write both languages | 29 | 58 |
| 4 | Claims ledger | 50 claims with scope, caveat and dates in two languages | 15–30 min per claim once sources are appraised | 13 | 25 |
| 5 | Glossary | 54 bilingual terms with cross-references | 9–18 min per term | 8 | 16 |
| 6 | Design system, templates and components | 2,053 template lines, 2,472 CSS lines, two locales | a senior front-end developer at roughly 50–100 finished lines per hour including responsive and accessibility work | 40 | 80 |
| 7 | Interaction | Alpine and Flowbite integration, 381 lines of site JavaScript, no-JS fallbacks | small code, high testing and accessibility cost | 12 | 24 |
| 8 | Metadata and SEO | JSON-LD, localized previews, feeds, sitemap alternates | known patterns, per-locale verification | 8 | 16 |
| 9 | Validators and API exporter | 1,601 lines of Python and shell in the scripts directory | 35–65 lines per hour for tested tooling | 24 | 48 |
| 10 | Test suites | 40 pytest tests with fixtures; 23 Playwright blocks executing 72 tests | fixtures and browser flakiness dominate | 24 | 48 |
| 11 | Rust crate and CLI | 1,182 lines, 21 tests | typed contract plus CLI and contract tests | 16 | 32 |
| 12 | CI/CD and repository settings | three workflows and a composite action (352 lines), release script, rulesets, Pages | includes debugging live deployment | 12 | 24 |
| 13 | Supervision layer, rules, ADR, documentation | 6 project rules, 1 ADR, 5 documents, README | writing and wiring, not tool development | 10 | 20 |
| 14 | Artwork production pipeline | poster render script, icon set, localized preview cards | excludes the artistic concept | 8 | 16 |
| | **Subtotal** | | | **314** | **607** |
| | Coordination, review and integration | | 10–20% of the subtotal for a team of four to five people | 31 | 121 |
| | **Estimated total** | | | **≈ 345** | **≈ 730** |

At 40 hours a week that is roughly 9 to 18 person-weeks. The range is wide on purpose. The largest items, content and appraisals, depend on how carefully sources are read, and that is also where a human expert might produce a different and possibly better product.

Several judgements pull the estimate in opposite directions:

- **Towards lower:** an experienced team with a reusable Zola starter, an existing validator library or a translation memory would be faster on rows 6, 8, 9 and 2. Some items might not be built at all without an agent doing them cheaply (a second-language contract test, an executed command registry), and a team would be right to skip them.
- **Towards higher:** the ranges assume little rework. The agent's own records show rework (three task restarts, two pipeline failures, a flaky print test), and a human team would have its own. Bilingual review cycles, stakeholder feedback and waiting between people are not in the table.

## Part C: why these numbers cannot be divided

It is tempting to set 3 h 13 min against 345–730 person-hours and state a factor. This article does not, for five reasons.

**1. Different units.** Elapsed time is wall-clock time during which an agent, and sometimes several at once, worked while a person directed and reviewed. Person-hours are effort summed across people. Parallel human work would shorten the calendar time of the estimate without changing its hours, and parallel agents do the same to the measurement.

**2. No control condition.** There was one project, built once. There is no human team that built the same scope, no second agent session without supervision, and no repeat. A single case can show that something is possible. It cannot show how large an effect is.

**3. The quality bar is not demonstrably equal.** The estimate assumes the human team meets the same automated checks, and automated checks are not the whole of quality. The ledger records that source designs were checked against published abstracts and that two sources without a retrievable abstract are marked unverified. A human expert reading full texts would take longer and might grade differently. The Czech terminology review and the ADR acceptance are still open. Where the agent's product is weaker, the comparison flatters it; where it is more thorough than a team would bother to be (every command executed in a test), the comparison penalises it.

**4. Human direction time is unrecorded.** The person wrote briefs, expanded scope, chose between options and reviewed output. None of that is timed. If the person attended the whole window, their effort is bounded by it; if not, it is smaller. Either way it belongs in the comparison and is missing.

**5. The estimator is not independent.** The estimate was written after the fact by an AI agent of the same kind that did the work, with knowledge of the result. Anchoring on the known outcome is a plausible bias in either direction. Line counts and word counts are also weak proxies for effort: a 17-line vendoring script and a 255-line validator do not cost in proportion to their length.

What the records do support is narrower. The scope of v0.5.0, measured above, reached a verified release about three hours after the repository was created. Every release in the window passed the same automated checks, and the two failures were caught by those checks and recovered within minutes. Against any plausible reading of the estimate table, that is a large difference in elapsed time. How large, in a sense that would survive scrutiny, is not something one uncontrolled case can say.

## What a real measurement would need

A defensible comparison of supervised AI delivery with conventional delivery would need at least:

1. **A fixed, pre-registered scope and acceptance gate.** The same brief, and the same validation script and test suite as the definition of done, agreed before any work starts.
2. **Comparison arms.** A human team, an agent directed by a person without supervision tooling, and an agent with supervision, ideally on several projects of different kinds, with arms assigned so that the same person does not direct two arms of the same project.
3. **Effort, not just elapsed time.** Time tracking of human attention (direction, review, waiting) in every arm, and agent compute time and cost alongside.
4. **Blind quality assessment.** Independent experts rating samples of content (accuracy of claims against sources, appropriateness of grades, quality of the Czech) without knowing which arm produced them, plus an accessibility audit.
5. **Outcomes after release.** Defects found in the weeks after release, review dates missed, and the cost of the first substantial change, since maintainability is where hurried work usually charges its bill.

Until then, the honest summary is the pair of numbers with their labels: a measured three hours and thirteen minutes to a verified v0.5.0, and an estimated 345 to 730 person-hours for a human team to build the same scope, which are not the same kind of number.
