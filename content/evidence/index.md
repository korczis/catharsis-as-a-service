+++
title = "Evidence ledger"
description = "Every public claim on this site with its type, evidence level, confidence, sources and review date, and an appraisal of each reference. How claims are graded, how art is kept apart from evidence, and how to report a problem."
date = 2026-09-14
template = "evidence.html"

[taxonomies]
tags = ["evidence", "methods", "verification"]

[extra]
kicker = "Evidence"
summary = "The evidence ledger lists every substantive claim this site makes, from landing-page findings to advice and the artwork, together with the sources it rests on. Each source is appraised by design and graded from A to E; a claim can never be graded stronger than its best source. Confidence is a separate judgement of how well the claim, as worded, is supported. Every claim carries a review date, and a claim past that date fails the build until it is re-examined."
levels = [
  { level = "A", name = "Systematic synthesis", text = "A meta-analysis or systematic review of controlled studies. Syntheses of correlational studies are graded by the design of the studies they pool." },
  { level = "B", name = "Controlled experiment", text = "One or more randomised or controlled experiments, usually with short-term outcomes and specific samples." },
  { level = "C", name = "Longitudinal or quasi-experimental", text = "Prospective, longitudinal or quasi-experimental studies, including uncontrolled pre-post comparisons." },
  { level = "D", name = "Correlational, qualitative or theoretical", text = "Cross-sectional, correlational or qualitative studies, narrative reviews and theoretical work." },
  { level = "E", name = "Classical, expert or record", text = "Classical and historical texts, expert opinion, project records, policy statements and artistic material." },
]
confidence = [
  { value = "HIGH", text = "The claim, as worded, is well supported and further research is unlikely to reverse it." },
  { value = "MODERATE", text = "The claim is supported, but results are limited, heterogeneous, disputed or not fully re-verified." },
  { value = "LOW", text = "The claim rests mainly on theory or indirect evidence and could change with new research." },
  { value = "UNKNOWN", text = "The available evidence is insufficient to judge the claim." },
]
claim_types = [
  { id = "empirical", name = "Empirical", text = "A statement about what studies observed. Reviewed at least every 365 days." },
  { id = "theoretical", name = "Theoretical", text = "A definition, framework or argument that organises findings without being a single finding. Reviewed every 730 days." },
  { id = "historical", name = "Historical", text = "A statement about the history of an idea or practice. Reviewed every 730 days." },
  { id = "clinical-boundary", name = "Clinical boundary", text = "A statement about the limits of self-help and when professional help is needed. Reviewed every 180 days." },
  { id = "technical", name = "Technical", text = "A statement about how the site or a measurement method works, backed by records or methods literature. Reviewed every 730 days." },
  { id = "artistic", name = "Artistic", text = "A statement belonging to the artwork. It expresses a thesis and is not a finding. Reviewed every 730 days." },
]
review_policy = "Clinical-boundary claims are reviewed at least every 180 days, empirical claims every 365 days, and theoretical, historical, technical and artistic claims every 730 days. An automated check runs every week and on every change; a claim or source past its review date fails the build until someone re-examines it and records the outcome in the evidence changelog."
report_label = "Report an outdated or incorrect claim"
+++

## Why a ledger

A site that argues that relief is not resolution has to hold its own statements to the same standard. It is easy to write "research shows" and much harder to say which research, of what design, with which limits, and when someone last checked. The ledger answers those questions in one place.

Every substantive public claim on the site has an entry: the four findings on the landing page, the answers to frequently asked questions, the key points of each research note, the recommendation in each advice entry, the statements made by the artwork and the technical statements about the site itself. Each entry records the claim's wording, its type, its evidence level, a confidence judgement, its sources, its scope, its most important caveat, the pages where it appears and the dates of its last and next review.

Bibliographic facts and judgement are kept apart. The reference registry holds titles, authors and DOIs checked against Crossref. The ledger holds the appraisal of each source, including its design, population and main limitation, and that appraisal is dated because judgement can go out of date even when a citation does not.

## How a claim is graded

Grading happens in two steps.

First, each source is graded by design. A meta-analysis of randomised trials is level A; a single controlled experiment is level B; a longitudinal or uncontrolled pre-post study is level C; correlational, qualitative, narrative-review and theoretical work is level D; classical texts, project records and artistic material are level E. A meta-analysis that pools correlational studies is graded by what it pools, not by the word "meta-analysis" in its title.

Second, each claim receives an evidence level no stronger than its strongest source, and a separate confidence rating. The two answer different questions. The level describes the kind of study behind the claim. Confidence describes how well the claim, as worded, is supported. A meta-analysis with heterogeneous results can support a level A claim held at moderate confidence. A well-replicated correlation can be level D and still justify high confidence, provided the claim speaks of association and not of cause.

When a source's abstract could not be retrieved, the ledger says so, states no sample sizes for it and lowers confidence in claims that rely on it. When wording on a page went further than its sources, the ledger records the stricter version and the changelog notes the revision.

## Relief, resolution and the limits of evidence

Most of the research cited here measures short-term outcomes in specific samples: anger minutes after a provocation, closeness after a dance, mood after a film. That evidence is suited to questions about relief. It is much less suited to questions about resolution, which unfold over months in circumstances no laboratory reproduces. Where the ledger says there is insufficient evidence, that is a finding about the literature, not a verdict on the experience.

## Art and evidence on the same site

The site is both an artwork and a library, and the two use different kinds of statements. The ledger marks them explicitly. A claim labelled ARTISTIC belongs to the artwork: the telemetry values, the status line and the field `problem_solved: false` express a thesis and are never measurements of anyone. A claim labelled EMPIRICAL reports what studies observed, with sources and limits. Theoretical, historical, technical and clinical-boundary claims sit between them and are labelled as well.

Keeping the labels visible protects both sides. The artwork can use the language of dashboards without its numbers being quoted as data, and the research notes can be read without the artwork's rhetoric lending them false authority.

## How to report a problem

If a claim seems outdated, overstated or wrongly sourced, use the report link on this page. A useful report names the claim, explains what is wrong and, where possible, cites a newer or better source. Reports are checked against the original publications. Confirmed problems lead to a revised, downgraded or retracted claim, and the change is recorded in the evidence changelog with its date and reason.

The content of this site is general education, not medical advice. If distress persists, disrupts daily life or includes thoughts of harming yourself, contact a qualified professional or local emergency services.
