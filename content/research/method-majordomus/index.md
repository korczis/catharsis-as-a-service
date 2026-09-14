+++
title = "Method: building an evidence-gated artifact with Majordomus"
description = "How this site was built by an AI coding agent under Majordomus supervision: the measured timeline of the first release, the kinds of instructions given, what the supervision layer caught, and what cannot be claimed."
date = 2026-09-14
weight = 6

[taxonomies]
tags = ["method", "majordomus", "verification", "software delivery"]

[extra]
kicker = "Research note 06"
kind = "technical"
summary = "The site went from an empty GitHub repository to a verified release in 51 minutes and 36 seconds, and from Majordomus initialisation to that release in 19 minutes and 19 seconds. This note reports the recorded timeline, the types of instructions that drove the work, the findings Majordomus raised before anything was pushed, and the limits of any claim about speed."
key_points = [
  "Measured from the repository and pipeline records: repository created 09:54:06 UTC, first release v0.1.0 verified and published 10:45:42 UTC on 14 September 2026.",
  "Majordomus reported two scope errors and one bootstrap failure before the first push; the first deployment pipeline passed all seven jobs.",
  "No control condition exists, so no speed-up factor is claimed; the records show where time was not lost and make every completion claim checkable.",
]
figures = [
  { kind = "screens", id = "majordomus-cockpit", caption = "Concept screens of a Majordomus cockpit: views over sessions, rules, worktrees, issues, tests, documentation, milestones and model usage. All names, numbers and dates in them are illustrative and do not describe this project; its real records are the timeline in this note.", items = [
    { src = "assets/majordomus/cockpit-sessions.png", title = "Sessions", alt = "Concept screen of the Majordomus cockpit Sessions view: a list of working sessions and the timeline of one session from start to updated documentation, with the context sources it loaded.", caption = "Each session keeps its timeline, context sources, decisions and handover." },
    { src = "assets/majordomus/cockpit-rules.png", title = "Rules", alt = "Concept screen of the Majordomus cockpit Rules view: a list of enforced repository rules with coverage, the detail of one rule, its validation status and where it is enforced.", caption = "Executable rules with their enforcement points: command line, CI, pre-commit hook." },
    { src = "assets/majordomus/cockpit-worktrees.png", title = "Worktrees", alt = "Concept screen of the Majordomus cockpit Worktrees view: parallel branches with their status, a diff of changed files, commits ahead and a terminal.", caption = "Parallel branches in their own worktrees, each tied to an issue and a session." },
    { src = "assets/majordomus/cockpit-issues.png", title = "Issues", alt = "Concept screen of the Majordomus cockpit Issues view: an issue list and the detail of one issue with its linked worktree, session, pull request, tests and documentation.", caption = "An issue connected to the work that implements and verifies it." },
    { src = "assets/majordomus/cockpit-tests.png", title = "Tests", alt = "Concept screen of the Majordomus cockpit Tests view: pass and fail counts, a results trend, coverage, quality gates and live test output.", caption = "Test runs, failures and quality gates in one place, linked to issues and commits." },
    { src = "assets/majordomus/cockpit-docs.png", title = "Documentation", alt = "Concept screen of the Majordomus cockpit Documentation view: a document tree and an architecture decision record with context, decision and consequences.", caption = "Documentation and architecture decisions next to the rules they implement." },
    { src = "assets/majordomus/cockpit-milestones.png", title = "Milestones", alt = "Concept screen of the Majordomus cockpit Milestones view: three milestones with progress bars, a cumulative progress chart, a timeline and dependencies.", caption = "Milestones with progress, schedule and dependencies derived from the issue plan." },
    { src = "assets/majordomus/cockpit-models.png", title = "Models", alt = "Concept screen of the Majordomus cockpit Models view: AI model providers with usage, latency, cost breakdown and live requests.", caption = "Which models were used for what, at what latency and cost." },
  ] },
]
references = ["majordomus-2026", "repository-2026"]
+++

## What was built

The site is a bilingual static publication generated with Zola, deployed to GitHub Pages and verified against the live URL on every change. It was produced in a single working session by an AI coding agent (Claude Code) directed by one person, with [Majordomus](https://majordomus.dev) as the supervisory layer between the agent and the repository.

This note documents that process with the same standard the research notes apply to psychology: report what was measured, separate it from interpretation, and state what cannot be concluded.

## The recorded timeline of the first release

All times are UTC on 14 September 2026 and come from the Git history, the GitHub API, the Majordomus ledger and the pipeline records.

| Time | Event | Source |
|---|---|---|
| 09:45 | Working session begins with the poster rebuild | local file timestamps |
| 09:54:06 | GitHub repository created; poster committed | GitHub API, Git |
| 10:26:23 | Majordomus layer initialised; first supervised task started | Majordomus ledger |
| 10:29:16 | Scope drift reported after files were moved; task restarted | Majordomus ledger |
| 10:39:39 | A malformed scope reported by the pre-push check; task restarted before any push | Majordomus ledger |
| 10:42:45 | Site committed; the pre-commit hook ran the Majordomus health check with zero failures | Git, hook output |
| 10:43:02–10:45:45 | Pages pipeline: 7 jobs, 2 minutes 43 seconds, all passed | GitHub Actions |
| 10:45:42 | Release v0.1.0 published after live verification | GitHub API |
| 10:47:25 | Task closed as completed; verification command was the live smoke test (exit 0, 7 seconds) | Majordomus ledger |

Derived durations:

- repository creation to first verified release: **51 min 36 s**
- Majordomus initialisation to first verified release: **19 min 19 s**
- push to verified release: **2 min 57 s**

At that release the site was checked by 7 validation stages and 30 browser tests. Later phases (link previews and structured data, then this research library and the advice library) followed the same loop and are visible in the repository's release history.

## The kinds of instructions

The work was driven by about fifteen messages from one person. They fell into five types:

1. **A one-line request** to create a project on GitHub.
2. **Art direction** for the poster, followed by a choice between three offered approaches.
3. **Structured execution briefs.** Three long specifications of increasing scope: a static artwork page, an interactive microsite, and a multilingual publishing system with dozens of numbered requirements and an explicit completion gate.
4. **Short directives during work:** deploy, validate in a browser, release automatically, use Majordomus and enforce it.
5. **Editorial direction:** apply HTML5 Boilerplate practices, improve link previews and search visibility, and replace promotional copy with serious, sourced psychology.

None of these messages specified implementation details such as template syntax or test cases. Those were decisions of the agent, and the supervision layer's job was to keep them checkable.

## What Majordomus contributed

Majordomus did not write code. It constrained and recorded the work:

- **Scoped tasks.** Every change ran as a task with declared paths. When files were moved outside that scope, [`majordomus watch`](../../commands/#majordomus-watch) reported drift, and the task was restarted with a correct scope. When a later scope was malformed, [`majordomus check`](../../commands/#majordomus-check) reported every file as out of scope before the push, which would otherwise have been refused by the pre-push hook.
- **A health check on every commit.** [`majordomus doctor`](../../commands/#majordomus-doctor) runs in the pre-commit hook. Before the first commit it reported that the README did not link the agent bootstrap file; the defect was fixed before it reached the repository.
- **A finish contract.** [`majordomus finish`](../../commands/#majordomus-finish) refuses to close a task as completed unless its verification command passes. For this site that command is the live smoke test, so "completed" means "deployed and checked", not "written".
- **Continuity.** Checkpoints and handovers recorded the current state and the next action whenever a task was restarted, so each restart took seconds and depended on recorded facts rather than on the agent's memory.
- **Rules in the repository.** Project rules such as "no deployment claim without live verification" live in `.ai/repo/rules/`, next to the code they govern.

## Did it make development faster?

The honest answer is that no speed-up factor can be stated. There was one session and no comparable session without supervision, so there is no control condition.

What the records do show is where time was not lost. No push was rejected by CI, no deployment had to be rolled back, and the first pipeline run passed all seven jobs. Three defects (two scope errors and a documentation bootstrap failure) became local findings instead of failed pipeline runs. Each would have cost at least one additional push-and-wait cycle of several minutes, and a failed deployment would have cost more.

The larger effect is on confidence rather than raw speed. Every "done" in this project is backed by a recorded command and its exit code, which a reader can check with [`majordomus history`](../../commands/#majordomus-history) in the repository.

## Limits of this account

- The timeline starts at the first recorded file; planning that happened before it is not included.
- Durations depend on the tools, the hardware and network latency of this session.
- The session also relied on conventional safeguards unrelated to Majordomus, including local validation, browser tests and continuous integration. Their effects are not separated here.
