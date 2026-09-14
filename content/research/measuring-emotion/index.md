+++
title = "Instrumented emotion: why the telemetry here is conceptual"
description = "Affective computing promises to read emotion like a system metric. The evidence on inferring emotion from facial movements, together with questions of consent, explains why every metric in this artifact is an artistic value."
date = 2026-09-14
weight = 5

[taxonomies]
tags = ["affective computing", "measurement", "ethics", "emotion"]

[extra]
kicker = "Research note 05"
summary = "The artifact borrows the language of dashboards but refuses to measure anyone. Research reviewed by Barrett and colleagues shows that emotional states cannot be reliably read from facial movements, and a visitor to an artwork has not consented to being analysed. The page therefore labels every metric as an artistic value and collects nothing."
key_points = [
  "Affective computing studies systems that recognise and respond to emotion (Picard, 1997) and has produced a commercial market for emotion recognition.",
  "A large review concluded that facial movements are not reliable, specific indicators of particular emotional states across people and contexts (Barrett et al., 2019).",
  "Validity, consent and coherence are the three reasons this site presents conceptual values instead of measurements.",
]
figures = []
references = ["picard-1997", "barrett-2019"]
+++

## The appeal of emotion as data

Dashboards promise that anything important can be observed, quantified and graphed. The artifact borrows that language on purpose: *input state*, *synchronization*, *root cause*. It then declines to deliver the measurement. This note explains why.

## Affective computing

In 1997 Rosalind Picard described *affective computing*, the study and development of systems that can recognise, interpret and respond to human emotion. The field has produced valuable research on emotion, human–computer interaction and assistive technology. It has also given rise to commercial products that claim to infer emotional states from faces, voices, text and physiological signals, often at scale and in public settings.

## The evidence problem

Barrett, Adolphs, Marsella, Martinez and Pollak (2019) reviewed the scientific evidence behind the common assumption that particular emotions are reliably expressed by particular facial configurations, for example that a scowl signals anger. They examined studies of how people move their faces when they experience emotions and studies of how observers infer emotions from faces.

Their conclusion was that people do, on average, scowl when angry or smile when happy more often than would be expected by chance, but the relationship is weak and inconsistent. The same facial configuration can accompany different emotional states, the same emotional state can be expressed in many ways, and the relationship varies substantially across contexts, individuals and cultures. A facial configuration alone therefore cannot be treated as a reliable readout of a specific internal state. The authors cautioned that technologies built on that assumption are not justified by the evidence.

## Why the artifact does not measure

**Validity.** Inferring internal states from observable signals is least reliable in exactly the conditions a crowd provides: noise, movement, varied lighting, intoxication, diverse individuals and rapidly changing contexts.

**Consent.** A person looking at an artwork has not agreed to have their emotional state analysed, stored or displayed. A piece about instrumenting people should not quietly instrument its own audience.

**Coherence.** The artifact is about the difference between a successful response and a solved problem. Producing confident numbers it cannot justify would repeat the very confusion it describes.

## How to read the numbers on the page

Every metric in the observability table is an artistic value, chosen to express a relationship rather than to report an observation. Relief is shown high but marked temporary. The root cause is shown at full scale and marked unchanged. The page states this next to the table, and the site contains no analytics, trackers or cookies, which can be verified in its source code.
