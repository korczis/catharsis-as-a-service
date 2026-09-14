# Case study snapshot

The case study page (`/case-study/`, `/cs/pripadova-studie/`) shows how Majordomus supervised the delivery
of this site. Its numbers, timeline and findings come from one file, `data/case_study.json`, which Zola
reads at build time with `load_data`. This document explains how that file is produced, what it contains,
what it deliberately leaves out, and how to refresh it.

## Why a snapshot

The records behind the case study live in three places, and two of them are not available at build time:

| Source | Where | Available in CI |
|---|---|---|
| Majordomus ledger, task titles, decisions, handovers, checkpoints | `.ai/local/state/` of the working checkout | no: ignored by Git, never shared |
| Commit history | Git | yes |
| Releases, Pages workflow runs and their jobs | GitHub API | only with network and a token |

`.ai/local/` must never be published by a generator (see `.ai/README.md`), and the site build must not
depend on the network. The exporter therefore runs locally, curates the records into a small, sanitized
JSON file, and that file is committed. CI only checks it.

## Producing it

[`python3 scripts/export-case-study.py`](https://korczis.github.io/catharsis-as-a-service/commands/#export-case-study)
reads:

- the ledger through [`majordomus history`](https://korczis.github.io/catharsis-as-a-service/commands/#majordomus-history)
  with its JSON output for the whole history, falling back to `.ai/local/state/ledger.jsonl`;
- task titles from `.ai/local/state/archive/*.yaml` and `current.yaml`;
- decisions from `.ai/local/state/decisions.md`;
- handovers and checkpoints from `.ai/local/state/handovers/` and `checkpoints/`;
- the Git history (full SHA, commit time, subject);
- releases and runs of `pages.yml` with their jobs through the GitHub CLI, the same data
  [`gh run list`](https://korczis.github.io/catharsis-as-a-service/commands/#gh-run-list) shows.

Options:

- `--offline` keeps the GitHub records (pipelines, releases) of the existing snapshot and refreshes only
  the Majordomus and Git records.
- `--out <file>` writes elsewhere, for example to compare two exports.
- `--check` validates the existing snapshot and exits non-zero on any problem. It reads only the snapshot,
  `data/commands.toml` and the case-study front matter, so it needs neither `.ai/local`, Git, the GitHub CLI
  nor the network.

The export validates its own output with the same schema check before writing, and writes nothing when the
check fails.

## Determinism

The output is JSON with sorted keys and two-space indentation. It carries no generation timestamp:
`generated_from.through` is the time of the latest record, not the time of the export. Events are sorted by
time, then by source order (ledger order for Majordomus events), then by id. The same records produce the
same bytes, which `tests/python/test_case_study.py` checks when the local state is present.

Event ids are stable because they are derived from the records themselves: `<task-id>-start`,
`<task-id>-finish`, `checkpoint-<ledger time>`, `handover-<ledger time>`, `decision-<n>`, `adr-0001-proposed`,
`commit-<short sha>`, `pipeline-<run id>`, `release-<tag>` and `finding-<id>`. The page links to them as
`#event-<id>`, and the lifecycle steps in the front matter name them in `example_event`; `--check` fails when
a front-matter reference does not exist in the snapshot or a `command_id` is not in the command registry.

## Schema

Top level (`schema = "case-study/v1"`):

| Key | Content |
|---|---|
| `generated_from` | counts per source (ledger events, tasks, checkpoints, handovers, decisions, ADR proposals, findings, commits, pipeline runs, releases, events) and `through` |
| `milestones` | first commit, Majordomus initialisation, first release, and the two durations in seconds |
| `tasks` | id, title, start and finish time, outcome (`active` while unfinished), profile, number of scope paths, checkpoints, handovers, decisions, finish contract results, verification command with exit code and seconds, duration |
| `events` | `id`, `ts`, `kind` (task, checkpoint, finish, decision, handover, finding, commit, pipeline, release), `title_en`, optional `title_cs`, `detail_en`, `detail_cs`, `task`, and `links` (label and https URL) |
| `findings` | id, time, English and Czech title and detail, `caught_by` (a registry command id, `ci:<job>` or null), evidence event ids, links |
| `commits` | SHA, time, subject, URL |
| `pipelines` | run id, SHA, title, conclusion, created and updated time, seconds, URL, jobs with conclusion and timing |
| `releases` | tag, publication time, URL, and the run and SHA whose Release job published it |

All timestamps are UTC in the form `YYYY-MM-DDTHH:MM:SSZ`.

## What is included and what is not

Included, because each item is a fact about the delivery that a reader can check against the repository or
GitHub:

- event types, times, task ids, profiles and the number of scope paths;
- finish contract results per rule and the verification command with its exit code and duration;
- decision titles with their rationale, rejected alternatives and evidence, as recorded in the decision log;
- the Current State and Next Action sections of handovers, which are short factual summaries;
- for checkpoints, only whether the note was authored or derived and, for derived ones, the number of changed files;
- commit subjects, run and job outcomes, and release tags, all linked.

Excluded, for privacy and because they are not needed to check the account:

- absolute local paths, the repository and worktree fields computed on the author's machine, and file paths
  under `.ai/local/` (the check fails if a local path or one of these field names appears);
- bodies of authored checkpoints, which are working notes;
- prompts and session contexts (`.ai/local/prompts/`, `.ai/local/session-contexts/`), which are never read;
- scope path lists, of which only the count is kept; the one-path scope of `.` is quoted because it is
  itself a finding.

The owner handle `korczis` appears in URLs and task records; it is already public in the repository URL.

## Findings

Findings are not written by hand. The exporter declares each one as a function over the
loaded records, and a finding is published only when its evidence exists: a handover that records the drift,
a task whose scope was `.`, a checkpoint that records the ruleset bypass, a pipeline job that failed. Each
finding lists the event ids it rests on. Events that other accounts mention but that no record confirms
(for example a refused command, since refusals are not written to the ledger) are not findings, and the
case study says so.

## Refreshing

1. In the primary checkout, with Majordomus state and an authenticated GitHub CLI, run
   [`python3 scripts/export-case-study.py`](https://korczis.github.io/catharsis-as-a-service/commands/#export-case-study).
2. Review the diff of `data/case_study.json`. New events should only be appended in time; a changed old
   event means a record was rewritten and needs an explanation.
3. Update prose in `content/case-study/index.md` and `index.cs.md` only where it quotes numbers that changed.
   The metrics, timeline and findings update themselves.
4. Run [`npm run validate`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-validate) and
   [`npm run test:python`](https://korczis.github.io/catharsis-as-a-service/commands/#npm-run-test-python),
   then commit.

A snapshot is a record of a moment. Pipeline runs that were still queued at export time are not included, and
the page states the time of the latest record it contains.
