+++
title = "Supervised AI delivery: briefs, scoped tasks, hooks, CI and live verification"
description = "How one person directed an AI coding agent under Majordomus supervision: the kinds of instructions, scoped tasks, commit and push hooks, the pipeline, live verification and releases, and a record-based account of who did what."
date = 2026-09-14
weight = 2

[taxonomies]
tags = ["engineering", "majordomus", "ai agents", "software delivery"]

[extra]
kicker = "Engineering 02"
kind = "technical"
summary = "The site was written by an AI coding agent. The person directing it did not write code; they set goals, expanded scope, chose between options and held the right to accept decisions. Majordomus sat between the agent and the repository: every change ran as a scoped task, commits and pushes passed hooks, and a task could be closed as completed only when a verification command against the live site succeeded. This article reconstructs that loop from the records."
key_points = [
  "Six supervised tasks are recorded on 14 September 2026; three were closed as partial and restarted, two as completed, and one was still active at the time of writing.",
  "Hooks run a health check on every commit and the finish contract on every push; the pipeline repeats the supervision check in CI before anything deploys.",
  "The person set scope and accepted decisions; the agent implemented, tested, recorded decisions and proposed an architecture decision record that still awaits human acceptance.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## The claim this article makes, and the one it does not

This site was produced by an AI coding agent (Claude Code) directed by one person, with [Majordomus](https://majordomus.dev) as a supervisory layer. That sentence invites two readings. One is "the AI built a website", which hides the work the person did and the constraints that made the output usable. The other is "the AI only typed", which hides how much of the design was the agent's. The records support neither. This article describes the loop that actually ran, using the Git history, the Majordomus ledger and the GitHub Actions runs as sources.

The [case study](../../case-study/) presents the same records as an interactive timeline. The research note [Method: building an evidence-gated artifact with Majordomus](@/research/method-majordomus/index.md) covers the first release in detail. Here the focus is the mechanism: how a brief becomes a verified release, and where each safeguard sits.

## Instructions: from a one-line request to a completion gate

The method note classifies the person's messages during the first phases into five kinds: a one-line request to create the project; art direction for the poster, with a choice between offered approaches; three structured execution briefs of increasing scope; short directives during the work ("deploy", "validate in a browser", "release automatically", "use Majordomus and enforce it"); and editorial direction, such as replacing promotional copy with sourced psychology.

The briefs are the interesting part. They did not specify templates or test cases. They specified outcomes, constraints and, crucially, **what counts as done**: numbered requirements and an explicit completion gate. That shape matters for an agent, because an agent will otherwise report completion when the code is written. A gate of the form "deployed, verified against the live URL, released" turns completion into something a machine can check.

Scope also changed during the work, and the records say so. A checkpoint written at 11:09 UTC notes: "User scope expanded mid-task: landing explainer of catharsis, research essays with citations, advice library, tags, illustrations, per-page previews, Majordomus method page with real timeline, Rust integration, command registry with links and test coverage, pytest, JS coverage, docs." The agent's response was not to absorb the expansion into the running task but to close the task, hand over, and start a new one whose scope covered the new paths.

## Scoped tasks

Every change ran as a Majordomus task started with [`majordomus start`](../../commands/#majordomus-start) and a list of paths the work may touch. The ledger, which [`majordomus history`](../../commands/#majordomus-history) prints, records six tasks on 14 September 2026:

| Task | Started (UTC) | Closed (UTC) | Outcome | Why it ended |
|---|---|---|---|---|
| Ship the site with CI/CD | 10:26:23 | 10:29:16 | partial | files moved outside the declared scope; restarted |
| Ship the site (scope `.`) | 10:29:16 | 10:39:39 | partial | `.` was not read as the whole repository; restarted |
| Ship the site | 10:39:39 | 10:47:25 | completed | v0.1.0 deployed, verified and released |
| Boilerplate, previews, structured data | 10:50:57 | 11:10:10 | partial | new top-level paths planned; restarted with a wider scope |
| Evidence-based library, Rust, registry | 11:10:11 | 13:08:34 | completed | v0.5.0 deployed, verified and released |
| Extend the site | 14:54:07 | — | active | open at the time of writing |

Three of six tasks ended as partial, and each ended for the same kind of reason: the declared scope no longer matched the work. That is the intended behaviour. [`majordomus watch`](../../commands/#majordomus-watch) and [`majordomus check`](../../commands/#majordomus-check) report drift between the task and the files that changed; the handover written at 10:29 UTC states the problem plainly ("The first task scope omitted the pre-existing root files that were moved into artwork/ and static/ … so watch reports scope drift") and the next action ("Restart the task with a scope covering the whole repository").

One caveat about sources. The Majordomus ledger, checkpoints, handovers and decision log live under `.ai/local/`, which by policy is never committed. The quotations from them in this article are from the working copy on which the site was built; the public, independently checkable records are the Git history, the Actions runs and the releases linked throughout.

Restarting is cheap because state is externalised. Before closing a task, the agent writes a handover with [`majordomus handover`](../../commands/#majordomus-handover), which has three required headings: Objective, Current State and Next Action. Progress notes go through [`majordomus checkpoint`](../../commands/#majordomus-checkpoint). The next task begins from those records rather than from the agent's memory of the conversation, which is what makes the restart take seconds. The three partial tasks cost 2 minutes 53 seconds, 10 minutes 23 seconds and 19 minutes 13 seconds of recorded task time, and none of them pushed anything.

## Decisions are records, not chat

Choices with lasting consequences were recorded with [`majordomus decision`](../../commands/#majordomus-decision). The ledger holds four decision events that day: structured data built as Tera data and serialised with `json_encode`; link previews localized per language with every edition in the sitemap; Python validators tested with pytest in a project virtual environment; and the evidence ledger design. Each entry in the decision record has the same fields:

```text
Why: Hand-written JSON-LD inside HTML templates gets HTML-escaped and breaks on quotes;
     building the graph as template maps keeps escaping correct by construction
Rejected: hand-written JSON-LD strings; a client-side script injecting JSON-LD
Evidence: templates/partials/structured-data.html; scripts/validate-html.py parses every JSON-LD block
```

The largest decision became an architecture decision record, [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md), "Evidence ledger with dated review for every public claim". Its status is `proposed`. The handover written when v0.5.0 shipped lists acceptance as the first next action for a person: "Accept or amend ADR-0001." The agent can propose architecture; accepting it is left to the human.

## Hooks: the checks nobody has to remember

Three Git hooks live in `.githooks/`, and [`npm ci`](../../commands/#npm-ci) points Git at them through the `prepare` script in `package.json`:

- **commit-msg** runs [`scripts/lint-commits.sh`](../../commands/#lint-commits) on the message. Conventional Commits are not a style preference here: the release version is computed from them.
- **pre-commit** requires Majordomus and runs its health check:

```sh
majordomus doctor || exit $?
```

- **pre-push** runs the finish contract in check mode, so a push is refused while the active task would not be allowed to finish:

```sh
majordomus finish --check || exit $?
```

[`majordomus doctor`](../../commands/#majordomus-doctor) earned its place before the first commit: it reported that the README did not link the agent bootstrap file, and the defect was fixed locally. [`majordomus finish`](../../commands/#majordomus-finish) is the contract that makes "completed" mean something. The task that shipped v0.1.0 was closed with the live smoke test as its verification command; the contract result in the ledger records each rule it evaluated (`scope-integrity: pass`, `blocker-resolution: pass` and so on).

Hooks can be skipped locally, so CI repeats the check. The `Majordomus supervision` job installs a pinned Majordomus release, verifies its SHA-256 through the installer, and runs the health check on the pushed tree. A repository ruleset names that job, together with commit linting, validation and the end-to-end suite, as required checks for `main`. The ruleset allows the repository administrator to bypass it, and the checkpoint after the first push records that the bypass was used: direct pushes to `main` are how this pipeline starts. The protection that does not depend on the ruleset is the order of the pipeline itself, which will not deploy a commit whose CI failed.

## CI, deployment and live verification

The pipeline is described in [How the site was built](@/engineering/how-the-site-was-built/index.md); what matters for supervision is its order. `pages.yml` runs CI, then deploys the exact artifact CI validated, then verifies production, then releases. The project rule [project.verified-deployment](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/verified-deployment.v1.md) states the reporting standard: "A deployment is complete only when the Pages workflow's verify job has passed against the live URL returned by GitHub, and a release is cut only after that job."

This is a rule for the agent's reports as much as for the pipeline. An agent that watches a green build and says "deployed" is wrong in a way that is hard to notice. Here the agent watched the run with [`gh run list`](../../commands/#gh-run-list), and the checkpoint written after the first push says what it was waiting for: "Pages run 34834554169 triggered (ci -> deploy -> verify -> release); watching it now." Its next steps were to investigate any failing job, run the smoke test and the browser suite against the live URL, confirm the release tag, and only then finish the task with a live verification command.

The records also show the rule holding when something failed. [Run 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250), for commit [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163), passed all seven CI jobs and deployed, but one of 84 browser tests failed against production. The `Release` job was skipped, and under the rule above that commit did not count as deployed. It was released only in [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) at 15:43:36 UTC, after a fix had passed verification in [run 34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153).

## Releases

A release is the last job and has no manual step. [scripts/release.sh](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/release.sh) finds the last `v*` tag, reads commit subjects since then, bumps minor for `feat`, patch otherwise (breaking changes bump minor while the version is 0.x), and publishes notes that name the live URL and the pipeline run. Tags are protected by a ruleset that forbids deleting, moving or updating them, and `main` forbids force pushes. Six releases were published on 14 September 2026 by the time of writing, from [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0) at 10:45:42 UTC to [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) at 15:43:36 UTC.

## Who did what

Attributing work in a human–agent session is easy to get wrong, so this list stays with what the records show.

**The person** created the direction and the boundaries: the project itself, the art direction, the briefs and their completion gates, the mid-task scope expansions recorded in checkpoints, the instruction to make supervision mandatory, and editorial standards for the psychology. The person owns the decisions still open in the handover: accepting ADR-0001 and reviewing Czech glossary terms that the agent flagged as non-standard. The time the person spent reading, thinking and reviewing is not recorded anywhere, which matters for [Time accounting](@/engineering/time-accounting/index.md).

**The agent** wrote the code, templates, content drafts in both languages, validators, tests, workflows and documentation; chose the implementation (Tera components, the ledger schema, the test strategy); configured the repository rulesets; ran every command; recorded checkpoints, handovers and decisions; and proposed the ADR. Commits carry a `Co-Authored-By` trailer naming the model and a `Claude-Session` trailer naming the session.

**Majordomus** wrote nothing. It refused, recorded and reported: scope drift, a malformed scope, a missing bootstrap link, and the finish contract. **The pipeline** refused twice that day: once before deployment (a reference title mismatch against Crossref) and once before release (a failing production test).

## What this does not show

The records show a sequence of checked steps, not that supervision made the work faster or better than an unsupervised session would have been. There was no second session to compare with. The agent also made errors that the supervision layer did not catch and the pipeline did; those are listed in [Testing a static site](@/engineering/testing-a-static-site/index.md). What the records do support is narrower and still useful: every "done" in this repository is attached to a command, an exit code and a timestamp that a reader can check.
