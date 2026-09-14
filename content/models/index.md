+++
title = "Interactive models: what relief, arousal, memory and synchrony do over time"
description = "Five interactive models, computed in your browser from values you set, show how relief can strengthen a habit, how arousal shapes anger, how memory weighs peaks and endings, how rhythms fall into step and how stress load accumulates."
date = 2026-09-14
template = "models.html"

[taxonomies]
tags = ["models", "simulation", "theory", "relief", "synchrony"]

[extra]
kicker = "Interactive models"
summary = "Several arguments on this site are about processes that unfold over time: relief that returns, anger that fades, memories that favour endings, rhythms that fall into step and stress that accumulates. This page turns five of those ideas into small models that you can run and change. Each model states its rules and assumptions openly, so you can see exactly where its behaviour comes from. The inputs are invented, the outputs are illustrative, and nothing here describes or assesses any real person."
banner = "Illustrative models · not predictions about any person"
key_points = [
  "Every number on this page is computed in your browser from values you set; none comes from a person, a device or a study dataset.",
  "Each model turns one idea from research into a few explicit rules, so the rules can be inspected, varied and questioned.",
  "Where a model draws on empirical findings, its curves follow the direction of those findings, not their size or their timing.",
  "A model that behaves plausibly is not evidence that people behave that way; the evidence is in the cited studies, not in the curves.",
]
references = ["rescorla-wagner-1972", "hayes-1996", "kjaervik-bushman-2024", "bushman-2002", "kahneman-1993", "fredrickson-kahneman-1993", "kuramoto-1984", "strogatz-2000", "wiltermuth-heath-2009", "tarr-2015", "mcewen-1998"]

[[extra.models]]
id = "relief-loop"
title = "The relief loop"
question = "What happens to the urge to repeat a relieving behaviour when the cause of distress stays the same, and what changes when the cause itself changes?"
explanation = "Negative reinforcement strengthens a behaviour that removes an unpleasant state, whether or not the behaviour touches the source of that state. The model reduces this to one quantity, the urge to repeat, which grows after each episode by a share of the distance still left to its maximum, scaled by the size of the relief. That update borrows the error-correcting form of the Rescorla–Wagner model of conditioning in simplified form. While the cause persists, distress returns to the same baseline before every episode, so the habit can grow without anything changing in what it responds to. Try strong relief with no chance of change, then keep the relief and raise the chance that the cause changes."
reading = "Each episode has two distress values: the level before the relief behaviour and the lower level just after it, and the gap between them is the relief. The level before each episode stays flat until the cause changes. The urge line shows how strongly the behaviour has been learned, from none to its maximum."
assumptions = [
  "Distress before each episode is fixed at 70 out of 100 while the cause persists and at 20 once it has changed.",
  "Relief is the same size in every episode and has worn off completely by the next one.",
  "The urge grows by 15% of the remaining distance to its maximum, scaled by relief divided by 100; after the cause changes, the urge falls by 10% per episode.",
  "Whether the cause changes is a random draw in each episode from a fixed seed, so the same settings always produce the same run.",
]
limits = [
  "The Rescorla–Wagner rule was developed for Pavlovian conditioning; using its form for a habit of seeking relief is an analogy, not an application of the fitted model.",
  "In life, relief varies from one occasion to the next, and causes rarely change by chance: they change through action, support and circumstance, none of which the model represents.",
  "Distress and urge are invented quantities, not scores on any questionnaire.",
]
references = ["rescorla-wagner-1972", "hayes-1996"]
labels = { relief = "Relief per episode", change = "Chance the cause changes per episode", episodes = "Episode", distress_before = "Distress before", distress_after = "Distress after", urge = "Urge to repeat", resolved = "Cause changed in episode", never = "Cause did not change within 30 episodes", reset = "Reset", chart = "Line chart over 30 episodes showing distress before and after each episode on a scale from 0 to 100 and the learned urge to repeat, with a marker at the episode in which the cause changed, if it changed." }

[[extra.models]]
id = "venting-arousal"
title = "Venting and arousal over time"
question = "After a provocation, how might anger change over half an hour when a person waits quietly, lowers arousal or raises it by hitting a bag?"
explanation = "Catharsis theory predicted that expressing anger vigorously would drain it. In an experiment, hitting a punching bag while thinking about the person who had caused the anger left participants angrier and more aggressive than doing nothing (Bushman, 2002). A meta-analysis of 154 studies found that activities that lower arousal reduced anger and aggression (g = −0.63), while activities that raise arousal had no overall effect (g = −0.02) (Kjærvik & Bushman, 2024). The model draws curves in the direction of those findings: anger fades with time, fades faster when arousal is lowered, and fades no faster than waiting when arousal is raised, while arousal itself stays high for longer. Compare the anger value after ten minutes for the three activities."
reading = "The horizontal axis shows minutes after the provocation. Anger and arousal are drawn on an illustrative scale without units, so the shapes of the curves carry the comparison, not the numbers. The value after ten minutes gives one point at which to compare the activities."
assumptions = [
  "All three activities start from the same level of anger immediately after the provocation.",
  "Anger declines exponentially, with a time constant of 10 minutes for waiting, 5 minutes for slow breathing and 11 minutes for hitting a bag.",
  "When arousal is raised, it first climbs and then declines slowly; anger and arousal are computed separately, without feedback between them.",
  "The shapes reflect only the direction of published effects; effect sizes have not been converted into minutes.",
]
limits = [
  "No study cited here measured these curves minute by minute; the time constants are invented to make the direction of the findings visible.",
  "Pooled effects hide heterogeneity: the studies of arousal-raising activities varied, and an average does not describe how any one person's anger changes.",
  "The model concerns anger after a provocation. It says nothing about grief or fear, or about exercise in general, which has other documented benefits.",
]
references = ["kjaervik-bushman-2024", "bushman-2002"]
labels = { activity = "Activity", waiting = "Waiting quietly", calming = "Lowering arousal (slow breathing)", venting = "Raising arousal (hitting a bag)", minutes = "Minutes after provocation", anger = "Anger (illustrative)", arousal = "Arousal (illustrative)", at_ten = "Anger after 10 minutes", chart = "Line chart over 30 minutes after a provocation showing illustrative anger for the selected activity and, when arousal is raised, an illustrative arousal curve, with the anger value at 10 minutes marked." }

[[extra.models]]
id = "peak-end"
title = "Peak and end in remembered discomfort"
question = "Why might a longer unpleasant episode be remembered as less unpleasant than a shorter one that contained less discomfort in total?"
explanation = "Retrospective evaluations of unpleasant episodes tend to be dominated by the worst moment and the final moment, while duration plays only a small role (Fredrickson & Kahneman, 1993). In a cold-water experiment, a significant majority of participants chose to repeat a longer trial that ended with 30 seconds of slightly less cold, still painful water rather than a shorter trial without that ending (Kahneman et al., 1993). The model places the average and the total of all moments next to a peak–end estimate, the mean of the highest moment and the last one. Set a high final moment, then add a milder one and watch the total rise while the peak–end estimate falls."
reading = "Bars show the discomfort of each moment in order. The average and the total describe the whole episode, while the peak–end estimate uses only two of its moments. Adding a final moment of 3 lowers the estimate when the current last moment is higher than 3 and raises it when that moment is lower."
assumptions = [
  "Remembered discomfort is approximated by the simple mean of the peak and the final moment.",
  "Every moment lasts equally long, and discomfort is rated from 0 to 10.",
  "The total, the sum of all moments, stands in for how much discomfort was actually experienced.",
]
limits = [
  "The peak–end pattern describes a tendency across participants in laboratory film clips and cold-water trials; it is not a formula for one person's memory, and applying it to nights out or life events is an extrapolation.",
  "Choosing to repeat an episode is not the same as having benefited from it; the model shows how memory can diverge from experience, not which experience is better.",
]
references = ["kahneman-1993", "fredrickson-kahneman-1993"]
labels = { moment = "Moment", discomfort = "Discomfort", average = "Average of all moments", peak_end = "Peak–end estimate", total = "Total discomfort", add = "Add a milder final moment", remove = "Remove the last moment", reset = "Reset", chart = "Bar chart of discomfort from 0 to 10 for each moment in order, with reference lines for the average of all moments and for the peak–end estimate, and the total discomfort shown alongside." }

[[extra.models]]
id = "synchrony"
title = "Synchrony in coupled oscillators"
question = "How strong must the mutual pull between rhythms with different natural tempos be before they fall into step?"
explanation = "The Kuramoto model describes a population of oscillators, each with its own natural frequency, in which every oscillator is pulled towards the phases of the others. When coupling is weak relative to the spread of natural frequencies, phases drift apart; above a threshold, part of the population locks into a common rhythm while the rest keeps drifting (Kuramoto, 1984; Strogatz, 2000). The order parameter r summarises the state of the whole group: near 0 when phases are scattered around the circle and 1 when all oscillators move together. Start with no coupling and raise K slowly, then widen the spread of tempos and see how much more coupling is needed."
reading = "Each dot is one oscillator travelling around the circle at its own tempo. The value r is the length of the average of all the dots' positions taken as arrows from the centre: short when the dots are spread out, long when they cluster. Watch r over time rather than at a single moment, because it fluctuates."
assumptions = [
  "Every oscillator is coupled equally to every other one, through a single strength K.",
  "Natural tempos are drawn at random from a range whose width is set by the spread.",
  "Each oscillator is described only by its phase; amplitude, fatigue and outside noise are left out.",
]
limits = [
  "With 4 to 40 oscillators, r fluctuates and rarely falls to 0 even without coupling; the sharp threshold of the mathematical theory holds for very large populations.",
  "It is a mathematical model of synchronization in general, not a model of dancers, crowds or bonding; the experiments that linked moving in synchrony with cooperation and closeness studied people, not oscillators.",
]
references = ["kuramoto-1984", "strogatz-2000", "wiltermuth-heath-2009", "tarr-2015"]
labels = { coupling = "Coupling strength K", count = "Number of oscillators", spread = "Spread of natural tempos", order = "Synchrony r", play = "Play", pause = "Pause", step = "Step", reset = "Reset", chart = "Animated circle with one dot per oscillator moving at its own tempo, and a readout of the synchrony value r between 0 and 1." }

[[extra.models]]
id = "allostatic-load"
title = "Allostatic load and recovery"
question = "When does repeated stress accumulate instead of passing, and how does the pace of recovery change that?"
explanation = "Stress responses help the body meet challenges, but McEwen (1998) described how repeated activation, or responses that are not switched off efficiently, can carry a cumulative cost he called allostatic load. The model turns that idea into simple bookkeeping: each stressor adds 10 units, and every day a fixed percentage of the current load is recovered. When stressors add load faster than recovery removes it, load rises until it levels off on a higher plateau, or keeps climbing for weeks when recovery is slow. Keep the number of stressors fixed and change only recovery, then do the reverse."
reading = "The horizontal axis shows weeks, and the line shows load in arbitrary units. The highest load over the 12 weeks is shown separately. A line that flattens out means that daily recovery has caught up with daily input; it does not mean that the load has gone."
assumptions = [
  "All stressors are equal, and each adds the same 10 units.",
  "Recovery removes the same percentage of the current load every day, whatever produced it.",
  "Stressors keep arriving at the same weekly rate for all 12 weeks, with no breaks and no crises.",
]
limits = [
  "Allostatic load is a conceptual framework whose measurement is still debated; the units here correspond to no biomarker, score or health risk.",
  "Real stressors differ in size, meaning and controllability, and recovery depends on sleep, support, health and resources that the model does not represent.",
]
references = ["mcewen-1998"]
labels = { frequency = "Stressors per week", recovery = "Recovery per day", weeks = "Week", load = "Accumulated load (arbitrary units)", peak = "Highest load", chart = "Line chart of accumulated load in arbitrary units over 12 weeks for the chosen number of stressors per week and daily recovery rate, with the highest load marked." }
+++

## Why models, and why they are not predictions

Many of the arguments in this library are about time. Relief is felt now, and the difficulty that produced it may return tomorrow. Anger fades at different speeds depending on what a person does. An evening is remembered for its best or worst moments rather than for its length. A crowd falls into step gradually, and stress that is not recovered from builds up over weeks. Prose describes these processes one sentence at a time; a model lets you watch them unfold and change the conditions.

A model, in the sense used here, is a small set of explicit rules applied repeatedly to numbers. Its value is transparency. Every assumption is written down, so you can see why a curve rises or flattens and which choice produced the effect. If you disagree with an assumption, the disagreement is precise: you can name the rule you think is wrong.

That transparency comes at a price. The models on this page are deliberately simple, and their numbers are invented. They are not fitted to data, they have not been validated against anyone's experience, and they make no forecast about what will happen to you or to anyone else. When a curve on this page resembles something you have lived through, the resemblance shows that the rules can produce such a pattern. It does not show that those rules are why it happened to you.

## How to use these models responsibly

Treat each model as a thought experiment with a calculator attached. Three habits help.

Change one thing at a time. Each model has two or three inputs, and the clearest lessons come from holding the others still. Look for thresholds, where a small change in one input changes the pattern, and for ranges where nothing much happens.

Read the assumptions before the chart. The list under each model says what is fixed, what is simplified and what is left out. A striking result often depends on one of those assumptions, and the page states the limits so that you do not have to guess.

Keep the direction of evidence separate from the numbers. Where a model draws on research, the cited studies support a direction of effect, such as calmer activities reducing anger more than vigorous ones. The size of each effect on screen, its timing and the exact shape of each curve are choices made for illustration. The claims this page makes are recorded in the [evidence ledger](@/evidence/index.md) with their sources and their strength.

## Background: the relief loop

[Negative reinforcement](../glossary/#negative-reinforcement) is the process by which a behaviour becomes more likely because it removes something unpleasant. It does not require the behaviour to address the source of the unpleasant state; it requires only that relief follows. Experiential avoidance, the attempt to escape unwanted inner experience, has been proposed as a process common to many psychological difficulties (Hayes et al., 1996).

The model represents learning with the error-correcting update of the Rescorla–Wagner model (Rescorla & Wagner, 1972), in which each learning episode closes part of the gap between what has been learned and the most that can be learned. Here the gap is closed by 15% per episode, scaled by the amount of relief, so strong relief builds the urge quickly at first and more slowly as it approaches its limit. Because distress returns to the same level before every episode, the chart can show a growing habit alongside an unchanged problem. That is the pattern [Research note 04](@/research/relief-is-not-resolution/index.md) describes as the difference between [relief and resolution](../glossary/#relief-vs-resolution). When the cause changes, the baseline falls and the urge, no longer reinforced, fades.

## Background: venting and arousal over time

The [hydraulic](../glossary/#hydraulic-model) image of anger, as pressure that must be let out, predicts that hitting something should leave a person calmer. The experimental evidence points the other way. [Venting](../glossary/#venting) while ruminating on a provocation increased anger and aggression compared with doing nothing (Bushman, 2002), and in a meta-analysis of anger management activities, those that lowered [arousal](../glossary/#arousal) reduced anger and aggression while those that raised arousal were ineffective overall (Kjærvik & Bushman, 2024).

The model shows these findings as three trajectories over half an hour. It is not a measured account of how anger decays, and the time constants are invented. What it keeps is the ordering: lowering arousal ends above waiting, and raising arousal ends no better than waiting. The separate arousal curve is a reminder that a vigorous activity can feel like discharge while leaving the body activated. [Research note 02](@/research/venting-hypothesis/index.md) sets out the studies and their limits.

## Background: peak and end in remembered discomfort

Retrospective evaluations do not add up an experience moment by moment. Participants who rated film clips gave overall evaluations that were barely affected by how long the clips lasted (Fredrickson & Kahneman, 1993), a finding known as duration neglect. In the cold-water experiment, extending an unpleasant trial with a slightly milder ending made it the one most participants chose to repeat (Kahneman et al., 1993). The [peak–end rule](../glossary/#peak-end-rule) summarises the pattern: remembered discomfort tracks the worst and the final moments.

The model makes the arithmetic visible. You can build an episode whose total discomfort increases while its remembered version improves. The relevance to catharsis is direct: an intense night that ends on a high may be remembered as more restorative than its course would justify, and that memory can shape the choice to seek it again.

## Background: synchrony in coupled oscillators

Synchronization appears in systems as different as flashing fireflies, cardiac pacemaker cells and oscillating chemical reactions. Kuramoto's model captures what these systems share: many rhythms with different natural tempos, each nudged by the others. Strogatz (2000) reviewed a quarter of a century of work on the model, which shows a transition: below a critical coupling strength the population stays incoherent, and above it some oscillators spontaneously synchronize while others continue to drift.

The model is included as an analogy for [interpersonal synchrony](../glossary/#interpersonal-synchrony), the experience of moving in time with others. The analogy is useful for one point in particular: synchrony is a property of the group that emerges from interaction, without any conductor imposing it. Its limits are just as important. The oscillators have no feelings and no bonds. The human findings, that people who acted in synchrony cooperated more afterwards (Wiltermuth & Heath, 2009) and that synchronised dance raised pain thresholds and in-group bonding (Tarr et al., 2015), come from experiments with people and do not depend on this mathematics. [Research note 03](@/research/collective-synchrony/index.md) discusses them.

## Background: allostatic load and recovery

McEwen (1998) described stress mediators as protective in the short term and damaging when they are activated too often or not switched off efficiently. [Allostatic load](../glossary/#allostatic-load) names that cumulative cost. The model reduces the idea to input and recovery. With frequent stressors and slow recovery, load keeps rising for weeks; with the same stressors and faster recovery, it settles at a lower plateau. The lesson is qualitative: how quickly a person recovers can matter as much as how often stress arrives, and a single restorative event lowers the load only briefly if the rate of arrival does not change. [Research note 09](@/research/stress-and-social-buffering/index.md) describes the research on stress and social support.

## What models cannot capture

Every model on this page leaves out the things that matter most in a life.

Individual differences are absent. The models apply the same rules to everyone, whereas people differ in temperament, history, health, sensitivity to stress and ways of coping. A group-level finding describes an average across participants and does not say how any one person will respond.

Context is absent. A relief behaviour at a party, in a crisis or after a loss is the same number in the model and a different event in life. Who is present, what is at stake and what options a person has are not variables in any of these simulations.

Meaning is absent. The models count units of distress, anger, discomfort, phase and load. They cannot represent what an experience means to the person living it, how people make sense of what happened to them, or why an episode that looks the same on a chart can be a turning point for one person and a repetition for another.

Change through action is absent. In the relief loop, the cause changes by a random draw. In life, causes change because people talk, decide, ask for help, leave, repair or are supported by others. None of that is modelled, and it is precisely the part a simulation cannot do for anyone.

For these reasons the models are not tools for assessing yourself or anyone else. If distress, anger or stress is persistent or severe, a conversation with someone you trust and, where needed, with a qualified professional is more informative than any curve.

## Where to read further

The [methods page](@/methods/index.md) explains why signals and models support inferences with stated uncertainty rather than conclusions about a person, and the [evidence overview](@/evidence/index.md) shows how every claim on this page is graded and reviewed.

The research notes give the empirical background for each model: [relief is not resolution](@/research/relief-is-not-resolution/index.md), [the venting hypothesis](@/research/venting-hypothesis/index.md), [collective synchrony](@/research/collective-synchrony/index.md) and [stress and social buffering](@/research/stress-and-social-buffering/index.md).

The theory pages develop the ideas behind them in more depth: [learning, avoidance and relief](@/theory/learning-avoidance-and-relief/index.md), [allostasis and stress](@/theory/allostasis-and-stress/index.md), and [collective emotion and ritual](@/theory/collective-emotion-and-ritual/index.md).
