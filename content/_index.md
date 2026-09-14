+++
title = "Catharsis as a Service™"
description = "An artwork and evidence library about collective catharsis: what it is, why relief is not resolution, what psychological research shows, and practical, evidence-graded advice."
template = "index.html"

[extra]
featured = "artifacts/catharsis-as-a-service/index.md"

[extra.intent]
label = "Intent"
heading = "Relief is not resolution."
lead = "Catharsis as a Service™ is an artwork and an evidence library about one widespread confusion: the belief that feeling released means that something has been resolved."
problem_label = "The problem it addresses"
problem = "Contemporary culture sells emotional release as a solution: a night out, a playlist, a scream, a purchase. The sense of relief is real and often valuable. The difficulty lies in what it is mistaken for. When relief is treated as resolution, people repeat what helps in the moment and are left puzzled when the underlying difficulty returns. Psychological research has examined this gap for decades, yet its findings rarely reach the places where release is sold."
cta_research = "Read the research"
cta_advice = "Open the advice library"
audience_label = "Who it is for"
audience = [
  "People who rely on intense experiences to cope and want to understand what those experiences do and do not do.",
  "Readers interested in the psychology of emotion, emotion regulation and collective behaviour.",
  "Artists, designers and technologists who work with the language of data, wellbeing and self-optimisation.",
]
approach_label = "The approach"
approach = [
  { title = "Artwork", text = "A poster and an interactive page that present collective euphoria and then diagnose it as a service transaction." },
  { title = "Evidence", text = "Nine research notes that summarise classical sources and peer-reviewed studies, each with verified references." },
  { title = "Practice", text = "Ten advice entries graded by the strength of their evidence, with concrete steps and explicit limits." },
]

[extra.concept]
label = "What catharsis is"
heading = "A felt release, and an open empirical question."
definition = "In this project, catharsis is a subjectively felt release of emotional tension that follows expression, physical exertion or immersion in an experience. Whether the cause of that tension changes is a separate question, and the answer depends on the emotion, the method and the context."
lenses = [
  { years = "c. 335 BCE", title = "Classical", text = "Aristotle describes tragedy as achieving, through pity and fear, the katharsis of such emotions. Scholars still debate whether he meant purgation, purification or clarification." },
  { years = "1895", title = "Clinical", text = "Breuer and Freud's cathartic method relieved symptoms through the discharge of emotion, known as abreaction. Freud later abandoned it, partly because relief was often temporary." },
  { years = "1986 to today", title = "Empirical", text = "Controlled studies show that venting anger increases aggression, while emotional expression helps when it adds social support, understanding or regulation." },
]
timeline_title = "A timeline of the concept of catharsis"
timeline_description = "Six milestones from Aristotle's Poetics to research on synchrony and social bonding."
timeline_caption = "How catharsis moved from aesthetics to clinical method to an empirical research question."
timeline = [
  { year = "c. 335 BCE", label = "Aristotle, Poetics: katharsis through pity and fear" },
  { year = "1895", label = "Breuer and Freud: the cathartic method and abreaction" },
  { year = "1986", label = "Pennebaker and Beall: writing about trauma and health" },
  { year = "1998", label = "Gross: the emotion regulation framework" },
  { year = "1999–2002", label = "Bushman and colleagues: venting anger does not reduce aggression" },
  { year = "2009–2015", label = "Synchrony research: shared rhythm and social bonding" },
]
link = "research/what-is-catharsis/index.md"
cta = "History and definition"

[extra.mechanism]
label = "How it works"
heading = "The relief loop."
intro = "The artifact models collective catharsis as a four-stage process. Each stage has a documented psychological or physiological basis, and none of them requires the original problem to change."
steps = [
  { name = "Unresolved state", text = "Stress, grief, anger or anxiety with a cause that lies outside the moment." },
  { name = "Repetition", text = "Rhythm and repeated movement narrow attention and interrupt rumination for a while." },
  { name = "Synchronization", text = "Moving in time with others increases closeness and cooperation and raises pain thresholds." },
  { name = "Discharge", text = "Exertion and musical peaks produce an acute lift in mood and a strong sense of release." },
]

[extra.mechanism.loop]
title = "The relief loop"
description = "An unresolved state leads to repetition, synchronization and discharge. Discharge produces temporary relief, and the unchanged state leads back to the start."
caption = "The loop implied by negative reinforcement: relief makes the sequence more likely to repeat while the unresolved state returns."
input = "Unresolved state"
repetition = "Repetition"
synchronization = "Synchronization"
discharge = "Discharge"
relief = "Temporary relief"
loop = "root cause unchanged"

[extra.mechanism.curve]
title = "Two trajectories of distress over time"
description = "Line chart with time on the horizontal axis and distress on the vertical axis. One curve peaks, drops during discharge and returns to baseline; the other declines gradually to a lower level."
caption = "Discharge versus processing. A conceptual illustration of the argument, not measured data."
axis_time = "time"
axis_arousal = "distress"
baseline = "baseline"
discharge = "discharge, then return"
processing = "processing"

[extra.evidence]
label = "Evidence"
heading = "What the research shows."
intro = "Nine research notes separate what studies found from what remains uncertain. Four findings frame the whole project."
read = "Read the note"
notes_label = "Research notes"
cta = "All research notes"
findings = [
  { title = "Venting increases aggression", text = "Hitting a punching bag while thinking about a provocation produced more anger and aggression than sitting quietly.", source = "Bushman, 2002", path = "research/venting-hypothesis/index.md" },
  { title = "Synchrony builds bonds", text = "Group dance in synchrony raised pain thresholds and increased reported closeness to the group.", source = "Tarr et al., 2015", path = "research/collective-synchrony/index.md" },
  { title = "Talking alone is not enough", text = "Talking about an emotional experience felt helpful but did not reduce its emotional impact without cognitive work.", source = "Zech & Rimé, 2005", path = "research/crying-and-sharing/index.md" },
  { title = "Debriefing did not prevent PTSD", text = "A Cochrane review found no preventive effect of single-session debriefing and some evidence of harm.", source = "Rose et al., 2002", path = "research/clinical-perspectives/index.md" },
]

[extra.library]
label = "Advice"
heading = "From evidence to practice."
intro = "Ten recommendations, each graded by the strength of its evidence and paired with concrete steps and explicit limits. They are general education, not a treatment plan."
cta = "Open the advice library"

[extra.making]
label = "How it was made"
heading = "Built in one session. Verified before every claim."
intro = "The site was written by an AI coding agent directed by one person and supervised by Majordomus, a control layer that scopes each task, records progress and refuses to close work that has not been verified on the live site."
cta = "Read the method note"
stats = [
  { value = "51 min 36 s", label = "from an empty repository to the first verified release" },
  { value = "19 min 19 s", label = "from Majordomus initialisation to that release" },
  { value = "2 min 57 s", label = "from push to a verified, published release" },
  { value = "7 / 7", label = "pipeline jobs passed on the first deployment" },
]
points = [
  "Two scope errors and one documentation defect were caught locally before the first push.",
  "Every push to main is validated, deployed, verified in a real browser against the live URL and released automatically.",
  "No speed-up factor is claimed: there was no control condition, and the method note explains what the records can and cannot show.",
]

[extra.faq]
label = "Questions"
heading = "Frequently asked questions."
items = [
  { question = "What is catharsis?", answer = "Catharsis is the idea that expressing an emotion reduces its intensity. The term comes from Aristotle's Poetics, and Breuer and Freud later used it for a clinical method of emotional discharge. Research shows that the feeling of release is real, while its effect on the underlying emotion depends on the emotion and on whether expression includes support, understanding or regulation." },
  { question = "Is venting anger healthy?", answer = "Controlled experiments found that venting anger while focusing on a provocation increased anger and aggression compared with doing nothing. Lowering arousal first and then reappraising the situation, or reflecting on it from a distance, reduces anger more reliably." },
  { question = "Why does dancing with other people feel so good?", answer = "Moving in synchrony increases liking, closeness and cooperation. In group dance, synchrony and physical exertion each raised pain thresholds, an indirect marker of endorphin activity, and peak moments in music are accompanied by dopamine release in the brain's reward system." },
  { question = "If relief is temporary, is it worthless?", answer = "No. Relief supports recovery, energy and connection, and it has value on its own. The distinction matters because relief is often expected to do something it cannot do: change the conditions that produced the distress." },
  { question = "Does this site measure my emotions?", answer = "No. Every metric shown is an artistic value, not a measurement. The site contains no analytics, trackers or cookies, and its source code is public." },
  { question = "Is this medical advice?", answer = "No. The content is educational and based on published research. If distress persists, disrupts daily life, or includes thoughts of harming yourself, contact a qualified professional or local emergency services." },
  { question = "How was the site built, and how long did it take?", answer = "It was built in one working session by an AI coding agent under the supervision of Majordomus (majordomus.dev). The first verified release took 51 minutes and 36 seconds from repository creation. The method note documents the timeline, the kinds of instructions given and what cannot be concluded." },
]
+++
