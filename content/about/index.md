+++
title = "About"
description = "What Catharsis as a Service™ is and why it exists: the motivation, the psychology and theory behind it, its principles, how it is built and how its delivery was supervised with Majordomus."

[extra]
figures = [
  { kind = "screens", id = "about-cockpit", caption = "Concept screens of a Majordomus cockpit for rules and worktrees. The data is illustrative and does not describe this project.", items = [
    { src = "assets/majordomus/cockpit-rules.png", title = "Rules", alt = "Concept screen of the Majordomus cockpit Rules view: a list of enforced repository rules with coverage, the detail of one rule, its validation status and where it is enforced.", caption = "Executable rules with their enforcement points: command line, CI, pre-commit hook." },
    { src = "assets/majordomus/cockpit-worktrees.png", title = "Worktrees", alt = "Concept screen of the Majordomus cockpit Worktrees view: parallel branches with their status, a diff of changed files, commits ahead and a terminal.", caption = "Parallel branches in their own worktrees, each tied to an issue and a session." },
  ] },
]
+++

Catharsis as a Service™ is the first work in an open series of Sig Nihl / Prismatic artifacts: finished pieces that treat human states the way engineers treat systems. Observed, named, measured, and still not fixed.

## What this is

A poster and a page. The poster sells a night of collective release. The page around it instruments that night: input, process, output, status. Both readings are true at once, and the piece only works if neither wins.

## What this is not

Not an event, not a product and not a critique of people who dance. The telemetry is conceptual; nothing here measures anyone. There is no analytics, no tracker and no cookie.

## Motivation

The project began with an observation about language. Relief is advertised in the vocabulary of services: on demand, repeatable, with a predictable response. A night out, a playlist, a scream room or a purchase is offered as the way to deal with what hurts. The relief is real. What troubled us is the silent promise that comes with it: that the feeling of release means the problem has been dealt with.

Psychology has studied exactly this gap for more than a century, from Breuer and Freud's cathartic method to controlled experiments on venting and to meta-analyses of emotion regulation. Its findings rarely reach the places where release is sold. The artwork makes the gap visible; the library around it explains what is known, how strongly, and where knowledge stops.

## The psychology behind it

The argument rests on a few well-studied ideas, each explained in its own note with references:

- **Catharsis as a concept** — its history from Aristotle to clinical practice: [What is catharsis](@/research/what-is-catharsis/index.md).
- **Venting** — why expressing anger through arousal tends to feed it: [The venting hypothesis](@/research/venting-hypothesis/index.md).
- **Relief versus resolution** — negative reinforcement and why relief can keep a problem in place: [Relief is not resolution](@/research/relief-is-not-resolution/index.md).
- **Collective experience** — synchrony, bonding and collective effervescence: [Collective synchrony](@/research/collective-synchrony/index.md) and [Music and emotion regulation](@/research/music-and-emotion-regulation/index.md).
- **Measurement** — what signals can and cannot say about a state: [Measuring emotion](@/research/measuring-emotion/index.md) and the [methods page](@/methods/index.md).

## Theory and background

Terms such as reappraisal, rumination, arousal or allostatic load are defined in the [glossary](@/glossary/index.md). Every claim the site makes is recorded in the [evidence ledger](@/evidence/index.md) with its sources, its strength and the date it must be reviewed again. The [advice library](@/advice/_index.md) turns that evidence into graded, limited recommendations.

The concept screens below show the kind of supervision cockpit Majordomus is developing. They are illustrations with invented data; the records of how this site was actually built are in the [method note](@/research/method-majordomus/index.md).

## Why a series

One poster is an opinion. A series is a method: the same diagnostic grammar (input, process, output, status) applied to different human rituals, so the differences between them become visible. The site is built so that the next artifact is a pair of Markdown files, not a redesign.

## Principles

- **The artwork leads.** The interface exists to frame the poster, never to compete with it.
- **Honest instruments.** Anything that looks like data is labelled as conceptual, and the page itself collects nothing.
- **Readable without scripts.** JavaScript adds view modes, an artwork viewer and a copy button; the content is complete without it.
- **Two languages, one structure.** English and Czech are equal editions, checked for parity on every build.
- **Claims need evidence.** Nothing is called deployed until the live URL has been tested.

## How it is built

Static HTML generated by [Zola](https://www.getzola.org/) from Markdown, styled with Tailwind CSS, with Flowbite and Alpine.js for the few interactive parts. Every push to `main` is validated, deployed to GitHub Pages, verified in a real browser against the live URL, and released with a version derived from its commits. The [guides](@/guides/index.md) explain each step and the reasoning behind it.

## How the work was supervised

The site was built by an AI coding agent working under [Majordomus](https://majordomus.dev), a supervisory layer between the agent and the repository. Majordomus did not write the site. It made the work accountable:

- **Scoped tasks.** Every change ran as a task with a declared scope. When files were moved outside that scope, [`majordomus watch`](../commands/#majordomus-watch) and [`majordomus check`](../commands/#majordomus-check) reported the drift before anything was pushed, and the task was restarted with a correct scope instead of being waved through.
- **Continuity.** Checkpoints and handovers recorded what had changed and what came next, so the work could be resumed from recorded facts rather than from memory.
- **A finish contract.** A task can only be closed as completed when its verification command passes. Here that command is the smoke test against the live site, so "done" means "live and checked".
- **Wired enforcement.** The `pre-commit` hook runs [`majordomus doctor`](../commands/#majordomus-doctor), the `pre-push` hook runs [`majordomus finish --check`](../commands/#majordomus-finish), and CI runs the same supervision check on every push and pull request.
- **Rules next to the code.** Project rules (live verification before any claim, Zola as the source of truth, releases only from verified `main`) live in `.ai/repo/rules/`, versioned with the code they govern.

The practical effect is fewer confident claims and more checked ones.

## Rights

© 2026 Sig Nihl. All rights reserved; no open license is granted for the artwork or the text. The fonts (Anton, JetBrains Mono, Barlow Condensed) are distributed under the SIL Open Font License 1.1.
