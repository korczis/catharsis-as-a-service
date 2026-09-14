+++
title = "Catharsis as a Service™"
description = "An artwork and evidence library about collective catharsis: what it is, why relief is not resolution, what psychological research shows, and practical, evidence-graded advice."
template = "index.html"

[extra]
featured = "artifacts/catharsis-as-a-service/index.md"

[extra.purpose]
body = [
  "A demonstration is only as good as the records behind it, so this page asks for no trust. The build history, the sources behind each claim and the rules the work followed are public, and every item below links to the record it describes.",
  "The subject matter is handled as academic work, not as marketing. The library summarises classical sources and peer-reviewed research at group level, grades the strength of that evidence and states its limits. It is an educational publication, not a medical resource, and it does not assess or advise individuals.",
]
label = "Why this site exists"
heading = "A case study in supervised, verifiable development."
lead = "Catharsis as a Service™ was created primarily as a technical demonstration and case study: for Majordomus (majordomus.dev), a supervisory control layer for AI-assisted development, and for Prismatic, as an example of development in which every public statement is sourced, graded and checkable. The artwork and the research library are the material on which both are demonstrated."
verify_label = "Check it yourself"
verify = [
  { title = "Source code", text = "The repository with its full commit history, validators, tests and workflow definitions.", url = "https://github.com/korczis/catharsis-as-a-service" },
  { title = "Pipeline runs", text = "Validation, deployment and verification against the live URL for every push to main.", url = "https://github.com/korczis/catharsis-as-a-service/actions" },
  { title = "Releases", text = "A release is published only after the live site has passed verification.", url = "https://github.com/korczis/catharsis-as-a-service/releases" },
  { title = "Build status", text = "The revision and content version of this build and the current statistics of the evidence ledger.", path = "status/index.md" },
  { title = "Evidence ledger", text = "Every claim with its type, evidence level, confidence, sources and review date.", path = "evidence/index.md" },
  { title = "API", text = "A versioned JSON export of the pages, the evidence ledger and the glossary.", file = "api/v1/index.json" },
]

[[extra.purpose.cases]]
label = "Case 01 · Majordomus"
title = "AI-assisted development under supervision"
text = "The site was written by an AI coding agent directed by one person. Majordomus scoped each task to declared paths, recorded its progress and accepted a task as finished only when its verification command passed."
points = [
  "Two scope errors and one bootstrap failure were reported locally before the first push; the method note gives the recorded timeline.",
  "Rules, workflows and context for any AI worker are kept in a provider-neutral .ai/ directory, versioned with the code.",
  "A deployment counts as complete only after the Pages workflow has verified the live URL, and a release is cut only after that check.",
]
links = [
  { label = "Method note", path = "research/method-majordomus/index.md" },
  { label = "Engineering articles", path = "engineering/_index.md" },
  { label = "majordomus.dev", url = "https://majordomus.dev" },
]

[[extra.purpose.cases]]
label = "Case 02 · Prismatic"
title = "Development that can be verified"
text = "Content is held to the same standard as code. A claim may be published only when the evidence ledger records it with appraised sources, an evidence level no stronger than its best source and a review date that has not passed; otherwise the build fails."
points = [
  "Journal articles in the bibliography must carry a DOI, and references are checked against Crossref.",
  "Overclaiming phrases listed in the content standards, missing clinical disclaimers and gaps between the English and Czech editions fail validation or the end-to-end tests.",
  "Every command mentioned in the documentation is registered together with the test that runs it.",
]
links = [
  { label = "Evidence ledger", path = "evidence/index.md" },
  { label = "Methods", path = "methods/index.md" },
  { label = "Command registry", path = "commands/index.md" },
]

[extra.intent]
body = [
  "The piece starts from an ordinary experience. After a concert, a long run, an argument that ends in shouting or a night of dancing, many people feel lighter, and the feeling is real, even when the body is still activated. What the site questions is the inference that often follows, that the lightness means the thing that weighed on them has been dealt with.",
  "That inference matters because it shapes behaviour. If relief is read as resolution, the relieving activity is repeated whenever the pressure returns, and the pressure keeps returning because nothing about its source has changed. Learning theory calls this negative reinforcement; everyday language calls it coping that has quietly stopped working.",
  "The library does not argue against relief. It separates three questions that are usually merged into one: what changed in the body, what changed in understanding, and what changed in the situation. Every research note, theory essay and advice entry is written to keep those questions apart.",
]
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
  { title = "Artwork", text = "A poster and an interactive page that present collective euphoria and then describe it as a service transaction." },
  { title = "Evidence", text = "Research notes that summarise classical sources and peer-reviewed studies, each with its references." },
  { title = "Practice", text = "Advice entries graded by the strength of their evidence, with concrete steps and explicit limits." },
]

[extra.concept]
body = [
  "The word has travelled far from its origin. In Aristotle it described what tragedy does to an audience, and scholars still disagree whether he meant a purging, a purification or a clarification of emotion. Breuer and Freud borrowed it for a clinical method in which recalling a painful memory with strong emotion relieved symptoms, at least for a while.",
  "Popular culture of the twentieth century turned the idea into a hydraulic picture: emotion builds up like pressure and must be let out, or it will burst out somewhere else. The picture is intuitive and still common in advice about anger, grief and stress. Experimental psychology has tested it many times, and in its simple form it has not held up.",
  "What remains is a narrower and more useful idea. Expressing emotion tends to help when it adds something: support from other people, a new understanding, a different appraisal of the situation, or a decision to act. Expression that only rehearses the emotion tends to keep it going.",
]
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
body = [
  "The model is deliberately simple, so that each step can be checked against research. Repetition and rhythm narrow attention; moving in time with others is associated with closeness and higher pain thresholds; physical and musical peaks are followed by a strong sense of release. None of these steps requires the original difficulty to change.",
  "The loop closes because relief is rewarding. Whatever reliably comes before relief becomes more likely next time, which is why the same ritual can be sought again and again. On the interactive models page you can change the size of the relief and the chance that the cause changes, and watch the urge to repeat grow or fade.",
]
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
body = [
  "Every claim on the site is recorded in an evidence ledger with its type, an evidence level from A to E, a confidence rating and a date by which it must be reviewed again. A claim is never graded more strongly than its best source, and the build fails when a review date passes.",
  "Grades describe the strength of the underlying study designs, not the importance of a topic. Much of what matters about catharsis, grief and collective experience has been studied mainly with correlational or qualitative designs, and the ledger says so rather than presenting those findings as experiments.",
]
label = "Evidence"
heading = "What the research shows."
intro = "The research notes separate what studies found from what remains uncertain. Four findings frame the whole project."
read = "Read the note"
notes_label = "Research notes"
cta = "All research notes"
cta_ledger = "Evidence ledger"
cta_methods = "Methods"
cta_glossary = "Glossary"
findings = [
  { title = "Venting increases aggression", text = "Hitting a punching bag while thinking about a provocation produced more anger and aggression than sitting quietly.", source = "Bushman, 2002", path = "research/venting-hypothesis/index.md" },
  { title = "Synchrony builds bonds", text = "Group dance in synchrony raised pain thresholds and increased reported closeness to the group.", source = "Tarr et al., 2015", path = "research/collective-synchrony/index.md" },
  { title = "Talking alone is not enough", text = "Talking about an emotional experience felt helpful but did not reduce its emotional impact without cognitive work.", source = "Zech & Rimé, 2005", path = "research/crying-and-sharing/index.md" },
  { title = "Debriefing did not prevent PTSD", text = "A Cochrane review found no preventive effect of single-session debriefing and some evidence of harm.", source = "Rose et al., 2002", path = "research/clinical-perspectives/index.md" },
]

[extra.library]
body = [
  "The advice is written for adults thinking about their own habits. Each entry states how strong the evidence behind it is, what to do in concrete steps, and where the recommendation stops applying. None of it replaces individual help, and several entries name the situations in which a professional is the right next step.",
]
label = "Advice"
heading = "From evidence to practice."
intro = "Recommendations, each graded by the strength of its evidence and paired with concrete steps and explicit limits. They are general education, not a treatment plan."
cta = "Open the advice library"

[extra.making]
body = [
  "The supervision layer made the work slower in small ways and faster in large ones. Every task had a declared scope, every completion claim had a verification command, and every deployment was checked against the live site before a release was published. Mistakes surfaced as local findings instead of broken pages.",
  "The concept screens show where the tooling is heading: a cockpit over sessions, rules, tests and milestones. Their data is illustrative. The real records of this project are its commits, its pipeline runs and the method note.",
]
label = "How it was made"
heading = "First release in one session. Verified before every claim."
intro = "The site was written by an AI coding agent directed by one person and supervised by Majordomus, a control layer that scopes each task, records progress and refuses to close work that has not been verified on the live site."
cta = "Read the method note"
cta_case = "Majordomus case study"
cta_engineering = "Engineering articles"
stats = [
  { value = "51 min 36 s", label = "from an empty repository to the first verified release" },
  { value = "19 min 19 s", label = "from Majordomus initialisation to that release" },
  { value = "2 min 57 s", label = "from push to a verified, published release" },
  { value = "7 / 7", label = "pipeline jobs passed on the first deployment" },
]
points = [
  "Two scope errors and one bootstrap failure were caught locally before the first push.",
  "Every push to main is validated, deployed, verified in a real browser against the live URL and released automatically.",
  "No speed-up factor is claimed: there was no control condition, and the method note explains what the records can and cannot show.",
]

[extra.faq]
label = "Questions"
heading = "Frequently asked questions."
items = [
  { question = "What is catharsis?", answer = "Catharsis is the idea that expressing an emotion reduces its intensity. The term comes from Aristotle's Poetics, and Breuer and Freud later used it for a clinical method of emotional discharge. Research shows that the feeling of release is real, while its effect on the underlying emotion depends on the emotion and on whether expression includes support, understanding or regulation." },
  { question = "Is venting anger healthy?", answer = "Controlled experiments found that venting anger while focusing on a provocation increased anger and aggression compared with doing nothing. Lowering arousal first and then reappraising the situation, or reflecting on it from a distance, reduces anger more reliably." },
  { question = "Why does dancing with other people feel so good?", answer = "Moving in synchrony increases liking, closeness and cooperation. In a study of group dance, synchrony and physical exertion each raised pain thresholds, which are used as an indirect marker of endorphin activity, and in an imaging study peak moments of musical pleasure were associated with dopamine release in reward-related regions (Salimpoor et al., 2011)." },
  { question = "If relief is temporary, is it worthless?", answer = "No. Relief supports recovery, energy and connection, and it has value on its own. The distinction matters because relief is often expected to do something it cannot do: change the conditions that produced the distress." },
  { question = "Does this site measure my emotions?", answer = "No. Every metric shown is an artistic value, not a measurement. The site contains no analytics, trackers or cookies, and its source code is public." },
  { question = "Is this medical advice?", answer = "No. The content is educational and based on published research. If distress persists, disrupts daily life, or includes thoughts of harming yourself, contact a qualified professional or local emergency services." },
  { question = "How was the site built, and how long did it take?", answer = "The first release was built in one working session by an AI coding agent under the supervision of Majordomus (majordomus.dev), 51 minutes and 36 seconds after the repository was created. Later phases followed the same supervised loop and are listed in the release history. The method note documents the timeline, the kinds of instructions given and what cannot be concluded." },
  { question = "Why does this site exist?", answer = "Primarily as a technical demonstration and case study: of Majordomus, a supervisory control layer for AI-assisted development, and of Prismatic's standard of verifiable work, in which every public claim is sourced, graded and dated for review. The artwork and the research library are the material the demonstration is built on, and both are held to that standard." },
]

[extra.making.screens]
id = "making-cockpit"
caption = "Concept screens of a Majordomus cockpit for sessions, tests and milestones. The data in them is illustrative and does not describe this project; the measured timeline is in the method note."
items = [
  { src = "assets/majordomus/cockpit-sessions.png", title = "Sessions", alt = "Concept screen of the Majordomus cockpit Sessions view: a list of working sessions and the timeline of one session from start to updated documentation, with the context sources it loaded.", caption = "Each session keeps its timeline, context sources, decisions and handover." },
  { src = "assets/majordomus/cockpit-tests.png", title = "Tests", alt = "Concept screen of the Majordomus cockpit Tests view: pass and fail counts, a results trend, coverage, quality gates and live test output.", caption = "Test runs, failures and quality gates in one place, linked to issues and commits." },
  { src = "assets/majordomus/cockpit-milestones.png", title = "Milestones", alt = "Concept screen of the Majordomus cockpit Milestones view: three milestones with progress bars, a cumulative progress chart, a timeline and dependencies.", caption = "Milestones with progress, schedule and dependencies derived from the issue plan." },
]

[extra.statement]
body = [
  "Physiological recovery is a normal and valuable process. After a stress response, heart rate, blood pressure and stress hormones return towards their baseline, and a prolonged failure to return is associated with cumulative wear on the body. Recovery is worth protecting.",
  "Recovery, however, describes the organism, not its circumstances. A person can sleep, run, cry, sing or dance their way back to baseline while the rent is still unpaid, the relationship still unrepaired and the loss still a loss. The line relief detected ≠ cause resolved is a reminder to ask about both.",
]
label = "Thesis"
lines = ["The body can change state", "without the world", "changing with it."]
text = "Heart rate settles, muscles loosen, a crowd disperses and a person reports relief. All of that can be real, and much of it can be recorded. None of it shows that the debt, the conflict, the loss or the working conditions behind the distress have changed. That gap is the whole argument of the artwork, stated as plainly as possible."
formula = "relief detected ≠ cause resolved"
cta_methods = "The temporal model"
cta_note = "Relief is not resolution"

[extra.venting]
body = [
  "The distinction has practical consequences. Advice to hit pillows, scream into cushions or get anger out through exhausting effort rests on the hydraulic picture. Controlled studies suggest that bringing arousal down first, and then thinking about the situation from some distance, is the more reliable route to calmer feelings and less aggression.",
  "None of this makes physical activity or strong feeling suspect. Exercise has its own benefits for mood, and shouting at a concert is not a clinical problem. The point is narrower: when the goal is to reduce anger, the method that feels most like release is not the one that works best.",
]
label = "Catharsis is not venting"
heading = "Release is not the same as blowing off steam."
lead = "Catharsis names a felt release. Venting names a strategy: expressing anger through high-arousal activity in the expectation that it will drain away. The two are often treated as one, and the evidence separates them."
contrast = [
  { label = "Raising arousal", title = "Activities that increase arousal", value = "g = −0.02", text = "Across studies, activities that raised physiological arousal did not reliably reduce anger or aggression; the confidence interval spans zero." },
  { label = "Lowering arousal", title = "Activities that decrease arousal", value = "g = −0.63", text = "Activities that lowered arousal were associated with a moderate reduction in anger and aggression across studies and samples." },
]
stats = [
  { value = "154", label = "studies" },
  { value = "184", label = "samples" },
  { value = "10,189", label = "participants" },
]
source = "Kjærvik, S. L., & Bushman, B. J. (2024). Meta-analysis in Clinical Psychology Review, 109, 102414."
meaning = "The felt release after shouting or pounding something is real. What the evidence does not support is the expectation that discharging arousal reduces the anger that follows. Lowering arousal first, and then working with the situation, does better."
cta_note = "The venting hypothesis"
cta_advice = "Let anger cool"

[extra.questions]
body = [
  "Good questions keep relief and resolution apart without dismissing either. They are not tests to pass. They are ways of noticing whether a habit still does what it is used for.",
]
label = "Better questions"
heading = "Better questions than: did it help?"
intro = "Whether an experience felt good is the easiest question and the least informative one. These questions follow the research on emotion regulation and on what happens after relief."
items = [
  { instead = "Did I feel better?", better = "What exactly changed: my body, my mood, my understanding, or the situation?" },
  { instead = "Should I let it all out?", better = "Does expressing this lower my arousal and lead somewhere, or does it keep me rehearsing the provocation?" },
  { instead = "Why does it keep coming back?", better = "What did the relief make easier to avoid?" },
  { instead = "Is this normal?", better = "Is it lasting longer, growing stronger, or disrupting sleep, work or relationships?" },
  { instead = "How do I get that high again?", better = "Which parts of that experience, such as movement, music or other people, can I bring into an ordinary week?" },
  { instead = "Did the night out fix it?", better = "What is one concrete step toward the cause, and who could take it with me?" },
]

[extra.boundary]
body = [
  "Descriptions of research here are about groups of people studied under particular conditions. They cannot say what a particular reader is going through or what will help them. If what you are experiencing is severe, lasting or frightening, the most useful step is to talk with someone qualified who can listen to your situation.",
]
label = "Clinical boundary"
heading = "Where this site stops."
text = "This is an educational publication. It summarises group-level research, it cannot assess an individual, and nothing on it measures you. Some experiences need a qualified professional rather than an article."
signs_label = "Contact a qualified professional if"
signs = [
  "distress lasts for weeks or keeps intensifying",
  "sleep, work, study or relationships are disrupted",
  "relief depends on alcohol, drugs or risky behaviour",
  "a traumatic event keeps returning as intrusive memories, nightmares or avoidance",
]
urgent = "If you have thoughts of harming yourself or someone else, contact local emergency services or a crisis line now."
cta_advice = "After a traumatic event"
cta_evidence = "How claims are graded"

[extra.explore]
label = "Explore"
heading = "Nine ways into the library."
intro = "The artwork asks a question; the library answers it at different depths. Start where your question is: a finding, a theory, a model you can change, a practical step, the grading behind a claim, a term, or a search across everything."
items = [
  { title = "Research notes", text = "What studies found about venting, synchrony, crying, grief, sleep, exercise and measurement, with limits stated next to findings.", path = "research/_index.md" },
  { title = "Theory", text = "The frameworks behind the findings: catharsis theories, the process model of emotion regulation, appraisal, constructed emotion, avoidance learning, allostasis and ritual.", path = "theory/_index.md" },
  { title = "Interactive models", text = "Five small simulations of relief, arousal, remembered discomfort, synchrony and stress load, labelled as illustrations rather than predictions.", path = "models/index.md" },
  { title = "Advice", text = "Evidence-graded recommendations with concrete steps and explicit limits, written for adults thinking about their own habits.", path = "advice/_index.md" },
  { title = "Evidence ledger", text = "Every claim with its type, level, confidence, sources and review date, and a changelog of what was revised.", path = "evidence/index.md" },
  { title = "Glossary", text = "Psychological, physiological and methodological terms defined in plain language, linked to notes and sources.", path = "glossary/index.md" },
  { title = "Search", text = "Find notes, essays, advice and terms in either language; matching ignores accents and runs in your browser.", path = "search/index.md" },
  { title = "Case study", text = "How the site was built with an AI coding agent under Majordomus supervision, with an interactive timeline of the real task, commit, pipeline and release records.", path = "case-study/index.md" },
  { title = "Engineering", text = "Technical articles on the architecture, the evidence ledger as code, testing, parallel agents, interactive models and an honest account of time spent and saved.", path = "engineering/_index.md" },
]

[extra.statement.poster]
id = "poster-thesis"
caption = "From the Catharsis as a Service poster series. Slogans and numbers on the posters belong to the artwork; they are not findings."
items = [
  { src = "assets/posters/zvedavost-meni-realitu.png", title = "Curiosity changes reality", alt = "Poster in black and red: the Czech headline ZVĚDAVOST MĚNÍ REALITU (curiosity changes reality) above a figure walking towards a glowing red doorway between walls of screens; side panels list input, process and output, and an artistic telemetry box ends with root cause: unchanged.", caption = "Not to escape life, but to see it more clearly." },
]

[extra.venting.poster]
id = "poster-venting"
caption = "From the Catharsis as a Service poster series. Slogans and numbers on the posters belong to the artwork; they are not findings."
items = [
  { src = "assets/posters/vice-dat-mene-iluzi.png", title = "More data. Fewer illusions.", alt = "Poster: VÍCE DAT. MÉNĚ ILUZÍ. (more data, fewer illusions) over a crowd with raised hands in front of a stage with a glowing red gate; below, the request POST /v1/catharsis → 200 OK with problem_solved: false and an artistic telemetry panel.", caption = "The endpoint answers, the crowd dances, the root cause stays unchanged." },
]

[extra.questions.poster]
id = "poster-questions"
caption = "From the Catharsis as a Service poster series. Slogans and numbers on the posters belong to the artwork; they are not findings."
items = [
  { src = "assets/posters/tezsi-otazky.png", title = "Harder questions. A better world.", alt = "Poster: TĚŽŠÍ OTÁZKY. LEPŠÍ SVĚT. (harder questions, a better world). A hiker climbs a glowing red path towards a doorway on a mountain; signposts on the left read comfort, distraction, noise, same patterns and illusions, on the right curiosity, evidence, context, perspective and better decisions.", caption = "Not to know more answers, but to ask better questions." },
]

+++
