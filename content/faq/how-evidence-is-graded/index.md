+++
title = "How do you grade the evidence?"
description = "Every substantive claim on this site has a ledger entry with an evidence level from A to E, a separate confidence rating, its sources, scope, caveat and review date. A claim past its review date fails the build."
date = 2026-09-14
weight = 16

[taxonomies]
tags = ["evidence", "methods", "verification"]

[extra]
kicker = "Question 16"
short_answer = "Every substantive claim has an entry in the evidence ledger: an evidence level from A to E based on the design of its sources, a separate confidence rating of HIGH, MODERATE, LOW or UNKNOWN, plus scope, caveat and sources. A claim is never graded stronger than its best source. Each entry carries a review date, and a claim past that date fails the build until someone re-examines it."
related_questions = ["faq/how-this-was-built/index.md", "faq/why-an-artwork/index.md", "faq/is-this-medical-advice/index.md"]
read_next = ["evidence/index.md", "methods/index.md"]
+++

## Two steps, two different questions

Grading happens in two steps, and they answer different questions.

First, each source is graded by design. A meta-analysis or systematic review of controlled studies is **level A**. One or more randomised or controlled experiments, usually with short-term outcomes and specific samples, is **level B**. Prospective, longitudinal or quasi-experimental studies, including uncontrolled pre-post comparisons, are **level C**. Cross-sectional, correlational or qualitative studies, narrative reviews and theoretical work are **level D**. Classical and historical texts, expert opinion, project records, policy statements and artistic material are **level E**.

One consequence is worth spelling out: a synthesis is graded by what it pools, not by the word "meta-analysis" in its title. A meta-analysis of correlational studies is graded by the design of those studies.

Second, each claim receives an evidence level no stronger than its strongest source, and a separate confidence rating. The level describes the kind of study behind the claim. Confidence describes how well the claim, as worded, is supported.

## The four confidence values

- **HIGH** — the claim, as worded, is well supported and further research is unlikely to reverse it.
- **MODERATE** — the claim is supported, but results are limited, heterogeneous, disputed or not fully re-verified.
- **LOW** — the claim rests mainly on theory or indirect evidence and could change with new research.
- **UNKNOWN** — the available evidence is insufficient to judge the claim.

Because the two ratings are independent, they come apart in useful ways. A meta-analysis with heterogeneous results can support a level A claim held at moderate confidence. A well-replicated correlation can be level D and still justify high confidence, provided the claim speaks of association and not of cause. That proviso is where most of the editorial work happens: the same data supports a strong claim about association and a weak one about cause.

## What a ledger entry contains, and what expires

Each entry records the claim's wording in both languages, its type, its evidence level, its confidence, its sources, its scope, its most important caveat, the pages where it appears, and the dates of its last and next review. Bibliographic facts are kept separately in the reference registry, checked against Crossref, because a citation and a judgement about a source go out of date on different schedules.

Review intervals depend on the claim type. Clinical-boundary claims are reviewed at least every 180 days, empirical claims every 365 days, and theoretical, historical, technical and artistic claims every 730 days. An automated check runs every week and on every change; a claim or source past its review date fails the build until someone re-examines it and records the outcome in the evidence changelog.

That is the part that makes the rest more than a promise. A stale claim does not sit quietly on a page — it stops the site from being published.

## Art is labelled, not graded upward

The site is an artwork as well as a library, so the ledger labels statements by type. A claim marked ARTISTIC belongs to the artwork and expresses a thesis; it is never a measurement of anyone. A claim marked EMPIRICAL reports what studies observed, with sources and limits. Keeping the labels visible protects both sides: the artwork can use the language of dashboards without its numbers being read as data, and the research notes are not lent false authority by the artwork's rhetoric.

If a claim looks outdated, overstated or wrongly sourced, the ledger page carries a report link.
