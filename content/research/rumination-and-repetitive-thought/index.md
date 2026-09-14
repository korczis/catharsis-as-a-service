+++
title = "Rumination and repetitive thought: why going over it again can feel like processing"
description = "Repetitive thought about a problem can be constructive or can sustain distress. This note reviews experiments, experience sampling and trials on rumination, the difference between abstract and concrete thinking, and why brooding feels like work."
date = 2026-09-14
weight = 15

[taxonomies]
tags = ["rumination", "repetitive thought", "emotion regulation", "problem solving", "depression"]

[extra]
kicker = "Research note 15"
summary = "Thinking repeatedly about a problem is not in itself harmful. Whether it helps depends on how the thinking is done: abstract, evaluative questions about why something happened tend to be unconstructive, while concrete, process-focused thinking about how it unfolded and what to do next can support problem solving. Experiments show that induced rumination worsens interpretation and problem solving in low mood, experience sampling shows that rumination and negative affect feed each other, and a trial targeting rumination improved residual depression. Rumination feels like processing because it is about the problem; what it usually lacks is new information, a decision or an action."
key_points = [
  "The consequences of repetitive thought depend on its valence, context and level of construal; abstract processing tends to be unconstructive and concrete processing can be constructive (Watkins, 2008).",
  "In three experiments, dysphoric students induced to ruminate made more negative interpretations and generated less effective solutions to interpersonal problems than those induced to distract (Lyubomirsky & Nolen-Hoeksema, 1995).",
  "Among 40 depressed patients, concrete rather than abstract self-focus improved social problem solving (Watkins & Moulds, 2005); in 93 adults sampled eight times a day, rumination and negative affect predicted each other, with brooding but not reflection associated with more negative affect (Moberly & Watkins, 2008).",
  "Adding rumination-focused CBT to usual treatment improved residual depression in a trial of 42 people, mediated by change in rumination (Watkins et al., 2011); a 30-minute daily worry period reduced worry, anxiety and insomnia in 53 high worriers (McGowan & Behar, 2013).",
]
references = ["watkins-2008", "nolen-hoeksema-2008", "aldao-2010", "lyubomirsky-nolen-hoeksema-1995", "watkins-moulds-2005", "moberly-watkins-2008", "watkins-roberts-2020", "watkins-2011", "mcgowan-behar-2013", "kross-ayduk-mischel-2005", "scott-2021"]

[[extra.figures]]
kind = "pipeline"
id = "fig-rumination-loop"
title = "The rumination loop"
description = "Flow diagram: an unresolved problem leads to abstract why-questions, replaying and lower mood; a dashed return arrow leads from lower mood back to the why-questions without new information."
caption = "Figure 1. Abstract repetitive thought as a loop: it is about the problem, so it feels like processing, but it adds no new information, decision or action. Conceptual illustration of Watkins (2008) and Moberly and Watkins (2008), not measured data."
nodes = [
  { label = "Unresolved|problem", meta = "input" },
  { label = "Why does|this happen?", meta = "abstract", mark = "feels like processing", alert = true },
  { label = "Replaying", meta = "01" },
  { label = "Lower mood", meta = "02" },
]
loop = { from = 3, to = 1, label = "no new information", meta = "decision: null" }

+++

## Why this belongs in a library about catharsis

The catharsis idea has a cognitive cousin. Where the hydraulic model says that an emotion must be let out, its cognitive version says that a painful experience must be *gone over* until it is processed. Going over it again, replaying the conversation, asking why it happened, imagining what should have been said, feels like doing exactly that. Much of the time it does not lead anywhere, and the evidence on [rumination](../../glossary/#rumination) helps explain why.

This note distinguishes kinds of [repetitive thought](../../glossary/#repetitive-thought), reviews experimental, experience-sampling and clinical evidence on their consequences, and addresses the question in its title: why unconstructive repetitive thought is so easily mistaken for processing.

## Not all repetitive thought is the same

Watkins (2008) reviewed the literature on repetitive thought, a broad category that includes rumination, worry, reflection, problem solving and mental rehearsal. Repetitive thought about oneself and one's concerns is common and can have either constructive or unconstructive consequences. The review proposed that the difference depends on three factors: the valence of the thought content, the context in which the thinking occurs, and the level of construal, that is, whether thinking is abstract or concrete.

The last factor is the most useful in practice. *Abstract* repetitive thought is evaluative and general: why does this always happen to me, what does it say about me, what if it never changes. *Concrete* repetitive thought is specific and process-focused: how exactly did the situation unfold, what happened just before things went wrong, what could be done differently next time. The review found that abstract processing tends to be associated with unconstructive outcomes, while concrete processing can support problem solving and recovery.

A related distinction appears in questionnaire research between *brooding*, a passive comparison of one's situation with some unachieved standard, and *reflection* or *reflective pondering*, a more purposeful turning inward to understand or solve a problem. The term is defined in the [glossary](../../glossary/#brooding).

## What rumination is associated with

Nolen-Hoeksema, Wisco and Lyubomirsky (2008) reviewed response styles theory and the research it generated. Rumination, a repetitive, passive focus on one's distress and its causes and consequences, predicts the onset of depressive episodes and is associated with several other forms of psychopathology; in experiments, positive distraction relieved depressed mood relative to rumination.

At the level of pooled evidence, Aldao, Nolen-Hoeksema and Schweizer (2010) meta-analysed 114 studies relating emotion regulation strategies to symptoms of anxiety, depression, eating and substance-related disorders. Rumination showed the largest association with symptoms of all strategies examined. Because most of the pooled studies are correlational, this establishes a robust association, not that rumination causes symptoms ([Research note 08](@/research/clinical-perspectives/index.md)).

Watkins and Roberts (2020) reviewed later research and summarised the consequences attributed to rumination: magnifying and prolonging negative mood, interfering with problem solving and instrumental behaviour, reducing sensitivity to changing contingencies, acting as a vulnerability across anxiety, depression, psychosis, insomnia and impulsive behaviour, interfering with therapy, and maintaining physiological stress responses. These are summaries of a large literature of varying designs, and the causal claims among them rest mainly on the experiments described next.

## Experiments: what induced rumination does

Correlations cannot show direction, so experiments that induce rumination are central. Lyubomirsky and Nolen-Hoeksema (1995) ran three studies with dysphoric and nondysphoric students, who were induced either to focus ruminatively on their feelings and personal characteristics or to distract themselves. In the first study, dysphoric participants who ruminated endorsed more negative, biased interpretations of hypothetical situations than dysphoric participants who distracted, or than nondysphoric participants. In the second, dysphoric ruminators were more pessimistic about positive events in their future. In the third, they generated less effective solutions to interpersonal problems. In all three studies, dysphoric participants who distracted were as optimistic and effective as nondysphoric participants.

The result matters for the catharsis question because the ruminative induction was, in content, an invitation to think about one's feelings. In low mood, that focus did not produce better understanding; it produced more negative interpretation and worse solutions.

Watkins and Moulds (2005) then asked whether the harm lay in focusing on symptoms at all or in the style of that focus. In 40 depressed patients and 40 never-depressed controls, they assessed social problem solving before and after versions of symptom-focused rumination known to induce either abstract or concrete self-focus. In depressed patients, concrete self-focus improved problem solving relative to abstract self-focus. The authors conclude that the particular mode of symptom focus, rather than symptom focus itself, determines the effect of rumination on problem solving. The same topic, thought about in a different mode, had a different consequence.

## Daily life: a loop between rumination and mood

Laboratory inductions last minutes. Moberly and Watkins (2008) used experience sampling to see how rumination and mood relate in ordinary life. Ninety-three adults recorded momentary ruminative self-focus and negative affect at quasi-random intervals eight times a day for a week. Dispositional rumination scores were associated with more momentary rumination over the week. At the same moment, rumination was positively associated with negative affect. Over time, ruminative self-focus predicted negative affect at the next occasion, and negative affect also predicted ruminative self-focus at the next occasion. Brooding, but not reflective pondering, was associated with higher mean negative affect.

The reciprocal pattern is consistent with a self-sustaining loop: low mood prompts rumination, and rumination deepens low mood. This is an association in repeated observations, not a demonstration of cause, but it fits the experimental findings and helps explain why rumination can persist for hours or days once it starts.

## Why going over it again feels like processing

The research above does not directly measure what ruminating feels like from the inside, so this section is an interpretation that is consistent with the evidence rather than a finding.

First, rumination is *about* the problem. It has the same topic as problem solving, and it often carries the intention to understand. Watkins (2008) emphasises that repetitive thought about a concern can be constructive, which makes it difficult to tell from within whether a particular episode is helping.

Second, abstract questions feel deep. "Why did this happen?" and "what does it mean about me?" seem more serious than "what will I say on Tuesday?" Yet the experiments show that it is the concrete mode that improved problem solving.

Third, Watkins and Roberts (2020) propose a model, which they call H-EX-A-GO-N, in which rumination develops from dwelling on unresolved goals into a learnt habit, involving the tendency to process negative information abstractly, particularly with poor executive control and negative biases in information processing. If rumination is partly a habit triggered by reminders of unresolved goals, it will start automatically and feel purposeful even when it produces nothing new. The model is a proposal that integrates experimental evidence, not an established account.

Fourth, rumination can bring a kind of temporary relief: the sense of having attended to the problem. Relief that follows a behaviour tends to make that behaviour more likely, whether or not it solves anything ([Research note 04](@/research/relief-is-not-resolution/index.md)). That link has not been tested directly for rumination in the sources cited here.

A practical test follows from this analysis. Processing tends to yield something: new information, a changed interpretation, a decision, or an action. A loop that returns to the same question in the same words, with the same feeling, and yields none of these is more likely to be rumination than processing.

## What reduces unconstructive repetitive thought

Several lines of evidence point to ways of changing rumination rather than trying to exhaust it.

**Changing the mode.** The experiments above show that shifting from abstract to concrete thinking about the same problem changed its effect on problem solving. Asking how, specifically, rather than why, is the core of this shift.

**Changing the perspective.** Kross, Ayduk and Mischel (2005) found that reflecting on an upsetting experience from a self-distanced perspective, as an observer, reduced emotional reactivity and rumination compared with immersed recall.

**Changing attention.** In the experiments of Lyubomirsky and Nolen-Hoeksema, distraction left dysphoric participants as optimistic and effective as nondysphoric participants, and the review by Nolen-Hoeksema and colleagues reports that positive distraction relieved depressed mood. Distraction does not solve the problem, but it can interrupt the loop long enough for concrete thinking to become possible later.

**Containing it in time.** McGowan and Behar (2013) randomly assigned 53 people with high trait worry to two weeks of stimulus control training, a 30-minute time- and place-restricted worry period each day, or to a control condition of focused worry, in which participants were instructed not to avoid naturally occurring worry. Stimulus control produced greater reductions in worry, anxiety, negative affect and insomnia, though not in depression or positive affect. The study concerns worry rather than rumination, is small and preliminary, and cannot show long-term effects.

**Treatment that targets rumination.** Watkins and colleagues (2011) randomised 42 people with medication-refractory residual depression to treatment as usual or treatment as usual plus up to 12 sessions of rumination-focused cognitive-behavioural therapy. Adding the rumination-focused therapy improved residual symptoms and remission rates, and the effects were mediated by change in rumination. The trial lacked an attentional control group, so it cannot separate the specific content of the therapy from non-specific effects of additional therapy.

**Sleep.** In a meta-analysis of 65 trials, interventions that improved sleep also reduced rumination (g+ = -0.49) (Scott et al., 2021; [Research note 13](@/research/sleep-and-emotion-regulation/index.md)).

## Relevance to catharsis

Rumination and venting share a structure. Both keep attention on the source of distress, both feel like doing something about it, and both can be followed by a sense of having discharged or processed something. In the venting experiments, hitting a bag while thinking about the provocateur, a combination of exertion and rumination, produced the most anger ([Research note 02](@/research/venting-hypothesis/index.md)). In the rumination experiments, focusing on one's feelings in low mood produced more negative interpretation and worse problem solving.

The alternative in both cases is not suppression. It is a change in how the problem is held: concretely rather than abstractly, from a distance rather than immersed, in a bounded time rather than all day, and with a view to a next step.

## Practical implications, with limits

- **Notice the loop.** The same question, in the same words, with no new information, is a signal to change mode.
- **Switch from why to how.** Describe concretely what happened, when and in what sequence, and what could be done next.
- **Step back.** Describe the situation as an observer would.
- **Set a time for it.** If nothing can be done now, postpone the concern to a fixed, limited period.
- **Use absorbing activity to interrupt.** Distraction is not a solution, but it can break the loop.

These are reasoned from the evidence; the combination has not been tested as a package, and the advice on [interrupting rumination with concrete steps](@/advice/interrupt-rumination-with-concrete-steps/index.md) sets out its limits. Rumination that persists for weeks with low mood or anxiety warrants professional assessment; structured treatments that target it exist.

## Limits of the evidence

Most evidence linking rumination with symptoms is correlational. Experimental inductions are brief and mostly conducted with students or small clinical samples. The experience-sampling study shows reciprocal association, not cause. The treatment trial was small and lacked an attentional control, and the worry study was preliminary and concerned worry. The explanation of why rumination feels like processing is an interpretation consistent with the evidence, not a measured finding. The [evidence ledger](@/evidence/index.md) records the grade and review date of each claim.
