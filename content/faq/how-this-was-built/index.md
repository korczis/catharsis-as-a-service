+++
title = "How was this site built, and how long did it take?"
description = "It went from an empty GitHub repository to a verified release in 51 minutes and 36 seconds, built by an AI coding agent under supervision. The timeline comes from records, and no speed multiple is claimed."
date = 2026-09-14
weight = 17

[taxonomies]
tags = ["methods", "majordomus", "software delivery"]

[extra]
kicker = "Question 17"
short_answer = "It was built in a single working session by an AI coding agent directed by one person, with Majordomus as the supervisory layer. From repository creation to the first verified release took 51 minutes and 36 seconds, and from Majordomus initialisation to that release 19 minutes and 19 seconds. Those durations come from Git, GitHub, pipeline and Majordomus records. No speed multiple is claimed, because there was no control condition."
related_questions = ["faq/how-evidence-is-graded/index.md", "faq/why-an-artwork/index.md", "faq/does-this-site-measure-me/index.md"]
read_next = ["research/method-majordomus/index.md", "evidence/index.md"]
references = ["repository-2026", "majordomus-2026"]
+++

## What the records say

The site is a bilingual static publication generated with Zola, deployed to GitHub Pages and verified against the live URL on every change. It was produced in a single working session by an AI coding agent (Claude Code) directed by one person, with Majordomus as the supervisory layer between the agent and the repository.

All the times below are UTC on 14 September 2026 and come from the Git history, the GitHub API, the Majordomus ledger and the pipeline records. The working session began at 09:45 with the poster rebuild. The GitHub repository was created at 09:54:06. The Majordomus layer was initialised and the first supervised task started at 10:26:23. The site was committed at 10:42:45. The Pages pipeline ran 7 jobs in 2 minutes 43 seconds, all passed, and release v0.1.0 was published at 10:45:42 after live verification.

The derived durations are: repository creation to first verified release, **51 min 36 s**; Majordomus initialisation to first verified release, **19 min 19 s**; push to verified release, **2 min 57 s**. At that release the site was checked by 7 validation stages and 30 browser tests.

## What the person supplied

The work was driven by about fifteen messages from one person, of five kinds: a one-line request to create a project on GitHub; art direction for the poster, followed by a choice between three offered approaches; three structured execution briefs of increasing scope; short directives during work such as deploy, validate in a browser and release automatically; and editorial direction, including replacing promotional copy with serious, sourced psychology.

None of those messages specified implementation details such as template syntax or test cases. Those were the agent's decisions, and the supervision layer's job was to keep them checkable.

## What supervision caught

Majordomus did not write code. It scoped and recorded the work, and three defects became local findings rather than failed pipeline runs. At 10:29:16 scope drift was reported after files were moved, and the task was restarted. At 10:39:39 a malformed scope was reported by the pre-push check, and the task was restarted before any push. Before the first commit, the health check that runs in the pre-commit hook reported that the README did not link the agent bootstrap file, and the defect was fixed before it reached the repository.

One mechanism matters more than the rest: a task cannot be closed as completed unless its verification command passes. Here that command was the live smoke test, so "completed" meant "deployed and checked", not "written". The task was closed at 10:47:25 with that test passing in 7 seconds.

## Why no speed multiple is claimed

There was one session and no comparable session without supervision, so there is no control condition and no speed-up factor can be stated. That is the honest limit, and it is recorded in the ledger alongside the timeline itself.

What the records do show is where time was not lost. No push was rejected by CI, no deployment had to be rolled back, and the first pipeline run passed all seven jobs. Three further limits apply: the timeline starts at the first recorded file, so planning before it is excluded; durations depend on the tools, hardware and network latency of this session; and the session also relied on conventional safeguards unrelated to Majordomus, whose effects are not separated out.
