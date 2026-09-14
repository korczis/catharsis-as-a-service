+++
title = "Detection sandbox: what signals do not settle"
description = "Five synthetic signals, one setting, and every reading they support at once. Change the setting and the signals stay where they are while the leading interpretation changes, which is the point."
date = 2026-09-14
template = "sandbox.html"

[taxonomies]
tags = ["measurement", "inference", "epistemics", "simulation"]

[extra]
kicker = "Detection sandbox"
summary = "A working demonstration of the distance between a signal and a conclusion. You set five values, the sandbox derives four features from them by rules printed beside the numbers, and then it shows every reading those features support, ranked, with the arithmetic that ranked them. Change the setting from a concert to an emergency and the signals do not move while the leading reading does. Nothing is measured, recorded or sent."
key_points = [
  "The inputs are values you set. Nothing on this page reads a sensor, and nothing about you is computed, stored or transmitted.",
  "Derived features add no knowledge: each one restates the inputs by a rule shown next to it.",
  "A reading is never returned alone. The sandbox always shows the competing readings and says when the leading one is not separated from the next.",
  "The same signals under a different setting produce a different leading reading, because the setting supplies a prior the sensors cannot.",
  "The weights are illustrative. They were chosen to make the structure of the inference visible, not fitted to any dataset.",
]
references = ["barrett-2019", "siegel-2018", "mauss-robinson-2009", "stark-hoey-2021", "hoemann-2020"]
assumptions = [
  "Heart rate is read on a 50–190 scale and mapped linearly to 0–100 so that it can be averaged with the other signals; the remaining four are unitless 0–100 scales.",
  "Arousal is the mean of scaled heart rate, movement and vocal intensity; effort is the mean of scaled heart rate and movement; the synchrony feature is the alignment input unchanged.",
  "Each reading has a fixed prior per setting and a fit computed from the derived features; the share shown is prior times fit, normalised across the five readings.",
  "The priors and the fit expressions are invented. They encode direction — that anger fits high arousal with low alignment, that a collective reading fits high arousal with high alignment — and nothing about magnitude.",
  "Two readings within ten points of each other are reported as not separated, a threshold chosen for legibility rather than derived from anything.",
]
limits = [
  "This is not a classifier and must not be used as one. It ranks invented hypotheses under invented weights to show the shape of an inference, not to identify a state.",
  "Real affect recognition is harder than this, not easier: facial movements are not reliable indicators of emotion categories across people and contexts, and autonomic patterns do not clearly distinguish one emotion category from another.",
  "The five signals are a caricature of what a real system would record, and the four features are a caricature of what it would compute. A richer system would have the same problem in a less legible form.",
  "Nothing here says what the person being described means, why they feel it, or whether anything in their situation changed. Those are the questions that matter and no signal in this list reaches them.",
]

[extra.panel]
heading = "The sandbox"
intro = "Set the signals, choose the setting, and read the panel from left to right: what you set, what follows from it by rule, what it could mean, and what it cannot say."
unknown = [
  "What the person is experiencing from the inside, which no combination of these signals contains.",
  "Why they are in that state: the cause is not a property of the body, and the same body state follows from incompatible causes.",
  "Whether anything in their situation changed, which is the question this whole site is about and the one signals are silent on.",
  "Whether they want to be observed at all, which is a question about consent rather than about measurement.",
]

[extra.panel.labels]
figure = "Detection sandbox: five synthetic signals, the features derived from them, the competing readings they support and the questions they cannot answer."
banner = "Synthetic inputs · illustrative weights · nothing is measured or recorded"
nojs = "The sandbox needs JavaScript. Its rules are written out in the assumptions below, and the argument it demonstrates is stated in the text: the same signals support several readings, and the setting decides which one leads."
observed = "What you set"
observed_note = "These are values you chose, not readings from a device. The site records nothing and sends nothing."
kind_observed = "observed"
kind_derived = "derived"
kind_inferred = "inferred"
kind_unknown = "unknown"
context = "Setting"
context_concert = "Concert"
context_protest = "Protest"
context_sport = "Sports event"
context_emergency = "Emergency"
context_ritual = "Ritual"
signal_heart = "Heart rate (bpm)"
signal_movement = "Movement intensity"
signal_vocal = "Vocal intensity"
signal_alignment = "Rhythmic alignment with others"
signal_reported = "Self-reported activation"
reset = "Reset"
derived = "What follows by rule"
derived_arousal = "Arousal index"
derived_synchrony = "Synchrony index"
derived_effort = "Physical effort index"
derived_gap = "Body–report gap"
rule_arousal = "mean of scaled heart rate, movement and voice"
rule_synchrony = "the alignment input, unchanged"
rule_effort = "mean of scaled heart rate and movement"
rule_gap = "distance between the arousal index and the self-report"
inferred = "What it could mean"
inferred_note = "Every reading is shown, ranked by prior times fit. A share is not a probability that the state is present; it is this model's weight under its own invented numbers."
prior = "prior"
fit = "fit"
reading_collective = "High collective arousal"
reading_positive = "Possible positive affect"
reading_anger = "Possible anger"
reading_fear = "Possible fear"
reading_exertion = "Physical exertion"
undecided = "The leading reading is not separated from the next. On these signals the sandbox distinguishes nothing."
separated = "The leading reading is ahead of the next, under these invented weights and this setting."
alternatives = "The same signals, read elsewhere"
alternatives_note = "The inputs do not change. Only the setting does, and with it the prior that the sensors cannot supply."
unknown = "What no signal here settles"
vocabulary = "The six words used above"
[extra.lenses.essential]
heading = "What this shows"
body = "Signals do not carry conclusions. The panel takes five values you set and shows every reading they support at once; when you change nothing but the setting, the leading reading changes. That is the whole argument: the same body, read in a different place, means something different, and the sensors know nothing about the place."

[extra.lenses.practice]
heading = "For somebody who works with people"
body = "Nothing here assesses a person, and nothing here is a screening instrument. The sandbox exists to make the limits of inference visible, which matters when a device, an app or a service offers to report somebody's emotional state. Where the literature is summarised, it is the group-level finding with its population and its limits, and the clinical boundary is unchanged: distress that persists or includes thoughts of self-harm belongs with a qualified professional."

[extra.lenses.research]
heading = "The rules, in full"
body = "Every derived value is a stated function of the inputs, and every share is a prior multiplied by a fit and normalised. The priors and fits are invented; they encode direction, not magnitude. Nothing is estimated from data, and no parameter here was fitted to anything."
rules = [
  { name = "Arousal index", rule = "mean of heart rate scaled from 50–190 to 0–100, movement and vocal intensity" },
  { name = "Synchrony index", rule = "the rhythmic alignment input, unchanged" },
  { name = "Physical effort index", rule = "mean of scaled heart rate and movement" },
  { name = "Body–report gap", rule = "absolute difference between the arousal index and self-reported activation" },
  { name = "Share of a reading", rule = "prior for the setting × fit from the derived features, normalised across the five readings" },
]

[extra.lenses.technical]
heading = "The implementation"
body = "The computation is pure and deterministic: derive(signals) and hypotheses(derived, context) are functions of their arguments alone, exposed on window.caasSandbox so a test can call them without a browser page. The Alpine component holds state and asks them; the state is in the URL, so a configured sandbox can be linked."
model_label = "Model id"
implementation_label = "Implementation"
tests_label = "Tests"
state_label = "URL state"

[extra.lenses.epistemic]
heading = "What kind of thing each number is"
body = "The panel labels every part of itself with one of six words, and the labels are the point. What you set is observed only in the sense that you chose it. What the rules compute is derived and adds no knowledge. What the shares suggest is inferred and could be wrong. What the weights encode is illustrative. And the longest list on the page is the one headed by the sixth word."

+++

## Why a sandbox rather than a demonstration of accuracy

A system that reports an emotional state has done two separable things: it recorded something, and it concluded something. The first is engineering and the second is inference, and the gap between them is where almost every overclaim about emotion recognition lives.

This page takes that gap apart. The signals are yours to set, so nothing about the reader is involved. The features are computed by rules printed beside their outputs, so nothing is hidden in a model. And the readings are shown all at once, ranked but never reduced to one, because the honest output of this kind of inference is a spread rather than a verdict.

## The demonstration

Set the signals to something a concert would plausibly produce: a high heart rate, high movement, high alignment with the people nearby. Read the ranked list. Then change only the setting to an emergency. The signals have not moved by a single point, and the leading reading changes.

Nothing about the body changed. What changed is the prior that comes from knowing where the body is, and that prior is not available to any sensor in the list. A system deployed in a workplace, a school or a stadium inherits the same problem and usually hides it, because a single label reads as an answer while a ranked spread reads as an admission.

## What the research says about the real version of this

The sandbox is a caricature, and the underlying findings are not kinder to detection than the caricature is. A large review concluded that facial movements are not reliable, specific indicators of emotional states across people and contexts (Barrett et al., 2019). A meta-analysis of 202 studies found that autonomic responses did not clearly distinguish one emotion category from another (Siegel et al., 2018). There is no gold-standard measure to fall back on: experiential, physiological and behavioural measures converge only modestly and cannot be treated as interchangeable (Mauss & Robinson, 2009).

Systems built on those signals therefore rest on particular conceptual models of emotion and on proxy data, and those choices shape what the systems imply about people (Stark & Hoey, 2021). When repeated physiological sampling is done carefully in daily life, the patterns that recur within one person vary in number and in the labels attached to them (Hoemann et al., 2020).

## What to take from it

An inference can be honest about three things at once: what it saw, what it computed, and what it still does not know. The sandbox prints all three, and the third list is the longest. That is not a failure of the demonstration. It is the result.
