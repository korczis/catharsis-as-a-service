+++
title = "Methods: signals, inference and the limits of detecting a state change"
description = "How one could reason about recording a catharsis-like change of state: signals, features, inference and context, baselines, self-report, error costs and ethics, and why every step stays uncertain. Nothing on this site measures anyone."
date = 2026-09-14
template = "methods.html"

[taxonomies]
tags = ["methods", "measurement", "physiology", "uncertainty", "ethics"]

[extra]
kicker = "Methods"
summary = "A change in someone's state leaves traces in heart rate, skin conductance, movement, voice and self-report, but none of these traces identifies what the person feels or why. This page follows the chain from raw signal to interpretation, shows where error enters at each step, and explains why combining signals does not remove the core ambiguity. It separates what a sensor records from what a person or a model concludes, and sets out the vocabulary an honest system would need. The site collects no physiological data, and the interactive model runs on invented inputs."
key_points = [
  "Every conclusion about an emotional state passes through four steps, signal, feature, inference and context, and each step adds its own error.",
  "A meta-analysis of 202 laboratory studies found that autonomic responses did not clearly distinguish one emotion category from another (Siegel et al., 2018), and facial movements are not reliable, specific indicators either (Barrett et al., 2019).",
  "Self-report is indispensable but depends on when it is collected: retrospective evaluations are dominated by the worst and final moments (Kahneman et al., 1993), a bias momentary sampling aims to reduce (Shiffman et al., 2008).",
  "Signals can at most be consistent with a change of state. Whether the conditions that produced distress have changed is not measured by them, which is why the artwork's endpoint answers problem_solved: false.",
]
references = ["siegel-2018", "kreibig-2010", "barrett-2019", "poldrack-2006", "laborde-2017", "boucsein-2012", "robinson-clore-2002", "fredrickson-kahneman-1993", "kahneman-1993", "shiffman-2008", "kuppens-verduyn-2017", "wiltermuth-heath-2009", "tarr-2015", "kjaervik-bushman-2024", "picard-1997", "stark-hoey-2021"]

[[extra.detection_chain]]
id = "signal"
name = "Signal"
text = "A signal is what an instrument records: a physical quantity sampled over time, with no psychological meaning attached. Its shape depends on the device, its placement, its sampling rate and the environment as much as on the person."
example = "Raw skin conductance in microsiemens sampled 32 times per second by a wrist-worn sensor, or the three-axis trace of an accelerometer."
risk = "Artefacts enter here: a loose electrode, sweat caused by heat, movement or dropped samples can produce a trace that looks like a physiological response but is not one."

[[extra.detection_chain]]
id = "feature"
name = "Feature"
text = "A feature is a number computed from the signal to summarise it, such as a mean, a rate of events or a variability index. Choosing the feature, the time window, the filter and the artefact correction is already a modelling decision."
example = "The number of skin conductance responses per minute above a chosen amplitude threshold, or RMSSD, a heart rate variability index, computed over five minutes of heartbeat intervals."
risk = "Thresholds, window lengths and correction rules change the value; two reasonable processing pipelines can produce different features from the same recording."

[[extra.detection_chain]]
id = "inference"
name = "Inference"
text = "Inference maps features onto a description of a person, such as elevated arousal or a probable phase of an episode. It is the step at which measurement becomes interpretation, whether a statistical model or a human observer performs it."
example = "A model concludes that a simultaneous rise in heart rate and in skin conductance responses is consistent with increased physiological arousal."
risk = "Reverse inference: treating a pattern that often accompanies a state as evidence of that state, although the same pattern also accompanies many other states and activities."

[[extra.detection_chain]]
id = "context"
name = "Context"
text = "Context is what else is known about the situation: what the person is doing, where, with whom, what happened before, and what they say about it. Without it, most inferences from bodily signals remain underdetermined."
example = "The same rise in heart rate recorded while climbing stairs, during an argument, or at a concert as the music builds."
risk = "Context can be missing, wrong or itself inferred; a model that guesses the context from the same signals moves the uncertainty elsewhere instead of reducing it."

[[extra.temporal_model]]
id = "baseline"
name = "Baseline"
text = "The person's usual range of values for a given time of day, posture and situation, against which any change is judged."
observable = "Resting heart rate and heart rate variability over repeated recordings, typical skin conductance level, habitual movement, a baseline self-report."
caution = "A baseline is itself variable. Sleep, caffeine, illness, medication, temperature and the anticipation of being measured shift it, so one short recording may not be representative."

[[extra.temporal_model]]
id = "activation"
name = "Activation"
text = "A departure from baseline towards higher physiological activity and alertness."
observable = "Rising heart rate, more frequent skin conductance responses, faster breathing, more movement, reports of tension or excitement."
caution = "Activation is not specific: exercise, fear, excitement, anger, heat and stimulants produce overlapping patterns."

[[extra.temporal_model]]
id = "synchronization"
name = "Synchronization"
text = "In shared settings, individual movement and attention align with a common rhythm and with other people."
observable = "Correlated movement between people, steps or clapping entrained to a beat, shared orientation, reports of feeling part of the group."
caution = "Shared movement can reflect the music, choreography, crowd density or conformity. In experiments it is associated with cooperation and bonding, but it does not show what each person feels."

[[extra.temporal_model]]
id = "peak"
name = "Peak"
text = "The point of highest intensity within an episode."
observable = "Maximum heart rate or movement intensity, a cluster of skin conductance responses, vocal outbursts, a momentary rating of maximum intensity."
caution = "The physiological, behavioural and experienced peaks need not coincide in time, and a peak can only be identified after values have fallen; the remembered peak is shaped later by recall."

[[extra.temporal_model]]
id = "discharge"
name = "Discharge"
text = "A rapid fall in intensity after the peak, often experienced as release."
observable = "Falling heart rate, slower breathing, less movement, laughter or crying, reports of relief."
caution = "A falling signal is consistent with release, but also with exhaustion, the end of the music or simply sitting down. It describes bodily activity, not what was released or whether anything was resolved."

[[extra.temporal_model]]
id = "recovery"
name = "Recovery"
text = "A return towards baseline over minutes to hours."
observable = "Heart rate and heart rate variability approaching resting values, declining skin conductance level, reports of calm or tiredness."
caution = "The speed of recovery depends on fitness, fatigue, alcohol, sleep and temperature as well as on emotional processes; a fast return to baseline is not a marker of psychological resolution."

[[extra.temporal_model]]
id = "post-state"
name = "Post-state"
text = "The state after the episode is over, including whether the original difficulty is still present."
observable = "Later self-report, behaviour over the following days, recurrence of the same distress, changes in the situation the person returns to."
caution = "This is the phase that matters most for resolution and the one least accessible to sensors. Whether the conditions behind the distress have changed is not measured by any signal on this page."

[extra.detection_matrix]
caption = "What ten kinds of evidence record, what their patterns are consistent with, and what none of them can establish on its own."
columns = { signal = "Signal", records = "What is recorded", consistent_with = "Consistent with", cannot_establish = "Cannot establish", confounds = "Common confounds" }

[[extra.detection_matrix.rows]]
signal = "Heart rate"
records = "Beats per minute from an electrocardiogram or an optical wrist sensor."
consistent_with = "Changes in physiological activation, physical effort or posture."
cannot_establish = "Which emotion, if any, is present, or whether the change is pleasant or unpleasant."
confounds = "Exercise, standing up, caffeine, nicotine, alcohol, heat, fever, medication, dehydration, optical sensor error during movement."

[[extra.detection_matrix.rows]]
signal = "Heart rate variability"
records = "Variation in the intervals between successive heartbeats, summarised by time-domain or frequency-domain indices."
consistent_with = "Changes in cardiac vagal (parasympathetic) influence on the heart."
cannot_establish = "A specific emotional state, or a person's capacity for regulation, from one short recording."
confounds = "Breathing rate and depth, posture, physical activity, age, fitness, recording length, irregular beats, artefact correction choices."

[[extra.detection_matrix.rows]]
signal = "Electrodermal activity"
records = "Changes in the electrical conductance of the skin driven by sweat gland activity, as a slow level and fast responses."
consistent_with = "Sympathetic activation, orienting towards something new or significant."
cannot_establish = "Whether the activation is positive or negative, or what it is directed at."
confounds = "Ambient temperature and humidity, exertion, electrode placement and contact, large individual differences, habituation to repeated stimuli."

[[extra.detection_matrix.rows]]
signal = "Respiration"
records = "Breathing rate, depth and regularity from a chest band or nasal sensor, or estimated from other signals."
consistent_with = "Changes in arousal or effort, speaking, laughing or crying."
cannot_establish = "The meaning of the change, since singing, speaking and exertion alter breathing directly."
confounds = "Talking, singing, physical activity, posture, deliberate breath control, respiratory illness."

[[extra.detection_matrix.rows]]
signal = "Movement and accelerometry"
records = "Acceleration of the body part carrying the sensor, from which activity intensity and the timing of steps or beats are computed."
consistent_with = "Level of physical activity, dancing, restlessness."
cannot_establish = "Why someone moves; agitation and enjoyment can produce similar traces."
confounds = "Sensor placement, travel in vehicles, being jostled in a crowd, walking between places."

[[extra.detection_matrix.rows]]
signal = "Interpersonal movement synchrony"
records = "How strongly the movement time series of two or more people are correlated or aligned in phase."
consistent_with = "A shared rhythm and coordinated activity, conditions associated with affiliation and cooperation in experiments."
cannot_establish = "That people feel the same thing, feel close to each other, or feel anything in particular."
confounds = "A common external beat, choreography, crowd constraints, imitation, the window and lag settings of the analysis."

[[extra.detection_matrix.rows]]
signal = "Voice prosody"
records = "Pitch, loudness, speaking rate and voice quality in recorded speech."
consistent_with = "Changes in vocal effort and arousal, or in speaking style."
cannot_establish = "A specific emotion; prosody also carries language, dialect, irony, politeness and health."
confounds = "Background noise, microphone distance, language and accent, a cold, fatigue, shouting over music."

[[extra.detection_matrix.rows]]
signal = "Facial movement"
records = "Positions and movements of facial muscles from video, coded by people or by software."
consistent_with = "Communicative displays, attention, effort, and some instances of emotion."
cannot_establish = "A specific internal state; similar configurations accompany different emotions and often communicate something other than emotion (Barrett et al., 2019)."
confounds = "Lighting, head angle, glasses, masks, culture, social display norms, talking, chewing, squinting in bright light."

[[extra.detection_matrix.rows]]
signal = "Self-report (momentary)"
records = "A person's answer, given at the time, to questions about how they feel."
consistent_with = "The person's current account of their experience, in the categories the question offers."
cannot_establish = "Physiological state or facts about the situation; a report is an account, not an independent check of the cause."
confounds = "Question wording, response scales, social desirability, the effect of being asked, reluctance to disclose, available words for feelings."

[[extra.detection_matrix.rows]]
signal = "Context records (time, place, activity)"
records = "Time, location, activity, company and events logged by a person or a system."
consistent_with = "Plausible explanations for a change in signals, such as exercise or a scheduled performance."
cannot_establish = "How the person experienced the situation, or whether the situation is a problem for them."
confounds = "Missing or inaccurate logs, activity inferred rather than reported, privacy limits that rightly restrict what is recorded."

[[extra.uncertainty]]
term = "consistent with"
meaning = "Use when an observation fits an interpretation but would also fit others. It does not imply that the interpretation is the most likely one."

[[extra.uncertainty]]
term = "associated with"
meaning = "Use for a statistical relationship found across people or occasions. It implies neither cause nor that the relationship holds for a particular individual."

[[extra.uncertainty]]
term = "suggests"
meaning = "Use when several independent observations point the same way and alternatives have been considered. It is weaker than a conclusion and should name what would change it."

[[extra.uncertainty]]
term = "inferred with low confidence"
meaning = "Use for a model output that rests on assumptions not checked in the situation, such as an unknown baseline or missing context. It signals that the output should not drive a decision about the person."

[[extra.uncertainty]]
term = "insufficient evidence"
meaning = "Use when the available data cannot distinguish between interpretations. It is not evidence that a state is absent."

[[extra.uncertainty]]
term = "not measured"
meaning = "Use when no signal in the system addresses the question at all. It prevents silence from being read as a negative result."

[[extra.uncertainty]]
term = "unknown"
meaning = "Use when a value is required, for example in an API response, but there is no valid basis for filling it. It is preferable to a default value that looks like data."

[[extra.uncertainty]]
term = "contradicted by"
meaning = "Use when one source conflicts with an interpretation, for example a person reporting calm while a model infers distress. It should prompt a review of the model before any conclusion about the person."

[extra.errors]
false_positive = { name = "False positive", text = "The system reports a state that is not present, for example labelling someone as distressed, or as recovered, when they are not.", example = "Heart rate and skin conductance rise while someone runs to catch a train, and a model labels the episode as acute distress.", cost = "Unwanted attention or intervention, stigma and loss of trust; in institutions, consequences for a person on the basis of a state they never had." }
false_negative = { name = "False negative", text = "The system fails to report a state that is present.", example = "A person in serious distress sits still and breathes slowly, their signals stay close to baseline, and the model reports no change.", cost = "A missed need for support and false reassurance, especially when the output is used to decide that nobody needs to ask." }

[[extra.architecture]]
component = "Static publication"
role = "Generates the bilingual site from Markdown and templates."
status = "implemented"
note = "Pages are plain files; nothing is computed about the reader."

[[extra.architecture]]
component = "Reference registry with Crossref checks"
role = "Resolves every citation to one entry with bibliographic metadata."
status = "implemented"
note = "The check confirms metadata, not that a claim fairly represents its source; that remains an editorial task."

[[extra.architecture]]
component = "Evidence ledger with review dates"
role = "Records which claims rest on which sources and when they were last reviewed."
status = "implemented"
note = "A review date shows when a claim was checked, not that it will remain correct."

[[extra.architecture]]
component = "Versioned content API"
role = "Publishes the site's content as versioned, machine-readable files."
status = "implemented"
note = "It serves content only and accepts no personal or physiological data."

[[extra.architecture]]
component = "Rust client library and CLI"
role = "Read the published content and API from code or the terminal."
status = "implemented"
note = "They consume what the site publishes and have no measurement function."

[[extra.architecture]]
component = "Browser simulation of the detection model"
role = "Shows how an honest detection model would phrase its output for invented inputs."
status = "simulation"
note = "Runs entirely in the page on slider values set by the visitor; nothing is sent, stored or taken from a real person."

[[extra.architecture]]
component = "Context engine combining signals with self-report and situation"
role = "Would weigh signals against the person's own account, the situation and their history."
status = "conceptual"
note = "Described on this page to show what honest inference would require; not built, and no data flow exists to feed it."

[[extra.architecture]]
component = "Physiological signal ingestion"
role = "Would receive data from wearables or other sensors."
status = "not-planned"
note = "Deliberately excluded: the artwork is about instrumentation and does not instrument its audience."

[[extra.architecture]]
component = "Individual emotion inference or profiling"
role = "Would assign emotional states or traits to identifiable people."
status = "not-planned"
note = "Excluded on grounds of validity and consent."

[[extra.architecture]]
component = "Analytics or tracking of visitors"
role = "Would record the visits, behaviour or identity of readers."
status = "not-planned"
note = "The site uses no analytics, trackers or cookies."

[extra.simulation]
banner = "Simulation · not biometric analysis"
heading = "Try the detection model with invented inputs"
intro = "The sliders hold invented values, not readings from any device, and nothing you set is recorded or sent anywhere. The model applies the reasoning on this page to those values and shows how an honest system would phrase its conclusion, including what it cannot know."
inputs_label = "Invented inputs"
output_label = "Model output"
reset = "Reset"
inputs = [
  { id = "heart_rate", label = "Heart rate change from personal baseline", unit = "bpm", min = -10, max = 60, step = 1, value = 22 },
  { id = "eda", label = "Skin conductance responses per minute", unit = "/min", min = 0, max = 20, step = 1, value = 8 },
  { id = "synchrony", label = "Movement synchrony with nearby people", unit = "%", min = 0, max = 100, step = 5, value = 70 },
  { id = "relief", label = "Self-reported relief", unit = "/10", min = 0, max = 10, step = 1, value = 7 },
]
cause_label = "The person reports that the cause of their distress has changed"
out_activation = "Physiological activation"
levels = { low = "low", moderate = "moderate", high = "high" }
activation_note = "Activation is not specific: exercise, excitement, fear, anger and heat all raise these signals."
out_phase = "Phase most consistent with the inputs"
phases = { baseline = "Baseline", activation = "Activation", peak = "Peak", discharge = "Discharge", recovery = "Recovery" }
out_synchrony = "Shared movement"
synchrony_values = { low = "little shared movement", high = "strong shared movement" }
out_relief = "Relief"
relief_values = { reported = "reported", not_reported = "not reported" }
out_cause = "Cause resolved"
cause_values = { unknown = "unknown: not measurable from these signals", reported = "reported by the person, not verified" }
out_confidence = "Confidence"
confidence_value = "LOW"
confidence_note = "Without a verified personal baseline, context and repeated observations, an inference about one person from four signals cannot exceed low confidence."
problem_line = "problem_solved"
problem_values = { unknown = "unknown", false = "false" }

[extra.poster_figure]
id = "poster-methods"
caption = "From the Catharsis as a Service poster series. Slogans and numbers on the posters belong to the artwork; they are not findings."
items = [
  { src = "assets/posters/emoce-jsou-data.png", title = "Emotions are data", alt = "Poster: EMOCE JSOU DATA. (emotions are data) over a close-up of a face with closed eyes streaked with red light, above a crowd at a glowing stage gate; side panels repeat the artwork's input, process and output and show an artistic telemetry box.", caption = "An artistic slogan, not a method: this page explains why signals do not show what someone feels." },
]

+++

## Why this page exists

The artwork on this site presents collective catharsis as a service, complete with telemetry: input state, synchronization, discharge, relief. Its endpoint answers `200 OK` with `problem_solved: false`. The telemetry is conceptual. No number on the poster or in the dashboard was recorded from a person, and [Research note 05](@/research/measuring-emotion/index.md) explains why the artwork refuses to measure its audience.

That refusal raises a fair question. If someone did want to know whether a catharsis-like change of state had taken place, in a concert crowd, in a therapy session or in a laboratory, what could real measurement support? This page answers as carefully as the evidence allows. It describes how signals from the body and from self-report could be turned into a statement about a change of state, where each step introduces error, and what no combination of signals can settle.

Two commitments shape everything below. First, measurement and interpretation are kept apart: a sensor records skin conductance, and a person or a model concludes something about arousal. Second, nothing on this site measures anyone. The site collects no physiological data, runs no analytics and sets no trackers. The interactive part of this page is a simulation that works only with values you invent.

## The detection model: signal, feature, inference, context

Any claim of the form "this person went through a release" rests on a chain of four steps, shown in the chain below.

A [signal](../glossary/#signal) is what an instrument records: voltage from electrodes, light reflected through the skin of the wrist, acceleration, sound pressure. A signal has units and a sampling rate, but no psychological meaning.

A [feature](../glossary/#feature) is a quantity computed from the signal: mean heart rate over a minute, the number of skin conductance responses above a threshold, the correlation between two people's movements. Every feature embodies choices about the time window, the filter, the threshold and the way artefacts are removed. Those choices are rarely visible in the final number, yet they change it.

An [inference](../glossary/#inference) maps features onto a description of a person: elevated [arousal](../glossary/#arousal), a probable phase of an episode, a likely emotional category. This is where measurement becomes interpretation. Whether a trained classifier or a researcher looking at a plot performs it makes no difference to its logical status.

[Context](../glossary/#context) is everything known about the situation that is not in the signal: what the person was doing, where, with whom, what preceded the recording, and what the person says about it. Context often decides between interpretations that the features alone cannot separate.

Error enters at every step, and it compounds. A movement artefact in the signal becomes a spurious spike in a feature; the spike becomes an inferred "response"; and a missing context record allows that response to be interpreted as fear rather than as someone bumping into the sensor. Later steps cannot recover information that earlier steps lost. They can, however, make a weak signal look authoritative by giving it a confident label.

## Baseline: nothing means anything without one

A heart rate of 95 beats per minute is unremarkable for one person who is walking and notable for another who is sitting still. Physiological features acquire meaning only relative to a [baseline](../glossary/#baseline): the range of values typical for that person under comparable conditions.

Useful baselines are within-person. They are estimated from repeated recordings of the same individual, ideally at similar times of day, in similar postures and at similar levels of activity. Many ordinary factors move physiological signals without any emotional change: the circadian rhythm, standing rather than sitting, a recent meal, caffeine and nicotine, alcohol, medication, lost sleep, illness, ambient temperature and humidity, and the simple anticipation of being measured. Skin conductance, for example, responds to temperature and exertion as well as to psychological events, and methodological handbooks on [electrodermal activity](../glossary/#electrodermal-activity) treat recording conditions, electrode placement and individual differences as central to its interpretation (Boucsein, 2012).

[Heart rate variability](../glossary/#heart-rate-variability) is widely used in psychophysiology because it indexes cardiac vagal tone, the parasympathetic contribution to the regulation of the heart, and because it is inexpensive, non-invasive and easy to record. Laborde, Mosley and Thayer (2017) nonetheless warn that this ease of access should not obscure how easily HRV findings are misconstrued, and they set out recommendations for planning experiments, analysing data and reporting results so that conclusions are sound and comparable across laboratories.

Habituation adds another complication. Responses to a repeated stimulus tend to weaken, so the tenth loud chorus of an evening may produce a smaller skin conductance response than the first even when the listener describes both moments as equally intense. A falling response over time is therefore consistent with a fading experience, but also with an unchanged experience and a habituating body.

Group norms mislead for a related reason. A population average describes what is typical across people, not what is typical for this person. Resting heart rate, skin conductance level and heart rate variability differ with age, fitness, body size, health and medication. Applying a population threshold to an individual turns ordinary differences between people into apparent states, and it systematically mislabels those furthest from the average.

## Multimodality: more signals, not more certainty

If one signal is ambiguous, it is tempting to combine several. [Multimodality](../glossary/#multimodality) does help in some respects. Sensors with independent sources of artefact can cross-check each other: an accelerometer can show that a rise in heart rate coincided with running, and a microphone can show that faster breathing coincided with singing. Combining modalities reduces some errors, especially technical ones.

It does not remove the central ambiguity, for two reasons.

The first is that confounds are often shared across signals. Dancing in a warm room raises heart rate, lowers heart rate variability, increases skin conductance, speeds up breathing and produces movement, all at once. Five signals that agree are then five views of one cause, not five independent pieces of evidence about an emotion.

The second is that the physiological patterns themselves may not be specific to emotion categories. Siegel and colleagues (2018) meta-analysed 202 studies that measured autonomic nervous system reactivity during laboratory inductions of emotion in non-clinical adult samples. Autonomic variables did change, but the pattern of effect sizes did not clearly distinguish one emotion category from another. Variation within categories was considerable, and correcting for publication bias reduced the estimated effects further. The authors concluded that the findings were more consistent with emotion categories as variable populations of instances than with fixed autonomic "fingerprints".

The question is genuinely debated. An earlier review by Kreibig (2010), covering 134 experimental publications, concluded that autonomic responding showed considerable specificity when subtypes of distinct emotions were considered, and stressed that precise terminology for the states studied and a careful choice of physiological measures matter for such conclusions. The two reviews differ in method and in the questions they ask. For the purpose of this page, what they have in common matters more: both describe patterns estimated across many participants, under controlled inductions of defined states. Neither offers a pattern that could be applied to one person in an uncontrolled setting to establish what that person feels.

Facial movement, often added as "one more modality", has the same limitation. Barrett and colleagues (2019) found that people do smile, frown or scowl in the expected emotional situations more often than chance would predict, but that the way emotions are expressed varies substantially across cultures, situations and individuals, that similar facial configurations express more than one emotion category, and that a configuration such as a scowl often communicates something other than an emotional state.

Behind all of this lies the problem of [reverse inference](../glossary/#reverse-inference). Poldrack (2006) described it for neuroimaging: concluding that a mental process was engaged because a region associated with that process was active. Such inferences are not deductively valid, although they can add some evidence, and their value is limited by how selective the observed activity is. The same logic applies to bodily signals. Arousal rises during fear, but also during joy, effort and heat. The less selective a signal, the less its presence says about any single state, and adding more unselective signals does not make any of them selective.

## Self-report: indispensable and imperfect

[Self-report](../glossary/#self-report) is the only access to how an experience feels from the inside. Physiological data can show that something changed; only the person can say whether the change felt like release, dread, boredom or nothing in particular, and whether its [valence](../glossary/#valence) was pleasant or unpleasant. Any serious model of catharsis therefore needs self-report, and it needs to treat self-report as a measurement with errors of its own.

Robinson and Clore (2002) proposed an accessibility model of emotional self-report built on a distinction between emotion itself, which is episodic, experiential and tied to context, and beliefs about emotion, which are semantic, conceptual and detached from context. The distinction helps explain the discrepancies that often appear between reports of feelings a person is experiencing now and reports of feelings they are not currently experiencing, such as how they felt last week or how they usually feel at concerts. When the experience is no longer present, a report can draw more on what the person believes such situations feel like.

Retrospective reports are also shaped by the structure of the episode. Fredrickson and Kahneman (1993) asked participants to rate film clips continuously and then to evaluate each clip as a whole. The duration of a clip had only a small effect on the overall evaluations, which behaved like a weighted average of "snapshots" of the experience, as if duration did not matter. In a related experiment, Kahneman and colleagues (1993) exposed participants to a short trial of painfully cold water and a longer trial that added 30 seconds of slightly less cold, still unpleasant water. When asked which trial to repeat, a significant majority chose the longer one. Retrospective evaluations of such episodes are often dominated by the worst and the final moments. A night that ends on a high will tend to be remembered as more restorative than its minute-by-minute course would suggest.

Ecological momentary assessment (EMA) addresses part of this problem. It samples people's current experience and behaviour repeatedly, in real time and in their everyday environments, often at random moments, using tools that range from written diaries to electronic devices and physiological sensors. Its aim is to minimise recall bias and maximise ecological validity (Shiffman, Stone & Hufford, 2008). EMA does not remove every source of error. Being asked repeatedly can change what people notice, response options limit what can be reported, and people may answer in ways they consider acceptable, especially when they know someone else will see the data. That last concern, social desirability, is sharpest in exactly the settings where emotional monitoring is most often proposed: workplaces, schools and health services.

The practical consequence is that self-report and physiological data are not a truth and its proxy. They are two imperfect measurements of different aspects of an episode, and disagreement between them is information, not noise to be averaged away.

## The temporal model

Catharsis, as the artwork describes it, is a sequence rather than a state. The temporal model in the table below divides a catharsis-like episode into seven phases: baseline, activation, synchronization, peak, discharge, recovery and post-state. For each phase it lists what could in principle be recorded and why that observation does not establish the interpretation.

The model is a heuristic for organising observations, not an empirical finding. It borrows its framing from research on emotion dynamics, which studies the trajectories, patterns and regularities with which the experiential, physiological and behavioural elements of emotion fluctuate over time, the processes behind those fluctuations and their consequences for well-being (Kuppens & Verduyn, 2017). That framing is useful because it treats an emotional episode as a set of time series rather than as a single label. It does not imply that every episode passes through these seven phases, in this order, or at all.

Three cautions apply to the whole table. Phases are identified after the fact: a peak is a peak only once values have fallen. The physiological, behavioural and reported versions of a phase can unfold on different timescales and need not line up. And synchronization applies only to shared settings; a person crying alone may show activation, a peak and discharge with no synchronization at all.

Synchronization deserves a closer look because it is the phase most specific to collective catharsis. Across three experiments, people who had acted in synchrony with others cooperated more in subsequent group economic exercises, even when cooperation required personal sacrifice, and positive emotions did not need to be generated for this effect to appear (Wiltermuth & Heath, 2009). In group dance, synchrony and exertion each independently raised pain thresholds, used as a proxy for endorphin activity, and increased in-group bonding (Tarr et al., 2015). These results support treating shared movement as a meaningful social variable. The first of them also shows why it cannot serve as a readout of feeling: the social effect of synchrony did not depend on positive emotion. [Research note 03](@/research/collective-synchrony/index.md) discusses this work in more detail.

## Relief detected is not cause resolved

The artwork's endpoint answers `problem_solved: false`. This is not a joke at the expense of relief. It is the most precise statement the telemetry could make.

Suppose every step above worked well: a good baseline, clean signals, sensible features, rich context and a momentary report of relief. The strongest supportable conclusion would be that a pattern consistent with activation followed by a return towards baseline was observed, and that the person reported feeling relieved. That is a statement about a change of state. It says nothing about whether the conditions that produced the distress, such as a conflict, a loss, debt, loneliness or an unsafe home, have changed. Those conditions are not in the signal; they are not measured. [Relief and resolution](../glossary/#relief-vs-resolution) are different quantities, and [Research note 04](@/research/relief-is-not-resolution/index.md) describes the mechanisms, from negative reinforcement to memory, that make them easy to confuse.

The evidence on anger shows why a visible discharge should not be mistaken for a solution. Kjærvik and Bushman (2024) meta-analysed 154 studies, with 184 independent samples and 10,189 participants, that tested anger management activities. Activities that decrease arousal, such as deep breathing, mindfulness and meditation, reduced anger and aggression (Hedges' g = −0.63). Activities that increase arousal, such as hitting a bag, jogging or cycling, were ineffective overall (g = −0.02), and their results were heterogeneous. The authors concluded that the findings do not support venting anger or going for a run as effective ways of managing it. An arousal-increasing activity can produce a vivid peak and discharge in a physiological trace while, on this evidence, doing little on average to reduce anger. The advice entry [Let anger cool](@/advice/let-anger-cool/index.md) turns this into practice.

An honest model therefore has two outputs where a dashboard has one. The first, a change of state, can be inferred with a stated level of confidence. The second, whether the cause is resolved, is either reported by the person and unverified, or unknown.

## Measurement versus interpretation

Consider an invented but realistic heart-rate trace. From a resting value of about 65 beats per minute it climbs over several minutes to around 140, stays there for a while, then falls quickly and settles near 75 over the following quarter of an hour. Skin conductance responses become frequent during the climb and sparse afterwards.

Recorded at a concert, the trace is consistent with dancing, excitement and a crowd moving through a build-up and a release. Recorded during a panic attack, it is consistent with a surge of fear, rapid breathing and gradual calming as the attack subsides. Recorded during an interval run, it is consistent with effort followed by a cool-down, with no emotional episode at all.

The measurement is identical in all three cases. What differs is the interpretation, and what licenses the interpretation is not the trace but the context: the location, an accelerometer showing running or jumping, the person's own account, their history. Without context the only defensible output describes the measurement, "heart rate rose by roughly 75 beats per minute above baseline and returned close to it", together with the statement that the cause of the rise is not established.

The three cases share something else. In each of them, a system that labelled the fall in heart rate as "relief" would be using a word that belongs to experience to describe a quantity that belongs to the heart. At the concert, the label might happen to match what the person says. After the panic attack it would be misleading, because the fear may return. After the run it would be a category error.

## What each signal can and cannot tell us

The detection matrix below lists ten kinds of evidence that a system for detecting catharsis-like changes might draw on, from heart rate to context records. For each it separates what is recorded, what the recorded pattern is consistent with, what it cannot establish on its own, and the common confounds that produce the same pattern for unrelated reasons.

Two features of the matrix are deliberate. Every "consistent with" cell names something broader than a specific emotion, because the evidence reviewed above does not support tying these signals to specific emotions in individuals. And the last two rows, momentary self-report and context records, are not physiological at all. They are included because the physiological rows are largely uninterpretable without them, and because they have limits of their own: a report is an account, not a verification, and a log of time and place is not an account of experience.

## Speaking about uncertainty

A system that describes people should use words whose strength matches its evidence. The vocabulary below is used consistently across this site, and the simulation on this page uses it for its output.

The terms form a rough ladder. "Not measured" and "unknown" mark the absence of any basis for a claim. "Insufficient evidence" marks data that exist but cannot distinguish between interpretations. "Consistent with" and "associated with" mark compatibility and statistical relationship without implying cause or applicability to an individual. "Suggests" marks convergence after alternatives have been considered. "Inferred with low confidence" labels a model output for what it is. "Contradicted by" records a conflict between sources, which should prompt scrutiny of the model before any conclusion about the person.

What the vocabulary leaves out matters as much. It contains no term that would let a signal settle what someone feels, and no term for a model having access to someone's experience, because no method described on this page could support either claim.

## False positives and false negatives

Every classifier makes two kinds of mistake. A [false positive](../glossary/#false-positive) reports a state that is not present; a [false negative](../glossary/#false-negative) misses a state that is. Both are described with examples below.

It is tempting to summarise a system with a single accuracy figure. That hides two facts: the two errors rarely cost the same, and their costs depend on who uses the output and for what. Consider two labels a monitoring system could attach to a person after an intense evening.

A false "recovered" label, which is a false negative for continuing distress, can close a conversation that should have continued. A friend, a clinician or a support service that trusts the label may not ask the question that would have revealed that the person is not all right. The cost falls on someone who needed help and did not receive it.

A false "distressed" label, a false positive, can trigger unwanted attention, concern or intervention. In a workplace or a school it can attach a psychological description to someone who never disclosed anything, with consequences for how they are treated. The cost again falls on the person described, and it grows when the institution holds power over them.

Lowering a decision threshold to catch more real distress produces more false alarms; raising it to avoid false alarms misses more distress. No setting eliminates both. Choosing the threshold is therefore a decision about whose errors are acceptable. It should be made openly, by people accountable for the consequences and with the people affected involved, rather than tuned quietly for a benchmark.

Base rates matter as well. When the state being looked for is rare in the monitored population, even a system with good sensitivity and specificity will produce many false positives relative to true ones. This follows from arithmetic, not from any particular study, and it is one more reason to be cautious about screening whole crowds, classrooms or workforces.

## The context engine

The sections above keep returning to context. It is worth being specific about what a component combining signals with context would require, because the list itself shows why this page describes such a component as conceptual.

At a minimum it would need the situation: where the person is and what is happening around them. It would need the activity: whether they are sitting, dancing, running, speaking or singing. It would need recent history, such as sleep, substances, illness and what happened earlier that day, and a personal baseline built from the person's own repeated recordings. Above all it would need the person's own account, collected at the time, in their own words, with the freedom not to answer. And to say anything about resolution rather than relief, it would need information about the conditions the person returns to, which no sensor records and which people have every right to keep to themselves.

Each of these inputs is difficult to obtain reliably, intrusive to collect, or both, and several can come only from the person. Once they are available, most of the interpretive work is being done by the person's account and the situation rather than by the sensors, and the physiological signals become supporting evidence instead of the source of the conclusion. That is the appropriate relationship, and it is why a context engine is not a shortcut to knowing what people feel.

On this site the context engine is conceptual: a way of reasoning about what honest inference would require. It is not implemented, and no data flow exists that could feed it.

## Ethics and privacy

Affective computing, a term introduced by Picard (1997), is the study and design of systems that recognise, interpret and respond to human emotion. Stark and Hoey (2021) developed a taxonomy of the conceptual models of emotion and the proxy data used in digital analysis of emotional expression, and argued that the paradigms computer scientists have developed or adapted should not simply be trusted to produce ground truth about human emotions. How emotion is conceptualised, sensed, measured and turned into data shapes the ethical and social implications of the resulting systems.

Several concerns follow directly from the methods described above.

**Consent.** Physiological signals are produced continuously and involuntarily. People cannot decline to have a heart rate in the way they can decline to post a message. Meaningful consent to emotional inference has to be specific, informed and revocable, and it is hard to obtain in crowds and public spaces.

**Purpose limitation.** Data collected for one purpose, such as fitness tracking, can support inferences about stress, mood or health that the person never agreed to. A responsible system collects only what a declared purpose requires and does not repurpose it.

**Undisclosed states.** The central risk of emotional inference is not only that it is often wrong, but that it claims access to states people did not choose to disclose. Even a low-confidence inference, once written into a record, can be treated as a fact about the person.

**Power asymmetries.** The same inference means different things depending on who holds it. Between friends it might prompt a kind question. In an employer's dashboard, a school's monitoring system or an insurer's model it can shape evaluation, discipline or price, while the person described has little ability to see, contest or correct it. Use in workplaces and schools deserves particular scrutiny, because participation there is rarely voluntary in practice.

**Validity as an ethical issue.** Given the evidence on autonomic and facial patterns, deploying emotion inference with confident labels is not merely a technical overreach. It exposes people to consequences based on claims the methods cannot support.

This site's own stance follows from these points. It collects no physiological data and no personal data. It uses no analytics, trackers or cookies. The simulation on this page runs entirely in your browser on values you invent, and nothing you enter leaves the page.

## Technical architecture and implementation status

The status table below lists the components of this project and labels each one plainly: implemented, simulation, conceptual or not planned. The labels are part of the argument. A project that criticises confident claims about people should not make confident claims about itself.

What is implemented is publishing infrastructure: the static site, the reference registry checked against Crossref, the evidence ledger with review dates, a versioned content API, and a Rust client library and command-line tool for reading published content. None of these components receives data about readers. The browser simulation is a teaching device that applies the reasoning on this page to invented numbers. The context engine exists only as the description above. Physiological signal ingestion, individual emotion inference or profiling, and analytics or tracking of visitors are not planned, and their absence is a design decision rather than a missing feature.

## Limits of this page

This page is educational. It is not a clinical guideline, a validated measurement protocol or an engineering specification, and it should not be used to assess anyone's emotional or mental state. The signals and confounds it lists are illustrative rather than exhaustive, the temporal model is a heuristic rather than a finding, and the worked examples use invented values. Summaries of studies are deliberately brief; readers who need detail should consult the original sources in the reference list, and the [evidence overview](@/evidence/index.md) shows how claims on this site are graded and reviewed.

If you are worried about your own distress or someone else's, a conversation remains the most informative source available, and for persistent or severe difficulties so does a qualified professional. No sensor replaces either.
