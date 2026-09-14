+++
title = "Does this site measure my emotions?"
description = "No. The numbers in the artwork are artistic values, the site carries no analytics scripts, trackers or cookies, and the source is public so this can be checked rather than believed."
date = 2026-09-14
weight = 12

[taxonomies]
tags = ["privacy", "artwork", "emotion AI", "transparency"]

[extra]
kicker = "Question 12"
short_answer = "No. Every metric, status value and chart in the artwork is an artistic value chosen to express a relationship, not a measurement of anyone. The site contains no analytics scripts, trackers or cookies, and because the source code is public you can verify that instead of trusting it. The hosting provider may keep its own server logs, which this project does not control."
related_questions = ["faq/can-emotions-be-measured/index.md", "faq/why-an-artwork/index.md", "faq/how-this-was-built/index.md"]
read_next = ["research/measuring-emotion/index.md", "artifacts/catharsis-as-a-service/index.md", "methods/index.md", "detection-sandbox/index.md"]
references = ["repository-2026", "stark-hoey-2021", "picard-1997"]
+++

## What the numbers in the artwork are

The artwork borrows the vocabulary of an observability dashboard: input state, synchronisation, root cause, a chart that climbs and falls. None of it is data. Every metric, status value and chart in the artwork, and the relief figures elsewhere on the site, are artistic or conceptual values chosen to express a relationship. They were designed to resemble telemetry, which is exactly why they carry the ARTISTIC label wherever they appear, and why they must never be quoted as findings.

The simulation on the methods page works the same way: it runs on invented inputs and says so on its face. Nothing on this site takes a reading from a visitor, and nothing is inferred about one.

## What the site is technically

It is a static site. Pages are generated ahead of time from Markdown and templates and served as files; there is no application collecting anything at the other end. It contains no analytics scripts, no trackers and no cookies.

That claim is the kind that should not be taken on trust, so it is made checkable. The source code is public. You can read the templates and the built HTML, search them for third-party script tags, and open your browser's network panel while loading a page to see which hosts are contacted. Verification beats assurance, and this is the form of assurance that can be turned into verification.

There is one honest limit. The hosting provider serves the files, and a provider may keep its own server logs — request times, addresses, user agents — as part of operating a web server. That is outside this project's control and not something it can promise about on the provider's behalf.

## Why a site about emotion refuses to measure

Rosalind Picard framed affective computing as a research field in 1997, and it has produced serious work. It has also produced systems sold on the promise of inferring emotional states from faces, voices and physiological signals. Stark and Hoey's argument is that such systems are built on contested models of emotion and on proxy data, and that these choices — which model, which proxy — shape the ethical and social implications of what gets built. It is a conceptual argument about the field, not an audit of particular products.

Two reasons follow for this project. The first is validity: the syntheses on measurement do not support inferring a specific emotional state from any single recorded signal, so a dashboard here would be presenting error as precision. The second is consent: someone reading an essay about catharsis has not agreed to be analysed, and an artwork that quietly did so would be enacting the thing it criticises.

So the artwork keeps the interface and drops the measurement. The gauges move because a designer decided they should, and the page says so.
