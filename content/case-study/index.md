+++
title = "Case study: AI-assisted delivery under a supervisory control layer"
description = "A tech demo of how Majordomus supervised an AI coding agent building this site: task lifecycle, enforcement wiring, rules, decisions, what supervision caught and the recorded evidence of delivery, failures included."
date = 2026-09-14
template = "case-study.html"

[taxonomies]
tags = ["majordomus", "case study", "verification", "software delivery"]

[extra]
kicker = "Case study · Majordomus"
badge = "Tech demo · case study"
summary = "One person directed an AI coding agent that built this bilingual site on 14 September 2026 under Majordomus 0.6.0. From the ledger, Git and GitHub records, this case study shows how the supervisory layer was configured and used, what it caught, what it cost and what it does not check."
key_points = [
  "Measured, not estimated: 51 min 37 s from the first commit to the verified release v0.1.0, and 19 min 19 s from Majordomus initialisation to that release. No speed-up factor is claimed, because nothing was compared against a control.",
  "Supervision surfaced three scope problems locally, one of them a malformed scope before the first push. Separately, CI stopped one deployment on a reference check and one release on a failed production test.",
  "A task was recorded as completed only after the live smoke test passed. Majordomus lists the six project rules, but the project's validators, CI and review enforce them.",
]
references = ["majordomus-2026", "repository-2026"]
limits = [
  "One session, one person, one agent. There is no control condition, so no speed-up factor can be derived.",
  "The ledger stores accepted operations. A refused command leaves no ledger entry, so friction is undercounted.",
  "Majordomus does not judge content: evidence grading, medical wording and test adequacy belong to the project's validators, CI and a reviewer.",
  "The six project rules carry no x-majordomus block. Majordomus resolves and lists them but does not enforce them.",
  "The worker chooses the verification command. The contract checks that it ran and exited 0, not that it was the right check.",
  "Parallel workers in one checkout share one active task, so attribution between them comes from their instructions and from Git, not from Majordomus.",
  "Live verification needs a deployment, so a failed verify job leaves an unverified build online until the next run.",
  "The snapshot is curated: prompts, checkpoint bodies and local paths are not published, and a person's time spent reading and deciding is recorded nowhere.",
]
links = [
  { label = "majordomus.dev", url = "https://majordomus.dev" },
  { label = "Repository", url = "https://github.com/korczis/catharsis-as-a-service" },
  { label = "The .ai/ layer on GitHub", url = "https://github.com/korczis/catharsis-as-a-service/tree/main/.ai" },
  { label = "Releases", url = "https://github.com/korczis/catharsis-as-a-service/releases" },
  { label = "Pages workflow runs", url = "https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml" },
  { label = "Snapshot format (docs/CASE-STUDY.md)", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md" },
]

[extra.ui]
metrics_heading = "Recorded numbers"
metric_tasks = "Supervised tasks"
metric_checkpoints = "Checkpoints"
metric_handovers = "Handovers"
metric_decisions = "Decisions"
metric_findings = "Findings"
metric_commits = "Commits"
metric_pipelines = "Pipeline runs"
metric_releases = "Releases"
metric_first_release = "First commit to first verified release"
metric_first_release_note = "14 September 2026,"
metric_supervised = "from Majordomus initialisation:"
snapshot_prefix = "Snapshot of the records through"
lifecycle_heading = "The task lifecycle"
lifecycle_intro = "Select a step to see its registered command, why it exists and a real recorded example. Every step has its own address, so a link opens it directly."
command = "Command"
what = "What it does"
why = "Why"
example = "Recorded example"
timeline_heading = "Timeline"
timeline_intro = "Every recorded event, oldest first: Majordomus tasks, checkpoints, handovers, decisions and finishes, the findings derived from them, commits, pipeline runs and releases. Open an event for its detail and links. Filters are kept in the address, so a filtered view can be bookmarked."
filter_label = "Filter by kind"
filter_all = "All"
search_label = "Search"
search_placeholder = "scope, smoke, v0.3.0 …"
reset = "Reset"
events_label = "events"
no_results = "No event matches these filters."
permalink = "Link to this event"
record_language_note = "Original record in English."
kind_task = "Task"
kind_checkpoint = "Checkpoint"
kind_handover = "Handover"
kind_decision = "Decision"
kind_finish = "Finish"
kind_finding = "Finding"
kind_commit = "Commit"
kind_pipeline = "Pipeline"
kind_release = "Release"
features_heading = "Majordomus features used"
feature = "Feature"
how_used = "How it was used"
evidence = "Evidence"
wiring_heading = "Enforcement wiring"
wiring_intro = "Where each check runs, what it runs and what it stops. Only the two hook entries are declared in the Majordomus policy; the rest are conventional safeguards of the same repository."
where = "Where"
effect = "Effect"
file = "File"
findings_heading = "What supervision caught"
findings_intro = "Generated from the records: a finding is published only when the ledger, a handover, a checkpoint or pipeline data confirms it. Each card links to its evidence in the timeline."
caught_by = "Caught by"
no_catcher = "recorded, not enforced by a command"
evidence_events = "Evidence"
limits_heading = "Limits"
screens_heading = "Concept screens"
screens_disclaimer = "These screens are concepts of a Majordomus cockpit with illustrative data. They do not show this project; its real records are the timeline and the numbers above."
engineering_heading = "Read the engineering articles"
engineering_text = "The engineering section explains how the rest of the site was built and tested. Estimates of time saved, with every assumption labelled, are in the time accounting article; this case study reports measured durations only."
engineering_section = "Engineering articles"
engineering_time = "Time accounting"
sources_heading = "Sources and links"

[extra.screens]
id = "case-cockpit"
caption = "Concept screens of a Majordomus cockpit: sessions, rules, worktrees, issues, tests, documentation, milestones and model usage. All names, numbers and dates in them are illustrative."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-sessions.png"
title = "Sessions"
alt = "Concept screen of the Majordomus cockpit Sessions view: a list of working sessions and the timeline of one session from start to updated documentation, with the context sources it loaded."
caption = "Each session keeps its timeline, context sources, decisions and handover."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-rules.png"
title = "Rules"
alt = "Concept screen of the Majordomus cockpit Rules view: a list of enforced repository rules with coverage, the detail of one rule, its validation status and where it is enforced."
caption = "Executable rules with their enforcement points: command line, CI, pre-commit hook."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-worktrees.png"
title = "Worktrees"
alt = "Concept screen of the Majordomus cockpit Worktrees view: parallel branches with their status, a diff of changed files, commits ahead and a terminal."
caption = "Parallel branches in their own worktrees, each tied to an issue and a session."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-issues.png"
title = "Issues"
alt = "Concept screen of the Majordomus cockpit Issues view: an issue list and the detail of one issue with its linked worktree, session, pull request, tests and documentation."
caption = "An issue connected to the work that implements and verifies it."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-tests.png"
title = "Tests"
alt = "Concept screen of the Majordomus cockpit Tests view: pass and fail counts, a results trend, coverage, quality gates and live test output."
caption = "Test runs, failures and quality gates in one place, linked to issues and commits."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-docs.png"
title = "Documentation"
alt = "Concept screen of the Majordomus cockpit Documentation view: a document tree and an architecture decision record with context, decision and consequences."
caption = "Documentation and architecture decisions next to the rules they implement."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-milestones.png"
title = "Milestones"
alt = "Concept screen of the Majordomus cockpit Milestones view: three milestones with progress bars, a cumulative progress chart, a timeline and dependencies."
caption = "Milestones with progress, schedule and dependencies derived from the issue plan."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-models.png"
title = "Models"
alt = "Concept screen of the Majordomus cockpit Models view: AI model providers with usage, latency, cost breakdown and live requests."
caption = "Which models were used for what, at what latency and cost."

[[extra.lifecycle]]
id = "start"
name = "Start with a scope"
command_id = "majordomus-start"
what = "Opens the checkout's single active task with a title, a profile and the paths the work may touch."
why = "A scope turns what the agent was asked to change into a list a tool can compare with the working tree."
example_event = "t-20260914103939-7b10-start"

[[extra.lifecycle]]
id = "check"
name = "Check"
command_id = "majordomus-check"
what = "Reports, without writing anything, whether the task is consistent with the policy, its scope and the recorded state."
why = "Problems show up on the machine, before a push or a pipeline run."
example_event = "finding-malformed-scope"

[[extra.lifecycle]]
id = "watch"
name = "Watch for drift"
command_id = "majordomus-watch"
what = "Reports drift between the recorded task, its scope, the policy and the generated instruction files."
why = "Moving or adding files changes what a task touches, often without anyone deciding it."
example_event = "finding-scope-drift"

[[extra.lifecycle]]
id = "checkpoint"
name = "Checkpoint"
command_id = "majordomus-checkpoint"
what = "Records a short progress note of at most 40 lines, or derives one from Git."
why = "Progress lives in a file instead of in the agent's conversation."
example_event = "checkpoint-20260914t104327z"

[[extra.lifecycle]]
id = "decision"
name = "Record decisions"
command_id = "majordomus-decision"
what = "Appends a dated decision with its rationale, the rejected alternatives and the evidence."
why = "The next worker can see why something is the way it is, and a person can promote the decision to an ADR."
example_event = "decision-1"

[[extra.lifecycle]]
id = "handover"
name = "Hand over"
command_id = "majordomus-handover"
what = "Writes a continuation record with Objective, Current State and Next Action; branch, commit and changed files come from Git."
why = "Any outcome other than completed has to say what comes next, so a restart depends on recorded facts."
example_event = "handover-20260914t111009z"

[[extra.lifecycle]]
id = "finish"
name = "Finish with verification"
command_id = "majordomus-finish"
what = "Evaluates the finish contract. Completed requires a verification command that exits 0, recorded with its exit code and duration."
why = "Done means the live site passed a check, not that code was written."
example_event = "t-20260914103939-7b10-finish"

[[extra.lifecycle]]
id = "history"
name = "Read the ledger"
command_id = "majordomus-history"
what = "Prints the append-only ledger of starts, checkpoints, decisions, handovers and finishes."
why = "Every claim on this page can be traced to one of its lines."
example_event = "majordomus-init"

[[extra.features]]
name = "Scoped tasks"
how_used = "Six tasks were started with an explicit list of paths. Scope problems were resolved by finishing the task as partial and starting a new one with a corrected scope."
evidence = "Each task start in the ledger carries its declared scope; three restarts are recorded."
links = [{ label = "task lifecycle", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/task-lifecycle.md" }, { label = "first task start", url = "#event-t-20260914102623-44b3-start" }]

[[extra.features]]
name = "Finish contract with a verification command"
how_used = "Tasks closed as completed ran the production smoke test against the live URL; partial outcomes carried a handover instead."
evidence = "Each finish in the ledger stores the contract results, the verification command, its exit code and its duration."
links = [{ label = ".ai/repo/policy.yaml", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml" }, { label = "first completed finish", url = "#event-t-20260914103939-7b10-finish" }]

[[extra.features]]
name = "Checkpoints"
how_used = "Short progress notes while a task ran, written by the agent or derived from Git."
evidence = "Seven checkpoints in the ledger; two derived from Git state only the number of changed files."
links = [{ label = "continuity workflow", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/continuity.md" }, { label = "a derived checkpoint", url = "#event-checkpoint-20260914t121646z" }]

[[extra.features]]
name = "Handovers"
how_used = "Written before every restart and at the end of the main task, with Objective, Current State and Next Action."
evidence = "Four handovers in the ledger; the policy requires the three sections."
links = [{ label = "handover prompt", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/prompts/handover.md" }, { label = "a handover before a restart", url = "#event-handover-20260914t111009z" }]

[[extra.features]]
name = "Decision log"
how_used = "Decisions with their rationale, rejected alternatives and evidence, written down while the work was fresh."
evidence = "Four recorded decisions, each linked to the files that implement it."
links = [{ label = "evidence-ledger decision", url = "#event-decision-4" }]

[[extra.features]]
name = "Architecture decision records"
how_used = "The evidence-ledger decision was written up as ADR-0001 and left proposed for a person to accept."
evidence = "One ADR proposal in the ledger; the ADR file still has the status proposed."
links = [{ label = "ADR-0001", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md" }, { label = "proposal event", url = "#event-adr-0001-proposed" }]

[[extra.features]]
name = "Rules as versioned documents"
how_used = "A pinned vendored baseline plus six project rules, loaded into the agent's context and listed with their class and the commands that enforce them."
evidence = "Rule files under .ai/repo/rules; the rule listing shows that the project rules have no Majordomus validator."
links = [{ label = "project rules", url = "https://github.com/korczis/catharsis-as-a-service/tree/main/.ai/repo/rules/project" }, { label = "rules format", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/README.md" }]

[[extra.features]]
name = "Health check wired into Git and CI"
how_used = "The pre-commit hook and a CI job run the health check, which also reconciles the policy's enforcement entries with the hooks."
evidence = "The hook file and the Majordomus supervision job, which passed in every Pages run of the snapshot."
links = [{ label = ".githooks/pre-commit", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit" }, { label = ".github/workflows/ci.yml", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml" }]

[[extra.features]]
name = "Provider instruction files"
how_used = "AGENTS.md, CLAUDE.md and GEMINI.md were generated from the policy, so every agent starts from the same bootstrap."
evidence = "The first ledger event records the projection into three target files."
links = [{ label = "AGENTS.md", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/AGENTS.md" }, { label = "projection event", url = "#event-majordomus-init" }]

[[extra.features]]
name = "Append-only ledger"
how_used = "Every start, checkpoint, decision, handover and finish was recorded with its time and Git commit; this page is exported from it."
evidence = "The snapshot behind this page and the script that exports and checks it."
links = [{ label = "data/case_study.json", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/data/case_study.json" }, { label = "scripts/export-case-study.py", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/export-case-study.py" }]

[[extra.wiring]]
where = "Git pre-commit hook"
command = "majordomus doctor"
command_id = "majordomus-doctor"
effect = "Refuses a commit unless the layer is healthy and every declared enforcement is wired without a swallowed exit code."
file = ".githooks/pre-commit"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit"

[[extra.wiring]]
where = "Git pre-push hook"
command = "majordomus finish --check"
command_id = "majordomus-finish"
effect = "Refuses a push when the active task would not satisfy its finish contract, for example with files outside its scope."
file = ".githooks/pre-push"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-push"

[[extra.wiring]]
where = "Git commit-msg hook"
command = "scripts/lint-commits.sh --file"
command_id = "lint-commits"
effect = "Refuses a commit subject that is not a Conventional Commit, because release versions are computed from the subjects."
file = ".githooks/commit-msg"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/commit-msg"

[[extra.wiring]]
where = "CI job: Majordomus supervision"
command = "majordomus doctor"
command_id = "majordomus-doctor"
effect = "Installs the pinned Majordomus 0.6.0 and repeats the health check on every push and pull request, so a clone without hooks is still checked."
file = ".github/workflows/ci.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml"

[[extra.wiring]]
where = "CI job: Conventional commits"
command = "scripts/lint-commits.sh <range>"
command_id = "lint-commits"
effect = "Lints every subject in the pushed range; nothing deploys when it fails."
file = ".github/workflows/ci.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml"

[[extra.wiring]]
where = "Pages workflow: Verify production"
command = "npm run smoke"
command_id = "npm-run-smoke"
effect = "Deploy needs CI; Verify production waits for the pushed commit on the live site and runs the smoke test and Playwright against it; Release needs Verify production."
file = ".github/workflows/pages.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/pages.yml"

[[extra.wiring]]
where = "Majordomus policy"
command = "verification.finish_requires"
command_id = ""
effect = "The finish contract selects five requirements: scope respected, verification ran, state updated, no open blockers, note present."
file = ".ai/repo/policy.yaml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml"

[[extra.wiring]]
where = "GitHub rulesets"
command = "repository settings"
command_id = ""
effect = "main requires CI (with an admin bypass), main history cannot be rewritten or deleted, and v* release tags cannot be moved or deleted."
file = "release-on-verified-main rule"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/release-on-verified-main.v1.md"
+++

## What this case study is (and is not)

This page documents one delivery: the site you are reading, built on 14 September 2026 by an AI coding agent (Claude Code) that one person directed, with [Majordomus](https://majordomus.dev) 0.6.0 as the supervisory control layer between the agent and the repository. It is written as a tech demo. Every number on it is computed from records the delivery left behind: the Majordomus ledger, the decision log and handovers of the working checkout, the Git history, and GitHub's records of pipeline runs and releases. The <a href="#timeline">timeline</a> renders those records one by one, and each event links to the commit, run, release or file it came from.

What the page is not matters as much:

- **Not a controlled comparison.** There was one session, one person and one agent, and no comparable session without supervision. No speed-up factor follows from these records, and none is claimed here. Measured durations are reported; estimates of time saved, with their assumptions labelled, are left to the [time accounting article](../engineering/time-accounting/).
- **Not a general claim about Majordomus.** It shows how one repository configured it, which commands ran, what they recorded and what they refused. Another configuration behaves differently.
- **Not a record of everything.** The ledger stores accepted operations. A command that Majordomus refused leaves no entry, so friction is visible here only where a handover, a checkpoint or a commit mentions it.
- **Not a transcript.** Prompts, checkpoint bodies and local paths stay in the checkout. The published snapshot is curated, and [docs/CASE-STUDY.md](https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md) describes what it contains and why.

The [method note](@/research/method-majordomus/index.md) covers the first release in detail, including the kinds of instructions that drove the work. This page covers the supervision layer itself: how it was set up, how each part was used and where it stopped helping.

## The setup

**The agent and the person.** The agent read the repository, ran commands, edited files, committed and pushed. In the first phases the person sent about fifteen messages: requests, art direction, long structured briefs and short directives such as "deploy", "release automatically" and "use Majordomus and enforce it". Implementation choices were the agent's. Later in the day, further agents and a second session worked on the same checkout in parallel; the section on continuity describes how.

**The repository.** A Zola 0.23.6 site in English and Czech, styled with Tailwind CSS and enhanced with Alpine.js and Flowbite; Python validators, a Playwright suite and pytest; a small Rust workspace that reads the site's JSON API; and GitHub Actions workflows that deploy to GitHub Pages and cut releases. The [about page](@/about/index.md) describes the site, and the [status page](@/status/index.md) shows the build that is running.

**The Majordomus layer.** Majordomus keeps its state in a directory named [.ai/](https://github.com/korczis/catharsis-as-a-service/tree/main/.ai), which has two halves:

- `.ai/repo/` is tracked in Git and shared by every checkout. Its [manifest](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/manifest.yaml) registers the sections. The [policy](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml) sets context budgets, the checkpoint interval of the default profile, the requirements of the finish contract (scope respected, verification ran, state updated, no open blockers, note present), the sections a handover must have (Objective, Current State, Next Action) and two enforcement entries that bind commands to Git hooks. Four execution [profiles](https://github.com/korczis/catharsis-as-a-service/tree/main/.ai/repo/profiles) exist (implementation, debugging, deep work, routine), and every task here ran under `implementation`. Rules live under `.ai/repo/rules/`: a pinned, read-only vendored baseline and six project rules. Architecture decisions live under `.ai/repo/adrs/`.
- `.ai/local/` is ignored by Git. It holds the active task, the append-only ledger, checkpoints, handovers, the decision log and open questions. Nothing in it may be published by a generator, which is why this page ships a curated export instead of the directory.

From the policy, Majordomus generated three instruction files, [AGENTS.md](https://github.com/korczis/catharsis-as-a-service/blob/main/AGENTS.md), [CLAUDE.md](https://github.com/korczis/catharsis-as-a-service/blob/main/CLAUDE.md) and [GEMINI.md](https://github.com/korczis/catharsis-as-a-service/blob/main/GEMINI.md). Each one points an agent at `.ai/README.md` and its discovery protocol. The first ledger event, at 10:26:23 UTC, is that <a href="#event-majordomus-init">projection</a>.

**Hooks and CI.** Running [`npm ci`](../commands/#npm-ci) points Git at the repository's `.githooks/` directory. The CI workflow repeats the Majordomus health check in a job of its own, so a clone without hooks is still checked. The <a href="#wiring">wiring table</a> lists every enforcement point.

## The task lifecycle in practice

Majordomus allows one active task per checkout. The <a href="#lifecycle">lifecycle diagram</a> above walks through each step with its registered command and a real recorded example; this section tells the same story in order.

**Start with a scope.** [`majordomus start`](../commands/#majordomus-start) opens a task with a title, a profile and the paths it may touch. The first task started at 10:26:23 UTC and claimed 20 paths. Six tasks were started in the recorded period, with scopes from one path to 31.

**Work, then check.** [`majordomus check`](../commands/#majordomus-check) is read-only: it reports whether the active task is consistent with the policy, its scope and the recorded state. [`majordomus watch`](../commands/#majordomus-watch) reports drift between the task, its scope, the policy and the generated instruction files. Between them they caught two scope problems before the first push (see <a href="#findings">what supervision caught</a>).

**Checkpoint.** [`majordomus checkpoint`](../commands/#majordomus-checkpoint) records a short progress note, capped at 40 lines by the policy. Seven checkpoints were recorded. The agent wrote four of them; the <a href="#event-checkpoint-20260914t104327z">checkpoint at 10:43:27</a>, for example, was written right after the first push, while the pipeline was running. Two were derived from Git without any authored text and state only how many files had changed since the task started: 65 at 12:16:46 and 144 at 12:52:41. The last one belongs to the task that was still active at the end of the snapshot.

**Record decisions.** [`majordomus decision`](../commands/#majordomus-decision) appends a dated entry with the rationale, the rejected alternatives and the evidence. Four decisions were recorded; they are listed under decisions and ADRs below.

**Hand over.** [`majordomus handover`](../commands/#majordomus-handover) writes a continuation record with the three sections the policy requires. Four handovers were written. Three of them came one or two seconds before a task was finished as `partial`, which is the pattern the finish contract asks for: an outcome other than `completed` needs a note that says what comes next.

**Finish with a verification command.** [`majordomus finish`](../commands/#majordomus-finish) evaluates the finish contract. An outcome of `completed` requires a verification command that ran and exited zero, and the ledger stores the command, its exit code and its duration. For this repository the agent chose the production smoke test, the script behind [`npm run smoke`](../commands/#npm-run-smoke), run against the live URL. The <a href="#event-t-20260914103939-7b10-finish">first completed task</a> closed at 10:47:25 UTC, less than two minutes after release v0.1.0 was published, and its verification command exited 0 after 7 seconds. Its contract recorded seven requirements as pass, four as skipped and none as failed; requirements that did not apply to the outcome or the configuration are recorded as skipped. The second completed task closed the same way at 13:08:34, after release v0.5.0.

**Read it back.** [`majordomus history`](../commands/#majordomus-history) prints the ledger. The snapshot behind this page was exported from its JSON output.

## Enforcement wiring

A rule that nothing runs is a suggestion. Majordomus reconciles the enforcement entries of its policy: [`majordomus doctor`](../commands/#majordomus-doctor) fails when a declared command is missing, is not executable, is not invoked by the hook the policy names, or is invoked in a way that swallows its exit code. The vendored rule behind this is enforcement-wiring, and the doctor enforces it.

- **Pre-commit.** [.githooks/pre-commit](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit) refuses to run when Majordomus is not installed and then runs [`majordomus doctor`](../commands/#majordomus-doctor). A commit therefore requires a healthy, wired layer.
- **Pre-push.** [.githooks/pre-push](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-push) runs [`majordomus finish --check`](../commands/#majordomus-finish), which evaluates the active task's finish contract without closing the task. A push that carries work outside the claimed scope is refused before it leaves the machine.
- **Commit messages.** [.githooks/commit-msg](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/commit-msg) runs [`scripts/lint-commits.sh`](../commands/#lint-commits). Conventional Commits are enforced because release versions are computed from them.
- **The CI supervision job.** The Majordomus supervision job in [ci.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml) installs Majordomus at the pinned version 0.6.0 (the installer verifies the SHA-256 of the release), points Git at the hooks and runs [`majordomus doctor`](../commands/#majordomus-doctor). It passed in every Pages run in the snapshot.
- **Deployment gates.** [pages.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/pages.yml) runs CI, then Deploy, then Verify production, then Release. Deploy asserts that the Pages URL equals the base URL in the Zola configuration. Verify production waits until the live site serves the pushed commit, then runs the smoke test and the browser suite against it with [`npm run test:production`](../commands/#npm-run-test-production). Release runs only after Verify production has passed.
- **Repository rulesets.** Three rulesets protect the repository on GitHub: `main` requires CI, the history of `main` cannot be rewritten or deleted, and `v*` tags cannot be moved or deleted. The CI requirement allows an admin bypass, and the first push used it.

Only the two hooks are Majordomus enforcement in the strict sense. The rest are conventional safeguards of the same repository, and this account does not separate their effects from those of Majordomus.

## Rules next to the code

Rules are Markdown documents with front matter: an `id`, a `version`, a class (`blocking` or `advisory`) and optional dependencies written as exact `id@version` references. The effective set is additive, the vendored Majordomus baseline plus the project's own rules, and there is no override mechanism. [`majordomus rules list`](../commands/#majordomus-rules) prints the set with each rule's class and the commands that enforce it.

The six project rules, each linked to its file:

- [verified-deployment](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/verified-deployment.v1.md): nothing is reported as deployed until the verify job of the Pages workflow has passed against the live URL that GitHub returns.
- [zola-source-of-truth](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/zola-source-of-truth.v1.md): Zola generates all public HTML; content lives in Markdown, interface strings in translation dictionaries, and templates are shared by both languages.
- [release-on-verified-main](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/release-on-verified-main.v1.md): Conventional Commits are mandatory, and every verified push to `main` produces a release whose version is derived from the commits.
- [evidence-ledger](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/evidence-ledger.v1.md): every public claim is recorded with its sources, evidence level, confidence and a review date that has not passed.
- [no-neuro-overreach](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/no-neuro-overreach.v1.md): no sentence may claim that a signal, a model or a brain region reveals what a person feels.
- [medical-claims](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/medical-claims.v1.md): findings are stated at group level with their limits, nobody is assessed individually, and every research note and advice entry carries the clinical disclaimer.

All six are blocking, and their dependencies are explicit: evidence-ledger depends on verified-deployment, no-neuro-overreach on evidence-ledger, and medical-claims on both. None of them has an `x-majordomus` block, and the rule listing reports them as having no validator. That is deliberate and written in each file: Majordomus resolves them, lists them and loads them into an agent's context, while the project's validators, CI jobs and review enforce them. The distinction matters when reading this case study. When a prohibited phrase or an expired claim fails the build, the project's [content validator](../commands/#validate-content) or [ledger validator](../commands/#validate-claims) caught it, not Majordomus.

Majordomus enforcement lives in the vendored baseline. Four of its rules did visible work in this delivery. Scope-integrity treats work outside the claimed paths as not belonging to the task; check, finish and watch enforce it. Verification-integrity requires a completed outcome to have a verification command that exited zero, with its exit code and duration recorded; finish enforces it. Note-integrity requires every outcome to carry a note with the sections that outcome needs; finish enforces it too. Enforcement-wiring, described above, is enforced by the doctor.

## Decisions and ADRs

Two mechanisms separate a working decision from a durable one.

The **decision log** is local, append-only and cheap to write. [`majordomus decision`](../commands/#majordomus-decision) records what was decided, why, what was rejected and where the evidence is. Four entries were recorded:

1. <a href="#event-decision-1">Structured data is built as Tera data and serialised with json_encode</a>. Hand-written JSON-LD inside templates is HTML-escaped and breaks on quotes. Rejected: hand-written JSON-LD strings, and a script that injects them in the browser.
2. <a href="#event-decision-2">Link previews are localized per language, and the sitemap lists every language edition</a>. Rejected: one English preview card for every page, and language alternates only in the HTML.
3. <a href="#event-decision-3">Python validators are tested with pytest in a project virtual environment</a>. Rejected: the standard library's unittest, and a global pytest installation.
4. <a href="#event-decision-4">Evidence is tracked as a dated ledger</a> of appraised sources and graded claims, with validators that fail the build on stale or inconsistent entries. Rejected: free-text evidence notes on each page, and a single file that mixes bibliographic facts with editorial judgement.

The first three were recorded within one second of each other (11:08:30 to 11:08:31 UTC), shortly before a handover. Decisions were written down when a task was about to close, not continuously while it ran.

The **architecture decision record** is tracked and durable. The fourth decision was written up as [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md) with its context, the decision, the rejected alternatives and the consequences, and the ledger records it as <a href="#event-adr-0001-proposed">proposed at 12:55:12</a>. The agent did not accept it, because acceptance is a person's act. The last handover of that task names accepting or amending ADR-0001 as the next action, and [`majordomus adr list`](../commands/#majordomus-adr) still shows it as proposed. The decision itself is visible on this site: the [evidence page](@/evidence/index.md) and the [methods page](@/methods/index.md) render grades from the ledger it describes.

## What supervision caught

The <a href="#findings">findings</a> on this page are generated from the records, not written by hand. The export script declares what to look for and publishes a finding only when the ledger, a handover, a checkpoint or the pipeline data confirms it. Each card links to its evidence in the timeline. In order:

- **Scope drift after a file move.** The first task claimed 20 paths but not the root files that were moved into the artwork and static directories. The handover records that [`majordomus watch`](../commands/#majordomus-watch) reported the drift. The task was finished as partial 2 minutes 53 seconds after it started and restarted with a scope that named those files.
- **A scope of "." before the first push.** The restarted task declared a single dot as its scope. Majordomus does not read that as the whole repository, so [`majordomus check`](../commands/#majordomus-check) reported every changed file as out of scope. The task was restarted at 10:39:39 with 26 explicit paths. The first push came about three minutes later, and its pipeline passed all seven jobs.
- **A brief that outgrew its scope.** When the work expanded to a Rust workspace, data files and Python tooling, the handover recorded that the new top-level paths fell outside the claimed scope. A new task claimed 31 paths.
- **A ruleset bypass.** The checkpoint written after the first push records that the push went through the admin bypass of the ruleset that requires CI on `main`. Deployment itself stayed gated by the job dependencies of the workflow. This was recorded, not prevented.
- **Completion only with a live check.** Both tasks closed as completed ran the production smoke test as their verification command, and both exited 0. The three partial tasks claimed no completion.
- **A failed reference check stopped a deployment.** CI caught this one, not Majordomus. Run 34842607207 failed in the References (Crossref) job, and Deploy, Verify production and Release were skipped. A fix to title matching (commit 94d734c) followed, and the next run published v0.3.0 at 12:24:28, seven minutes after the failing run had started.
- **A failed production verification.** Also CI. Run 34860959250 deployed and then failed in Verify production, when one of 84 browser tests timed out against the live site; Release was skipped. Because live verification needs a deployment, the unverified build stayed online until the next run. A follow-up commit made that test deterministic, and the next run, for a later commit that included it, passed and published v0.6.0.
- **An ADR left to a person.** Described under decisions and ADRs above.

Three events mentioned in other accounts of this delivery are not among the findings, because the records do not confirm them: a pre-commit health check that flagged the README for not linking the agent bootstrap, a finish command refused until a handover existed, and a rule dependency the resolver rejected until it was written as an `id@version` reference. Refusals are not written to the ledger, and none of the three appears in a handover, a checkpoint or a commit. They may have happened; this page does not count them.

## Continuity across restarts and parallel workers

Restarting a task was cheap in recorded time. Between a handover, the partial finish and the next start, the ledger never shows more than two seconds. Six tasks were started and three of them were restarts. What made restarts cheap is that the state lived in files rather than in the agent's conversation. A handover carries the objective, the current state and the next action, together with fields computed from Git (branch, commit, clean or dirty tree, changed files) that an author may not write. The policy also has the session hooks write a briefing when an episode starts, a derived checkpoint when the conversation is compacted, and a continuation record when an episode ends while a task is still active.

Later in the day the delivery tested a harder case: several workers on one checkout at the same time. At the end of the snapshot one task is active. It started at 14:54:07 UTC and claims 31 paths, which is the whole working tree. Content agents, a second Claude session and the main session worked inside it at once, each told which files it owned. This page was written by one of those workers, which was told not to start, checkpoint, hand over or finish tasks and not to edit files that other workers held.

That arrangement exposes a limit. Majordomus scopes work per task and per checkout. Inside one checkout, parallel workers share the active task, and Majordomus cannot tell which worker changed which file. Coordination came from explicit path ownership in each worker's instructions, and from Git. The vendored baseline states the Majordomus answer as principles: one worker, one scope, with a scope claimed by another worktree treated as a boundary, and parallel work isolated from each other. This delivery did not apply them inside one checkout.

## Evidence of delivery

Everything in this section is linked, and the <a href="#timeline">timeline</a> can be filtered to show only commits, pipeline runs or releases.

- **Commits.** Every commit subject is a Conventional Commit. The first, the poster, is dated 09:54:05 UTC, one second before the GitHub repository was created; the site followed at 10:42:45.
- **Pipeline runs.** The first Pages run started at 10:43:02 and finished at 10:45:45, with seven jobs that all passed. Later runs grew to ten jobs as Python tests, a Rust job and the Crossref check joined CI. Two of the first seven runs failed, and both failures are shown with what followed them.
- **Releases.** Release v0.1.0 was published at 10:45:42, after live verification: 51 minutes 37 seconds after the first commit and 19 minutes 19 seconds after Majordomus was initialised. Releases v0.2.0 to v0.5.0 followed by 13:07:10, each cut by the Release job of a run whose production verification had passed.
- **Completed tasks.** Both completed tasks store their verification command, exit code 0 and duration in the ledger.

Two loops can be measured directly. From the site commit to the published v0.1.0 took 2 minutes 57 seconds. From the start of the run that failed on references to the published v0.3.0 took 7 minutes 9 seconds. The [releases page](https://github.com/korczis/catharsis-as-a-service/releases) and the [runs of the Pages workflow](https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml) are the primary records, and [`gh run list`](../commands/#gh-run-list) reads the same data.

## What it cost and what it did not solve

**Friction.** Three of six tasks ended as partial and were restarted because of how their scope was declared. Two of those restarts happened within the first fourteen minutes of supervision. A scope has to be written as explicit top-level paths, and in this delivery a grown brief meant closing the task and opening a new one, which matches the baseline principle of claiming paths when a task starts instead of widening the scope silently. The records themselves cost attention: seven checkpoints, four handovers and four decisions between 10:26 and 13:08 UTC, plus the task that followed. And because the finish contract refuses a completed outcome without a passing verification command, a task could not be closed as completed before the pipeline had deployed and the live site answered.

**What Majordomus did not check.**

- Whether content is true, well sourced or safely worded. The project's validators and a reviewer own that.
- Whether the verification command is adequate. The contract checks that the command ran and exited zero; choosing a live smoke test was the agent's decision.
- Whether tests are meaningful, or whether a failing test is flaky or real.
- Which worker did what inside one checkout shared by parallel workers.
- The six project rules, which it lists but does not enforce.

**What the records cannot show.** Refused commands are not in the ledger. The time a person spent reading, deciding and writing briefs is recorded nowhere. Durations depend on hardware, the network and the CI queue. And because conventional safeguards (local validation, browser tests, CI gates and rulesets) ran alongside Majordomus, their effects cannot be separated here.

**What it did change, as far as the records show.** Every claim of completion in this project is tied to a recorded command and its exit code. Scope mistakes surfaced locally, before any push, instead of as failed pipeline runs. And the state needed to resume work sat in files that a new worker could read, which is also what made this case study possible.

## How to reproduce

The records are in the public repository, except `.ai/local/`, which never leaves a checkout. To inspect them in your own clone:

1. Install Majordomus from [majordomus.dev](https://majordomus.dev) and run [`npm ci`](../commands/#npm-ci) so that the hooks are active.
2. Check the layer with [`majordomus doctor`](../commands/#majordomus-doctor), list the effective rules with [`majordomus rules list`](../commands/#majordomus-rules) and the architecture decisions with [`majordomus adr list`](../commands/#majordomus-adr).
3. Read the pipeline history with [`gh run list`](../commands/#gh-run-list) and the task lifecycle in [.ai/repo/workflows/task-lifecycle.md](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/task-lifecycle.md).
4. In a checkout that has its own ledger, [`majordomus history`](../commands/#majordomus-history) prints it, and [`python3 scripts/export-case-study.py`](../commands/#export-case-study) regenerates the snapshot behind this page. With the check option, the same script validates the committed snapshot without local state or network access, which is how CI treats it.

The snapshot format, what it includes and what it leaves out are documented in [docs/CASE-STUDY.md](https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md). For how the rest of the site was engineered, read the [engineering articles](../engineering/).
