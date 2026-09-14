+++
title = "Instrumented emotion: why the telemetry here is conceptual"
description = "Affective computing promises to infer emotion as if it were a system metric. The evidence on facial movements and autonomic signals, together with questions of consent, explains why every metric in this artifact is an artistic value."
date = 2026-09-14
weight = 5

[taxonomies]
tags = ["affective computing", "measurement", "ethics", "emotion"]

[extra]
kicker = "Research note 05"
summary = "The artifact borrows the language of dashboards but refuses to measure anyone. Research reviewed by Barrett and colleagues shows that emotional states cannot be reliably inferred from facial movements, and a visitor to an artwork has not consented to being analysed. The page therefore labels every metric as an artistic value and collects nothing."
key_points = [
  "Affective computing studies systems that recognise and respond to emotion (Picard, 1997) and has produced a commercial market for emotion recognition.",
  "A large review concluded that facial movements are not reliable, specific indicators of particular emotional states across people and contexts (Barrett et al., 2019).",
  "A meta-analysis of 202 studies found that autonomic effect sizes did not clearly distinguish one emotion category from another (Siegel et al., 2018), although an earlier narrative review reported specificity at the level of emotion subtypes (Kreibig, 2010).",
  "In a meta-analysis, six classic basic emotions did not reliably co-occur with their predicted facial expressions: average co-occurrence effect sizes were .13 for full expressions and .23 when partial expressions were included (Durán & Fernández-Dols, 2021).",
  "Experience, facial behaviour and physiology are only partly coherent: in a film study, physiology was only modestly associated with experience and behaviour (Mauss et al., 2005), and no single measure is a gold standard (Mauss & Robinson, 2009).",
  "A meta-analysis of neuroimaging studies found little evidence that discrete emotion categories are consistently and specifically localised to distinct brain regions (Lindquist et al., 2012).",
  "Outside the laboratory, physiological signs of emotion can be masked by social engagement, workload, food intake and circadian variation (Wilhelm & Grossman, 2010).",
  "Validity, consent and coherence are the three reasons this site presents conceptual values instead of measurements.",
]
figures = []
references = ["picard-1997", "barrett-2019", "duran-2021", "watson-1988", "bradley-lang-1994", "kreibig-2010", "siegel-2018", "mauss-2005", "mauss-robinson-2009", "lindquist-2012", "trull-2013", "wilhelm-grossman-2010", "hoemann-2020", "stark-hoey-2021"]
+++

## The appeal of emotion as data

Dashboards promise that anything important can be observed, quantified and graphed. The artifact borrows that language on purpose: *input state*, *synchronization*, *root cause*. It then declines to deliver the measurement. This note explains why.

## Affective computing

In 1997 Rosalind Picard described *affective computing*, the study and development of systems that can recognise, interpret and respond to human emotion. The field has produced valuable research on emotion, human–computer interaction and assistive technology. It has also given rise to commercial products that claim to infer emotional states from faces, voices, text and physiological signals, often at scale and in public settings.

## The evidence problem

Barrett, Adolphs, Marsella, Martinez and Pollak (2019) reviewed the scientific evidence behind the common assumption that particular emotions are reliably expressed by particular facial configurations, for example that a scowl signals anger. They examined studies of how people move their faces when they experience emotions and studies of how observers infer emotions from faces.

Their conclusion was that people do, on average, scowl when angry or smile when happy more often than would be expected by chance, but the relationship is weak and inconsistent. The same facial configuration can accompany different emotional states, the same emotional state can be expressed in many ways, and the relationship varies substantially across contexts, individuals and cultures. A facial configuration alone therefore cannot be treated as a reliable readout of a specific internal state. The authors cautioned that technologies built on that assumption are not justified by the evidence.

A later [meta-analysis](../../glossary/#meta-analysis) approached the same question from the side of emotional experience. Durán and Fernández-Dols (2021) tested whether happiness, sadness, anger, disgust, fear and surprise each co-occur with the facial expression predicted for them. In studies that coded full expressions with the Facial Action Coding System (FACS), the average co-occurrence [effect size](../../glossary/#effect-size) was .13. Including partial expressions and other coding systems raised it to .23, and the average correlation between the reported intensity of an emotion and the intensity of its predicted expression was .30. Co-occurrence was greatest for disgust and least for surprise, and results varied between samples. The authors concluded that the six classic basic emotions do not reliably co-occur with their predicted facial signal.

## Asking people: self-report scales

Asking a person is the most direct route to how an experience feels, and several instruments are designed to make that brief and checkable. The Positive and Negative Affect Schedule (PANAS) consists of two 10-item mood scales. In the study that introduced it, the scales were highly internally consistent, largely uncorrelated with each other and stable at appropriate levels over a two-month period (Watson, Clark & Tellegen, 1988). The Self-Assessment Manikin (SAM) is a non-verbal pictorial technique that asks for only three judgements: pleasure, arousal and dominance. Compared with a semantic differential scale that requires 18 ratings, reports of experienced pleasure and felt arousal correlated highly across the two methods (Bradley & Lang, 1994).

Reliability of this kind shows that a scale measures something consistently. It does not show that a report matches what happened in the body, and it does not remove the dependence of [self-report](../../glossary/#self-report) on timing and on beliefs about emotion that the [methods page](@/methods/index.md) describes.

## Are bodily signals any clearer?

If faces are unreliable, physiology might seem a better source: heart rate, skin conductance, breathing and blood pressure are measured by instruments rather than judged by observers. The question is whether particular emotion categories have consistent autonomic patterns, sometimes called *fingerprints*, that would allow the category to be inferred from the signals.

Kreibig (2010) reviewed 134 publications reporting experiments on emotional effects on peripheral physiological responding in healthy people. The review suggested considerable autonomic response specificity in emotion when subtypes of distinct emotions are considered, and emphasised that sound terminology for the affective states studied and the choice of physiological measures are both important for assessing it. In other words, the review found patterns, but they depended on how finely emotions were defined and what was measured.

Siegel and colleagues (2018) tested the fingerprint hypothesis directly with a meta-analysis of 202 studies measuring autonomic reactivity during laboratory emotion inductions in non-clinical adult samples. Mean effect sizes increased for 59.4% of autonomic variables across emotion categories, but the pattern of effect sizes did not clearly distinguish one emotion category from another. Variation within categories was substantial: heterogeneity accounted for a moderate to substantial share of variability (I² of at least 30%) in 54% of the effect sizes. Experimental features such as whether emotion was induced with films or imagery did not explain much of that variation, and correcting for publication bias reduced the estimated effects further. The authors interpret the results as more consistent with the view that an emotion category is a population of variable, context-specific instances than with fixed fingerprints.

The two reviews are not simply contradictory. They differ in method (a narrative review versus a quantitative meta-analysis with pattern classification) and in the level of description (subtypes versus broad categories). Together they support a practical conclusion: emotion is accompanied by bodily change, but inferring a specific emotion from autonomic signals alone, outside controlled conditions and without context, is not supported by consistent evidence. A rising heart rate is a [signal](../../glossary/#signal); calling it fear, excitement or anger is an [inference](../../glossary/#inference) that needs other information. The [methods page](@/methods/index.md) describes how this library separates signals, inferences and claims.

## Do the channels agree?

Emotion theories commonly assume that an emotion organises experience, behaviour and physiology into one coherent response. Mauss, Levenson, McCarter, Wilhelm and Gross (2005) tested this within individuals, recording experience, facial behaviour and peripheral physiology second by second while participants watched a film that induced amusement and sadness. Experience and behaviour were highly associated, but physiological responses were only modestly associated with either. Greater intensity of amusement was associated with greater coherence between behaviour and physiology; greater intensity of sadness was not.

A review of experiential, physiological and behavioural measures reached a related conclusion. Each response system carries unique sources of variance, which limits how far measures converge, so there is no gold-standard measure and the three kinds of measure cannot be assumed to be interchangeable (Mauss & Robinson, 2009). The same review found that the bulk of the available evidence favours measures reflecting dimensions rather than discrete states. For any monitor this has two consequences: a physiological channel cannot stand in for self-report, and agreement between channels cannot be assumed where it has not been checked.

## What neuroimaging adds

Brain imaging is sometimes presented as a way around these limits. Lindquist, Wager, Kober, Bliss-Moreau and Barrett (2012) pooled the neuroimaging literature on human emotion to compare two hypotheses: that each discrete emotion category consistently and specifically corresponds to distinct brain regions, and that emotion categories are constructed from more general networks that are not specific to any category. They found little evidence that discrete emotion categories can be consistently and specifically localised to distinct brain regions. Instead, a set of interacting regions that are also involved in non-emotional psychological operations was active during the experience and perception of a range of emotion categories. As with bodily signals, reading a state back from the activity of a region is a [reverse inference](../../glossary/#reverse-inference), whose limits the [methods page](@/methods/index.md) explains.

## Outside the laboratory

Measuring emotion in everyday life replaces some laboratory problems with others. Ambulatory assessment gathers self-report, observational and physiological data from people in their natural environment, in real time or near real time. That minimises retrospective bias and yields ecologically valid data, and it raises questions of acceptability, compliance, privacy and ethics (Trull & Ebner-Priemer, 2013). Wilhelm and Grossman (2010) describe how emotional effects in physiological recordings can be masked by social engagement, mental and physical workload, food intake, and circadian and quasi-random variation in metabolic activity, so meaningful interpretation requires a high degree of context specification.

Hoemann and colleagues (2020) used physiologically triggered experience sampling: when cardiac activity changed substantially in the absence of movement, participants' self-reports and peripheral physiological activity were recorded. Clustering analyses revealed variability in the number and nature of physiological patterns that recurred within individuals, and in the affect ratings and emotion labels associated with each pattern; some broad patterns also recurred across individuals. The authors read the findings as support for the view, also taken by Siegel and colleagues, that emotion categories are populations of variable instances tied to situation-specific needs.

## Why the artifact does not measure

**Validity.** Inferring internal states from observable signals is least reliable in exactly the conditions a crowd provides: noise, movement, varied lighting, intoxication, diverse individuals and rapidly changing contexts. Even in everyday recordings of a single person, physiological signs of emotion can be masked by social engagement, workload, food intake and circadian variation (Wilhelm & Grossman, 2010). Stark and Hoey (2021) add that emotion-AI systems rest on particular conceptual models of emotion and on proxy data, that these choices shape the systems' ethical and social implications, and that the paradigms computer scientists have developed or adapted should not be taken at their word as producing ground truth about human emotions.

**Consent.** A person looking at an artwork has not agreed to have their emotional state analysed, stored or displayed. A piece about instrumenting people should not quietly instrument its own audience.

**Coherence.** The artifact is about the difference between a successful response and a solved problem. Producing confident numbers it cannot justify would repeat the very confusion it describes.

The [detection sandbox](@/detection-sandbox/index.md) turns this argument into something you can operate. It takes five synthetic signals, shows the features derived from them and every reading they support at once, and lets you change only the setting to watch the leading reading change while the signals stay where they are. Nothing in it measures anyone.

## How to read the numbers on the page

Every metric in the observability table is an artistic value, chosen to express a relationship rather than to report an observation. Relief is shown high but marked temporary. The root cause is shown at full scale and marked unchanged. The page states this next to the table, and the site contains no analytics, trackers or cookies, which can be verified in its source code.
