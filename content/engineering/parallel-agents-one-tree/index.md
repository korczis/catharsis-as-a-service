+++
title = "Parallel agents, one working tree: fan-out, proposals and explicit-path commits"
description = "How several AI workers extended the site at the same time on a single Git working tree: content agents that write only their own files and propose shared data, a main session that merges, a peer session that commits by explicit path, and what the records show went wrong."
date = 2026-09-14
weight = 5

[taxonomies]
tags = ["engineering", "ai agents", "parallel work", "git"]

[extra]
kicker = "Engineering 05"
kind = "technical"
summary = "After the fifth release, the work fanned out. A main session dispatched content agents to write new research notes, theory essays, models and glossary terms; a second, independent session worked on the same checkout and committed its own changes. Nobody used branches. This article describes the conventions that let that work, from file ownership and proposal files to a single merger and commits by explicit path, and it reports the failures that the Git history, the pipeline runs and the files show."
key_points = [
  "Content agents own directories, never shared files: pages go straight into their own paths, while additions to the shared ledger arrive as proposal files that one merger appends after checking identifiers and syntax.",
  "A peer session committed on the same tree by naming paths; one of its commits added six claims to a ledger file that at that moment held dozens of other uncommitted claims, and none of those were included.",
  "The shared tree is often mid-edit, so workers validate their own changes and render in a private copy; the repository-wide validators fail on other workers' unfinished files."
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Why one tree and not branches

The usual answer to parallel work in Git is branches, one per worker, merged through pull requests. On 14 September 2026 the site was extended differently: several AI workers wrote into one working copy of `main` at the same time. The reason was practical. The work was mostly additive (new pages, new ledger entries), the pipeline releases every verified push to `main`, and the person directing the work wanted the result visible in one place as it grew.

One tree removes merge conflicts in the Git sense and replaces them with a different problem: two workers can write the same file at the same time, a worker can commit someone else's half-finished change, and every repository-wide check sees everyone's work in progress. This article describes how that was handled and what went wrong. It only reports what the records show: the Git history and its commit trailers, the GitHub Actions runs, the Majordomus ledger, and the files in the working copy. The [case study](../../case-study/) shows the same period on a timeline.

## Who was working

Three kinds of worker appear in the records.

**The main session.** Every commit from the poster to [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) carries the same `Claude-Session` trailer. This session started the supervised task that was still active at the time of writing, recorded at 14:54:07 UTC with the objective "Extend the site: more research and advice, per-page social previews, search and glossary cross-linking, second artifact Closure as a Service".

**Content agents dispatched by the main session.** They do not appear in Git at all, because they were not allowed to commit. Their work appears as new directories in the working copy (research notes, theory essays, the interactive models page) and as proposal files in the main session's private scratch space, one directory per agent. This article is itself the output of such an agent.

**A peer session.** Commits [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163), [93fd07f](https://github.com/korczis/catharsis-as-a-service/commit/93fd07f) and [2125f1e](https://github.com/korczis/catharsis-as-a-service/commit/2125f1e) carry a different `Claude-Session` trailer from the main session's. They were made on the same checkout, during the main session's active task, while the tree held the main session's and the content agents' uncommitted work.

## Fan-out: a brief that fixes ownership

A content agent receives a brief, and the brief carries the concurrency rules. The brief behind this section is typical. It lists the only files the agent may create (the section index and one directory per article, in both languages), names the files it must not touch ("templates, scripts, data/*.toml, zola.toml, tests or other content; other workers … edit those"), forbids Git operations and Majordomus write commands, and says where proposals go: a directory in the scratch space.

The rules come down to one principle: **an agent writes only paths that no other worker writes.** A research note lives in its own directory, so two agents writing two notes never touch the same file. This makes most of the fan-out conflict-free by construction, with no locking.

The exceptions are the files every page depends on:

- `data/references.toml`, `data/sources.toml`, `data/claims.toml`, `data/glossary.toml` and `data/evidence_changelog.toml`, because every substantive claim needs a ledger entry ([The evidence ledger as code](@/engineering/evidence-ledger-as-code/index.md));
- `data/commands.toml`, because every command mentioned in prose needs a registry entry;
- `zola.toml`, because UI strings live there.

## Proposals and a single merger

For shared data, agents write **proposals**: TOML files with the same shape as the target, containing only their additions. The main session's scratch space holds four such directories from the day's fan-out, with names that match the work (`expand`, `expand-glossary`, `expand-models`, `expand-theory`), each with some of `references.toml`, `sources.toml`, `claims.toml`, `glossary.toml` and `changelog.toml`.

A short script in the same scratch space, `merge_expand.py`, applies them. Its docstring states the contract:

```text
Merge agent proposal files (scratchpad/expand*/{references,sources,claims,glossary,changelog}.toml)
into <root>/data/*.toml by appending TOML text. Entries whose id already exists are skipped and reported.
```

Three details make the merge safe to run repeatedly:

1. **Identifiers are checked before appending.** A reference, appraisal, claim or term whose id already exists is skipped with a report line, so two agents that cite the same paper do not produce a duplicate key, which TOML would reject.
2. **Each block must parse on its own** (`tomllib.loads(block)` before it is written), so a malformed proposal fails before it reaches the shared file.
3. **The changelog is prepended**, because the ledger keeps its changelog newest first, and after merging the script parses all five data files again.

The merge appends text rather than re-serialising the data. That keeps comments, section headings and formatting in the hand-maintained files intact, and it keeps the diff for review to exactly the added entries. The main session then runs the validators on the merged tree, where problems the agent could not see on its own (an id that another agent used for a different paper, for example) come to light.

This is the one place where the work is serialised: many agents propose, one session merges. The evidence changelog in the working copy shows the result, for example an entry recording the claims and three references added for the interactive models page.

## A peer session on the same tree

The peer session did not use proposals. It worked directly in the tree and committed its own changes, and the commits show how: by naming paths rather than committing everything that had changed.

- **d2b3c47** (15:14:22 UTC) changed five files: `static/js/app.js`, `styles/app.css`, `templates/components/library.html`, `tests/site.spec.js` and `zola.toml`. At the time of writing, four of those files (`styles/app.css`, the library component, the browser suite and `zola.toml`) carry further uncommitted changes from other workers, and those changes are not part of the commit.
- **2125f1e** (15:38:00 UTC) extended the research note on measuring emotion and added eight references and six claims. The committed `data/claims.toml` contains 56 claims, the 50 from v0.5.0 plus its own six. When this article's author counted the claims in the shared working copy a few minutes before that commit, the file already held 86; a count after the commit found 92, the same 86 plus the six. The other 36 entries stayed uncommitted.

The second case is the harder one. The peer session committed part of a file that other workers had also changed, and the result on `main` is a ledger consistent with the pages committed alongside it. The records do not say which Git mechanism was used to stage only those entries. They show the outcome: the commit's contents match its message.

Both sessions ran under the same hooks: `commit-msg` lints the subject and `pre-commit` runs [`majordomus doctor`](../../commands/#majordomus-doctor). The Majordomus ledger records one active task in this period, the one the main session started. The supervision layer's unit is the working tree and its task, not the session, so the peer session's commits fell within the scope of a task it did not start. That task's scope listed every top-level path in the repository, so the peer session's files fell inside it; under a narrower scope, [`majordomus check`](../../commands/#majordomus-check) would have reported them as drift.

## What went wrong

The records show four problems in this phase. None was a lost change, and all four follow from sharing one tree.

**Repository-wide validators fail on other workers' unfinished files.** When this article was drafted, running [`python3 scripts/validate-content.py`](../../commands/#validate-content) on the shared tree reported FAIL on files this agent does not own. The translation validator reported `content/about/index.cs.md: [extra] structure differs from en`, a page another worker was editing at that moment. On a shared tree, a red validator does not tell a worker that *its* change is wrong. Content agents are therefore told to ignore errors in files they do not own, and to build a private copy of the repository when they need a clean render.

**A commit can pass CI and still fail production.** d2b3c47 passed all seven CI jobs and deployed. In [run 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250), one production browser test failed and the release was skipped. The cause and fix are covered in [Testing a static site](@/engineering/testing-a-static-site/index.md). What matters here is how long the failure stayed open: the fix, 93fd07f, was committed 14 minutes 28 seconds after the failing job ended. Meanwhile the live site served a commit that had not been verified, while other workers kept writing into the tree.

**Two commits eight seconds apart produce one pipeline run.** 93fd07f and 2125f1e were committed at 15:37:52 and 15:38:00 UTC. The Pages workflow has a concurrency group with `cancel-in-progress: true`, and the run list shows one run, [34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153), for the head commit. The run passed, and [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) released d2b3c47, the fix and the content change together. That is correct behaviour: the release notes list every commit since the last tag. It also means that a fix and an unrelated content change are verified, and released or not, together.

**Earlier, before the fan-out: scope drift.** In the single-session morning, three supervised tasks ended as partial because the declared scope no longer matched the files being changed; see [Supervised AI delivery](@/engineering/supervised-ai-delivery/index.md). With several workers on one tree, the main session's task scope was set to cover every top-level path, which avoids those interruptions. It also means the supervision layer no longer separates one worker's files from another's.

## What held, and what would have to change

The conventions that held are simple enough to write in a brief: own a directory, propose shared data, let one session merge, commit by path, validate your own files, render in a copy. At the time of writing, no work was lost and no commit mixed one worker's changes with another's: each commit after the fan-out contains the files and entries its message describes, and each went through the same pipeline as everything else.

Two things would have to change for this to scale beyond a handful of workers. The first is attribution. Neither Git nor the Majordomus ledger records which content agent produced which page, and the proposal directories that would show it are private scratch files that will not survive the session. The second is isolation. The shared-tree failures above, validators contaminated by unfinished work and fixes batched with unrelated changes, are exactly what separate worktrees and branches exist to prevent. The agent bootstrap file in the repository already describes a worktree convention for future work. Using it would give each worker a clean tree and a pipeline run of its own, at the price of merges.
