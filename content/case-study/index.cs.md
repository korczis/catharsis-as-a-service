+++
title = "Případová studie: dodávka s AI pod dozorovou řídicí vrstvou"
description = "Technologické demo toho, jak Majordomus dozoroval AI agenta, který stavěl tento web: životní cyklus úloh, zapojení kontrol, pravidla, rozhodnutí, co dozor zachytil a zaznamenané doklady o dodávce včetně selhání."
date = 2026-09-14
template = "case-study.html"
slug = "pripadova-studie"

[taxonomies]
tags = ["majordomus", "případová studie", "ověřování", "dodávka softwaru"]

[extra]
kicker = "Případová studie · Majordomus"
badge = "Technologické demo · případová studie"
summary = "Jeden člověk řídil AI agenta pro programování, který 14. září 2026 postavil tento dvojjazyčný web pod dozorem Majordomu 0.6.0. Případová studie ze záznamů ledgeru, Gitu a GitHubu ukazuje, jak byla dozorová vrstva nastavená a používaná, co zachytila, co stála a co nekontroluje."
key_points = [
  "Naměřeno, ne odhadnuto: od prvního commitu k ověřenému vydání v0.1.0 uplynulo 51 min 37 s a od inicializace Majordomu k tomuto vydání 19 min 19 s. Žádný násobek zrychlení se neuvádí, protože chybí kontrolní srovnání.",
  "Dozor lokálně odhalil tři problémy s rozsahem úlohy, z toho chybně zadaný rozsah ještě před prvním pushem. CI nezávisle na tom zastavilo jedno nasazení na kontrole referencí a jedno vydání na neúspěšném testu produkce.",
  "Úloha se zaznamenala jako dokončená až poté, co prošel smoke test živého webu. Majordomus šest projektových pravidel vypisuje, vynucují je však validátory projektu, CI a revize.",
]
references = ["majordomus-2026", "repository-2026"]
limits = [
  "Jedno sezení, jeden člověk, jeden agent. Chybí kontrolní podmínka, takže žádný násobek zrychlení odvodit nelze.",
  "Ledger ukládá přijaté operace. Odmítnutý příkaz v něm nezanechá stopu, takže tření je podhodnocené.",
  "Majordomus neposuzuje obsah: hodnocení důkazů, zdravotní formulace a přiměřenost testů patří validátorům projektu, CI a recenzentovi.",
  "Šest projektových pravidel nemá blok x-majordomus. Majordomus je rozpozná a vypíše, ale nevynucuje.",
  "Ověřovací příkaz volí pracovník. Smlouva kontroluje, že proběhl a skončil kódem 0, ne že šlo o správnou kontrolu.",
  "Souběžní pracovníci v jednom checkoutu sdílejí jednu aktivní úlohu, takže kdo co udělal, plyne z jejich zadání a z Gitu, ne z Majordomu.",
  "Ověření živého webu potřebuje nasazení, takže neúspěšný job ověření nechá neověřený build online až do dalšího běhu.",
  "Snímek je kurátorovaný: zadání, texty checkpointů ani lokální cesty se nepublikují a čas, který člověk strávil čtením a rozhodováním, se nikde nezaznamenává.",
]
links = [
  { label = "majordomus.dev", url = "https://majordomus.dev" },
  { label = "Repozitář", url = "https://github.com/korczis/catharsis-as-a-service" },
  { label = "Vrstva .ai/ na GitHubu", url = "https://github.com/korczis/catharsis-as-a-service/tree/main/.ai" },
  { label = "Vydání", url = "https://github.com/korczis/catharsis-as-a-service/releases" },
  { label = "Běhy workflow Pages", url = "https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml" },
  { label = "Formát snímku (docs/CASE-STUDY.md)", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md" },
]

[extra.ui]
metrics_heading = "Zaznamenaná čísla"
metric_tasks = "Dozorované úlohy"
metric_checkpoints = "Checkpointy"
metric_handovers = "Handovery"
metric_decisions = "Rozhodnutí"
metric_findings = "Nálezy"
metric_commits = "Commity"
metric_pipelines = "Běhy pipeline"
metric_releases = "Vydání"
metric_first_release = "Od prvního commitu k prvnímu ověřenému vydání"
metric_first_release_note = "14. září 2026,"
metric_supervised = "od inicializace Majordomu:"
snapshot_prefix = "Snímek záznamů do"
lifecycle_heading = "Životní cyklus úlohy"
lifecycle_intro = "Vyberte krok a uvidíte jeho registrovaný příkaz, důvod, proč existuje, a skutečný zaznamenaný příklad. Každý krok má vlastní adresu, takže odkaz ho otevře přímo."
command = "Příkaz"
what = "Co dělá"
why = "Proč"
example = "Zaznamenaný příklad"
timeline_heading = "Časová osa"
timeline_intro = "Všechny zaznamenané události od nejstarší: úlohy Majordomu, checkpointy, handovery, rozhodnutí a dokončení, nálezy z nich odvozené, commity, běhy pipeline a vydání. Po rozbalení události uvidíte podrobnosti a odkazy. Filtry se ukládají do adresy, takže filtrovaný pohled lze uložit do záložek."
filter_label = "Filtrovat podle druhu"
filter_all = "Vše"
search_label = "Hledat"
search_placeholder = "rozsah, smoke, v0.3.0 …"
reset = "Zrušit filtry"
events_label = "událostí"
no_results = "Těmto filtrům neodpovídá žádná událost."
permalink = "Odkaz na tuto událost"
record_language_note = "Původní záznam je v angličtině."
kind_task = "Úloha"
kind_checkpoint = "Checkpoint"
kind_handover = "Handover"
kind_decision = "Rozhodnutí"
kind_finish = "Dokončení"
kind_finding = "Nález"
kind_commit = "Commit"
kind_pipeline = "Pipeline"
kind_release = "Vydání"
features_heading = "Použité funkce Majordomu"
feature = "Funkce"
how_used = "Jak se použila"
evidence = "Doklad"
wiring_heading = "Zapojení kontrol"
wiring_intro = "Kde která kontrola běží, co spouští a co zastaví. V politice Majordomu jsou deklarované jen dva hooky; ostatní jsou běžné pojistky téhož repozitáře."
where = "Kde"
effect = "Účinek"
file = "Soubor"
findings_heading = "Co dozor zachytil"
findings_intro = "Generováno ze záznamů: nález se zveřejní, jen když ho potvrdí ledger, handover, checkpoint nebo data pipeline. Každá karta odkazuje na své doklady v časové ose."
caught_by = "Zachytil"
no_catcher = "zaznamenáno, žádný příkaz to nevynucuje"
evidence_events = "Doklady"
limits_heading = "Limity"
screens_heading = "Koncepční obrazovky"
screens_disclaimer = "Tyto obrazovky jsou koncepty cockpitu Majordomu s ilustrativními daty. Nezobrazují tento projekt; jeho skutečné záznamy jsou časová osa a čísla výše."
engineering_heading = "Přečtěte si technické články"
engineering_text = "Technická sekce vysvětluje, jak byl zbytek webu postaven a otestován. Odhady ušetřeného času s vyznačenými předpoklady najdete v článku o účtování času; tato případová studie uvádí jen naměřené doby."
engineering_section = "Technické články"
engineering_time = "Účtování času"
sources_heading = "Zdroje a odkazy"

[extra.screens]
id = "case-cockpit"
caption = "Koncepční obrazovky cockpitu Majordomu: sezení, pravidla, worktrees, issues, testy, dokumentace, milníky a využití modelů. Všechna jména, čísla a data v nich jsou ilustrativní."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-sessions.png"
title = "Sezení"
alt = "Koncepční obrazovka pohledu Sezení v cockpitu Majordomu: seznam pracovních sezení a časová osa jednoho sezení od začátku po aktualizaci dokumentace, se zdroji kontextu, které načetlo."
caption = "Každé sezení uchovává časovou osu, zdroje kontextu, rozhodnutí a předávku."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-rules.png"
title = "Pravidla"
alt = "Koncepční obrazovka pohledu Pravidla v cockpitu Majordomu: seznam vynucovaných pravidel repozitáře s pokrytím, detail jednoho pravidla, stav jeho validace a místa, kde se vynucuje."
caption = "Spustitelná pravidla s místy vynucení: příkazová řádka, CI, pre-commit hook."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-worktrees.png"
title = "Worktrees"
alt = "Koncepční obrazovka pohledu Worktrees v cockpitu Majordomu: paralelní větve se stavem, rozdíl změněných souborů, commity napřed a terminál."
caption = "Paralelní větve ve vlastních worktrees, každá navázaná na issue a sezení."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-issues.png"
title = "Issues"
alt = "Koncepční obrazovka pohledu Issues v cockpitu Majordomu: seznam issues a detail jednoho z nich s navázaným worktree, sezením, pull requestem, testy a dokumentací."
caption = "Issue propojené s prací, která ho implementuje a ověřuje."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-tests.png"
title = "Testy"
alt = "Koncepční obrazovka pohledu Testy v cockpitu Majordomu: počty úspěšných a neúspěšných testů, vývoj výsledků, pokrytí, kvalitativní brány a živý výstup testů."
caption = "Běhy testů, selhání a kvalitativní brány na jednom místě, propojené s issues a commity."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-docs.png"
title = "Dokumentace"
alt = "Koncepční obrazovka pohledu Dokumentace v cockpitu Majordomu: strom dokumentů a záznam architektonického rozhodnutí s kontextem, rozhodnutím a důsledky."
caption = "Dokumentace a architektonická rozhodnutí vedle pravidel, která naplňují."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-milestones.png"
title = "Milníky"
alt = "Koncepční obrazovka pohledu Milníky v cockpitu Majordomu: tři milníky s ukazateli postupu, graf kumulativního postupu, časová osa a závislosti."
caption = "Milníky s postupem, harmonogramem a závislostmi odvozenými z plánu issues."

[[extra.screens.items]]
src = "assets/majordomus/cockpit-models.png"
title = "Modely"
alt = "Koncepční obrazovka pohledu Modely v cockpitu Majordomu: poskytovatelé AI modelů s využitím, latencí, rozpisem nákladů a živými požadavky."
caption = "Které modely se použily k čemu, s jakou latencí a za jakou cenu."

[[extra.lifecycle]]
id = "start"
name = "Start s rozsahem"
command_id = "majordomus-start"
what = "Otevře jedinou aktivní úlohu checkoutu s názvem, profilem a cestami, na které smí práce sáhnout."
why = "Rozsah převede to, co měl agent změnit, na seznam, který nástroj dokáže porovnat s pracovním stromem."
example_event = "t-20260914103939-7b10-start"

[[extra.lifecycle]]
id = "check"
name = "Kontrola"
command_id = "majordomus-check"
what = "Bez jakéhokoli zápisu ohlásí, zda je úloha v souladu s politikou, svým rozsahem a zaznamenaným stavem."
why = "Problémy se ukážou na vlastním stroji, dřív než proběhne push nebo běh pipeline."
example_event = "finding-malformed-scope"

[[extra.lifecycle]]
id = "watch"
name = "Hlídání odchylek"
command_id = "majordomus-watch"
what = "Hlásí odchylky mezi zaznamenanou úlohou, jejím rozsahem, politikou a vygenerovanými instrukčními soubory."
why = "Přesun nebo přidání souborů mění, na co úloha sahá, a často to nikdo výslovně nerozhodne."
example_event = "finding-scope-drift"

[[extra.lifecycle]]
id = "checkpoint"
name = "Checkpoint"
command_id = "majordomus-checkpoint"
what = "Zaznamená krátkou poznámku o průběhu o nejvýš 40 řádcích, nebo ji odvodí z Gitu."
why = "Postup práce žije v souboru, ne v konverzaci agenta."
example_event = "checkpoint-20260914t104327z"

[[extra.lifecycle]]
id = "decision"
name = "Zaznamenat rozhodnutí"
command_id = "majordomus-decision"
what = "Přidá datované rozhodnutí s odůvodněním, odmítnutými alternativami a doklady."
why = "Další pracovník vidí, proč je něco tak, jak to je, a člověk může rozhodnutí povýšit na ADR."
example_event = "decision-1"

[[extra.lifecycle]]
id = "handover"
name = "Předání"
command_id = "majordomus-handover"
what = "Zapíše záznam pro navázání s oddíly Objective, Current State a Next Action; větev, commit a změněné soubory doplní Git."
why = "Každý jiný výsledek než completed musí říct, co bude dál, takže restart stojí na zaznamenaných faktech."
example_event = "handover-20260914t111009z"

[[extra.lifecycle]]
id = "finish"
name = "Dokončení s ověřením"
command_id = "majordomus-finish"
what = "Vyhodnotí smlouvu o dokončení. Výsledek completed vyžaduje ověřovací příkaz, který skončí kódem 0; zaznamená se s návratovým kódem a dobou běhu."
why = "Hotovo znamená, že živý web prošel kontrolou, ne že byl napsán kód."
example_event = "t-20260914103939-7b10-finish"

[[extra.lifecycle]]
id = "history"
name = "Čtení ledgeru"
command_id = "majordomus-history"
what = "Vypíše ledger startů, checkpointů, rozhodnutí, handoverů a dokončení, do kterého se jen přidává."
why = "Každé tvrzení na této stránce lze dohledat k některému z jeho řádků."
example_event = "majordomus-init"

[[extra.features]]
name = "Úlohy s rozsahem"
how_used = "Šest úloh začalo s výslovným seznamem cest. Problémy s rozsahem se řešily ukončením úlohy jako partial a startem nové se správným rozsahem."
evidence = "Každý start úlohy v ledgeru nese deklarovaný rozsah; zaznamenány jsou tři restarty."
links = [{ label = "životní cyklus úlohy", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/task-lifecycle.md" }, { label = "start první úlohy", url = "#event-t-20260914102623-44b3-start" }]

[[extra.features]]
name = "Smlouva o dokončení s ověřovacím příkazem"
how_used = "Úlohy uzavřené jako dokončené spustily smoke test produkce proti živé URL; výsledky partial místo toho nesly handover."
evidence = "Každé dokončení v ledgeru ukládá výsledky smlouvy, ověřovací příkaz, jeho návratový kód a dobu běhu."
links = [{ label = ".ai/repo/policy.yaml", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml" }, { label = "první dokončení", url = "#event-t-20260914103939-7b10-finish" }]

[[extra.features]]
name = "Checkpointy"
how_used = "Krátké poznámky o průběhu během úlohy, napsané agentem nebo odvozené z Gitu."
evidence = "Sedm checkpointů v ledgeru; dva odvozené z Gitu uvádějí jen počet změněných souborů."
links = [{ label = "workflow kontinuity", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/continuity.md" }, { label = "odvozený checkpoint", url = "#event-checkpoint-20260914t121646z" }]

[[extra.features]]
name = "Handovery"
how_used = "Psaly se před každým restartem a na konci hlavní úlohy, s oddíly Objective, Current State a Next Action."
evidence = "Čtyři handovery v ledgeru; politika vyžaduje všechny tři oddíly."
links = [{ label = "šablona handoveru", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/prompts/handover.md" }, { label = "handover před restartem", url = "#event-handover-20260914t111009z" }]

[[extra.features]]
name = "Deník rozhodnutí"
how_used = "Rozhodnutí s odůvodněním, odmítnutými alternativami a doklady, zapsaná, dokud byla práce čerstvá."
evidence = "Čtyři zaznamenaná rozhodnutí, každé s odkazem na soubory, které ho implementují."
links = [{ label = "rozhodnutí o ledgeru důkazů", url = "#event-decision-4" }]

[[extra.features]]
name = "Záznamy architektonických rozhodnutí"
how_used = "Rozhodnutí o ledgeru důkazů bylo sepsáno jako ADR-0001 a ponecháno ve stavu návrhu, aby ho přijal člověk."
evidence = "V ledgeru je jeden návrh ADR; soubor ADR má stále stav proposed."
links = [{ label = "ADR-0001", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md" }, { label = "událost návrhu", url = "#event-adr-0001-proposed" }]

[[extra.features]]
name = "Pravidla jako verzované dokumenty"
how_used = "Zafixovaný převzatý základ a šest projektových pravidel, načtené do kontextu agenta a vypsané s třídou a příkazy, které je vynucují."
evidence = "Soubory pravidel v .ai/repo/rules; výpis pravidel ukazuje, že projektová pravidla nemají validátor v Majordomu."
links = [{ label = "projektová pravidla", url = "https://github.com/korczis/catharsis-as-a-service/tree/main/.ai/repo/rules/project" }, { label = "formát pravidel", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/README.md" }]

[[extra.features]]
name = "Kontrola zdraví zapojená do Gitu a CI"
how_used = "Kontrolu zdraví spouští pre-commit hook i job v CI; zároveň porovnává položky vynucování v politice s hooky."
evidence = "Soubor hooku a job Majordomus supervision, který prošel ve všech bězích Pages ve snímku."
links = [{ label = ".githooks/pre-commit", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit" }, { label = ".github/workflows/ci.yml", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml" }]

[[extra.features]]
name = "Instrukční soubory pro poskytovatele"
how_used = "AGENTS.md, CLAUDE.md a GEMINI.md se vygenerovaly z politiky, takže každý agent začíná ze stejného bootstrapu."
evidence = "První událost v ledgeru zaznamenává projekci do tří cílových souborů."
links = [{ label = "AGENTS.md", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/AGENTS.md" }, { label = "událost projekce", url = "#event-majordomus-init" }]

[[extra.features]]
name = "Ledger, do kterého se jen přidává"
how_used = "Každý start, checkpoint, rozhodnutí, handover a dokončení se zaznamenal s časem a commitem Gitu; tato stránka se z něj exportuje."
evidence = "Snímek, ze kterého stránka vychází, a skript, který ho exportuje a kontroluje."
links = [{ label = "data/case_study.json", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/data/case_study.json" }, { label = "scripts/export-case-study.py", url = "https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/export-case-study.py" }]

[[extra.wiring]]
where = "Hook pre-commit v Gitu"
command = "majordomus doctor"
command_id = "majordomus-doctor"
effect = "Odmítne commit, pokud vrstva není v pořádku nebo některé deklarované vynucení není zapojené bez spolknutého návratového kódu."
file = ".githooks/pre-commit"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit"

[[extra.wiring]]
where = "Hook pre-push v Gitu"
command = "majordomus finish --check"
command_id = "majordomus-finish"
effect = "Odmítne push, pokud by aktivní úloha nesplnila smlouvu o dokončení, například kvůli souborům mimo rozsah."
file = ".githooks/pre-push"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-push"

[[extra.wiring]]
where = "Hook commit-msg v Gitu"
command = "scripts/lint-commits.sh --file"
command_id = "lint-commits"
effect = "Odmítne předmět commitu, který není Conventional Commit, protože se z předmětů počítají verze vydání."
file = ".githooks/commit-msg"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/commit-msg"

[[extra.wiring]]
where = "Job v CI: Majordomus supervision"
command = "majordomus doctor"
command_id = "majordomus-doctor"
effect = "Nainstaluje zafixovaný Majordomus 0.6.0 a zopakuje kontrolu zdraví při každém pushi a pull requestu, takže se kontroluje i klon bez hooků."
file = ".github/workflows/ci.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml"

[[extra.wiring]]
where = "Job v CI: Conventional commits"
command = "scripts/lint-commits.sh <range>"
command_id = "lint-commits"
effect = "Zkontroluje každý předmět v pushnutém rozsahu; při selhání se nic nenasadí."
file = ".github/workflows/ci.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml"

[[extra.wiring]]
where = "Workflow Pages: Verify production"
command = "npm run smoke"
command_id = "npm-run-smoke"
effect = "Deploy čeká na CI; Verify production počká, až živý web servíruje pushnutý commit, a spustí proti němu smoke test a Playwright; Release čeká na Verify production."
file = ".github/workflows/pages.yml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/pages.yml"

[[extra.wiring]]
where = "Politika Majordomu"
command = "verification.finish_requires"
command_id = ""
effect = "Smlouva o dokončení vybírá pět požadavků: dodržený rozsah, proběhlé ověření, aktualizovaný stav, žádné otevřené blokery, přítomnou poznámku."
file = ".ai/repo/policy.yaml"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml"

[[extra.wiring]]
where = "Rulesety na GitHubu"
command = "nastavení repozitáře"
command_id = ""
effect = "main vyžaduje CI (s výjimkou pro administrátora), historii main nelze přepsat ani smazat a tagy vydání v* nelze přesunout ani smazat."
file = "pravidlo release-on-verified-main"
file_url = "https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/release-on-verified-main.v1.md"
+++

## Co tato případová studie je (a co není)

Tato stránka dokumentuje jednu dodávku: web, který právě čtete. Vznikl 14. září 2026; postavil ho AI agent pro programování (Claude Code), kterého řídil jeden člověk, a mezi agentem a repozitářem stál jako dozorová řídicí vrstva [Majordomus](https://majordomus.dev) ve verzi 0.6.0. Stránka je pojatá jako technologické demo. Každé číslo na ní je spočítané ze záznamů, které po dodávce zůstaly: z ledgeru Majordomu, z deníku rozhodnutí a handoverů pracovního checkoutu, z historie Gitu a ze záznamů GitHubu o bězích pipeline a vydáních. <a href="#timeline">Časová osa</a> tyto záznamy vykresluje jeden po druhém a každá událost odkazuje na commit, běh, vydání nebo soubor, ze kterého pochází.

Stejně důležité je, čím stránka není:

- **Není to kontrolované srovnání.** Proběhlo jedno sezení s jedním člověkem a jedním agentem a žádné srovnatelné sezení bez dozoru. Z těchto záznamů neplyne žádný násobek zrychlení a stránka ho netvrdí. Uvádí naměřené doby; odhady ušetřeného času s vyznačenými předpoklady přenechává [článku o účtování času](../engineering/time-accounting/).
- **Není to obecné tvrzení o Majordomu.** Ukazuje, jak ho nastavil jeden repozitář, které příkazy běžely, co zaznamenaly a co odmítly. Jiná konfigurace se chová jinak.
- **Není to záznam všeho.** Ledger ukládá přijaté operace. Příkaz, který Majordomus odmítl, v něm nezanechá žádnou položku, takže tření je tu vidět jen tam, kde ho zmiňuje handover, checkpoint nebo commit.
- **Není to přepis konverzace.** Zadání, texty checkpointů a lokální cesty zůstávají v checkoutu. Publikovaný snímek je kurátorovaný a [docs/CASE-STUDY.md](https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md) popisuje, co obsahuje a proč.

[Metodická poznámka](@/research/method-majordomus/index.cs.md) podrobně popisuje první vydání včetně druhů zadání, které práci řídily. Tato stránka se věnuje samotné dozorové vrstvě: jak byla nastavená, jak se používala každá její část a kde přestala pomáhat.

## Výchozí stav

**Agent a člověk.** Agent četl repozitář, spouštěl příkazy, upravoval soubory, commitoval a pushoval. Člověk v prvních fázích poslal zhruba patnáct zpráv: žádosti, výtvarné zadání, dlouhá strukturovaná zadání a krátké pokyny jako „nasaď“, „vydávej automaticky“ nebo „použij Majordomus a vynucuj ho“. Implementační volby dělal agent. Později během dne pracovali na stejném checkoutu souběžně další agenti a druhé sezení; jak, popisuje oddíl o kontinuitě.

**Repozitář.** Web v Zole 0.23.6 v angličtině a češtině, stylovaný Tailwind CSS a doplněný o Alpine.js a Flowbite; validátory v Pythonu, sada testů v Playwrightu a pytest; malý workspace v Rustu, který čte JSON API webu; a workflow GitHub Actions, která nasazují na GitHub Pages a vytvářejí vydání. Web popisuje stránka [O projektu](@/about/index.cs.md) a právě běžící build ukazuje [stránka stavu](@/status/index.cs.md).

**Vrstva Majordomus.** Majordomus drží svůj stav v adresáři [.ai/](https://github.com/korczis/catharsis-as-a-service/tree/main/.ai), který má dvě poloviny:

- `.ai/repo/` je v Gitu a sdílí ho každý checkout. Jeho [manifest](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/manifest.yaml) registruje jednotlivé sekce. [Politika](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/policy.yaml) nastavuje rozpočty kontextu, interval checkpointů výchozího profilu, požadavky smlouvy o dokončení (dodržený rozsah, proběhlé ověření, aktualizovaný stav, žádné otevřené blokery, přítomná poznámka), oddíly, které musí mít handover (Objective, Current State, Next Action), a dvě položky vynucování, které vážou příkazy na hooky Gitu. Existují čtyři [profily](https://github.com/korczis/catharsis-as-a-service/tree/main/.ai/repo/profiles) provádění (implementation, debugging, deep work, routine) a všechny úlohy tu běžely v profilu `implementation`. Pravidla leží v `.ai/repo/rules/`: zafixovaný převzatý základ, který se jen čte, a šest projektových pravidel. Architektonická rozhodnutí leží v `.ai/repo/adrs/`.
- `.ai/local/` Git ignoruje. Obsahuje aktivní úlohu, ledger, do kterého se jen přidává, checkpointy, handovery, deník rozhodnutí a otevřené otázky. Nic z něj nesmí publikovat žádný generátor, a proto tato stránka nese kurátorovaný export, ne samotný adresář.

Z politiky vygeneroval Majordomus tři instrukční soubory, [AGENTS.md](https://github.com/korczis/catharsis-as-a-service/blob/main/AGENTS.md), [CLAUDE.md](https://github.com/korczis/catharsis-as-a-service/blob/main/CLAUDE.md) a [GEMINI.md](https://github.com/korczis/catharsis-as-a-service/blob/main/GEMINI.md). Každý z nich odkáže agenta na `.ai/README.md` a jeho postup vyhledávání kontextu. První událost v ledgeru, v 10:26:23 UTC, je právě tato <a href="#event-majordomus-init">projekce</a>.

**Hooky a CI.** Příkaz [`npm ci`](../commands/#npm-ci) nasměruje Git na adresář `.githooks/` v repozitáři. Workflow CI opakuje kontrolu zdraví Majordomu ve vlastním jobu, takže se kontroluje i klon bez hooků. Všechna místa vynucení uvádí <a href="#wiring">tabulka zapojení</a>.

## Životní cyklus úlohy v praxi

Majordomus dovoluje jednu aktivní úlohu na checkout. <a href="#lifecycle">Diagram životního cyklu</a> výše prochází každý krok s jeho registrovaným příkazem a skutečným zaznamenaným příkladem; tento oddíl vypráví totéž popořadě.

**Start s rozsahem.** [`majordomus start`](../commands/#majordomus-start) otevře úlohu s názvem, profilem a cestami, na které smí sáhnout. První úloha začala v 10:26:23 UTC a nárokovala si 20 cest. Za zaznamenané období začalo šest úloh s rozsahem od jedné cesty po 31.

**Práce a kontrola.** [`majordomus check`](../commands/#majordomus-check) nic nezapisuje: ohlásí, zda je aktivní úloha v souladu s politikou, svým rozsahem a zaznamenaným stavem. [`majordomus watch`](../commands/#majordomus-watch) hlásí odchylky mezi úlohou, jejím rozsahem, politikou a vygenerovanými instrukčními soubory. Společně zachytily dva problémy s rozsahem ještě před prvním pushem (viz <a href="#findings">co dozor zachytil</a>).

**Checkpoint.** [`majordomus checkpoint`](../commands/#majordomus-checkpoint) zaznamená krátkou poznámku o průběhu, kterou politika omezuje na 40 řádků. Zaznamenalo se sedm checkpointů. Čtyři napsal agent; například <a href="#event-checkpoint-20260914t104327z">checkpoint v 10:43:27</a> vznikl hned po prvním pushi, zatímco běžela pipeline. Dva byly odvozeny z Gitu bez jakéhokoli psaného textu a uvádějí jen, kolik souborů se od začátku úlohy změnilo: 65 ve 12:16:46 a 144 ve 12:52:41. Poslední patří úloze, která byla na konci snímku stále aktivní.

**Zaznamenat rozhodnutí.** [`majordomus decision`](../commands/#majordomus-decision) přidá datovaný záznam s odůvodněním, odmítnutými alternativami a doklady. Zaznamenala se čtyři rozhodnutí; najdete je v oddílu o rozhodnutích a ADR.

**Předat práci.** [`majordomus handover`](../commands/#majordomus-handover) zapíše záznam pro navázání se třemi oddíly, které politika vyžaduje. Vznikly čtyři handovery. Tři z nich předcházely o jednu až dvě sekundy ukončení úlohy jako `partial`, což je přesně vzorec, který smlouva o dokončení požaduje: jiný výsledek než `completed` potřebuje poznámku, co bude následovat.

**Dokončit s ověřovacím příkazem.** [`majordomus finish`](../commands/#majordomus-finish) vyhodnotí smlouvu o dokončení. Výsledek `completed` vyžaduje ověřovací příkaz, který proběhl a skončil nulou, a ledger ukládá příkaz, jeho návratový kód a dobu běhu. V tomto repozitáři zvolil agent smoke test produkce, tedy skript za příkazem [`npm run smoke`](../commands/#npm-run-smoke), spuštěný proti živé URL. <a href="#event-t-20260914103939-7b10-finish">První dokončená úloha</a> se uzavřela v 10:47:25 UTC, necelé dvě minuty po publikování vydání v0.1.0, a její ověřovací příkaz skončil kódem 0 po 7 sekundách. Smlouva zaznamenala sedm požadavků jako pass, čtyři jako skipped a žádný jako fail; požadavky, které se na daný výsledek nebo konfiguraci nevztahují, se zaznamenají jako skipped. Druhá dokončená úloha se stejně uzavřela ve 13:08:34, po vydání v0.5.0.

**Přečíst záznam.** [`majordomus history`](../commands/#majordomus-history) vypíše ledger. Snímek, ze kterého tato stránka vychází, se exportoval z jeho výstupu ve formátu JSON.

## Zapojení kontrol

Pravidlo, které nic nespouští, je jen doporučení. Majordomus porovnává položky vynucování ve své politice se skutečností: [`majordomus doctor`](../commands/#majordomus-doctor) selže, když deklarovaný příkaz chybí, není spustitelný, nevolá ho hook, který politika jmenuje, nebo ho volá tak, že spolkne jeho návratový kód. Stojí za tím převzaté pravidlo enforcement-wiring, které vynucuje právě doctor.

- **Pre-commit.** [.githooks/pre-commit](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-commit) odmítne běžet bez nainstalovaného Majordomu a pak spustí [`majordomus doctor`](../commands/#majordomus-doctor). Commit tedy vyžaduje zdravou a zapojenou vrstvu.
- **Pre-push.** [.githooks/pre-push](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/pre-push) spustí [`majordomus finish --check`](../commands/#majordomus-finish), který vyhodnotí smlouvu o dokončení aktivní úlohy, aniž by úlohu uzavřel. Push, který nese práci mimo nárokovaný rozsah, se odmítne dřív, než opustí stroj.
- **Zprávy commitů.** [.githooks/commit-msg](https://github.com/korczis/catharsis-as-a-service/blob/main/.githooks/commit-msg) spustí [`scripts/lint-commits.sh`](../commands/#lint-commits). Conventional Commits se vynucují, protože se z nich počítají verze vydání.
- **Dozorový job v CI.** Job Majordomus supervision v [ci.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml) nainstaluje Majordomus v zafixované verzi 0.6.0 (instalátor ověří SHA-256 vydání), nasměruje Git na hooky a spustí [`majordomus doctor`](../commands/#majordomus-doctor). Prošel ve všech bězích Pages ve snímku.
- **Brány nasazení.** [pages.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/pages.yml) spouští CI, pak Deploy, pak Verify production a nakonec Release. Deploy ověří, že URL Pages odpovídá základní URL v konfiguraci Zoly. Verify production počká, až živý web servíruje pushnutý commit, a pak proti němu spustí smoke test a prohlížečové testy příkazem [`npm run test:production`](../commands/#npm-run-test-production). Release běží, jen když Verify production prošel.
- **Rulesety repozitáře.** Repozitář na GitHubu chrání tři rulesety: `main` vyžaduje CI, historii `main` nelze přepsat ani smazat a tagy `v*` nelze přesunout ani smazat. Požadavek na CI připouští výjimku pro administrátora a první push ji využil.

Vynucováním Majordomu v užším smyslu jsou jen oba hooky. Ostatní jsou běžné pojistky téhož repozitáře a tato zpráva jejich účinky od Majordomu neodděluje.

## Pravidla vedle kódu

Pravidla jsou dokumenty v Markdownu s front matter: `id`, `version`, třída (`blocking` nebo `advisory`) a volitelné závislosti zapsané jako přesné odkazy `id@version`. Platná sada se skládá sčítáním, převzatý základ Majordomu plus vlastní pravidla projektu, a žádný mechanismus přepisu neexistuje. [`majordomus rules list`](../commands/#majordomus-rules) sadu vypíše s třídou každého pravidla a příkazy, které ho vynucují.

Šest projektových pravidel s odkazy na jejich soubory:

- [verified-deployment](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/verified-deployment.v1.md): nic se nehlásí jako nasazené, dokud job ověření ve workflow Pages neprojde proti živé URL, kterou vrátí GitHub.
- [zola-source-of-truth](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/zola-source-of-truth.v1.md): veškeré veřejné HTML generuje Zola; obsah žije v Markdownu, texty rozhraní ve slovnících překladů a šablony sdílejí oba jazyky.
- [release-on-verified-main](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/release-on-verified-main.v1.md): Conventional Commits jsou povinné a každý ověřený push do `main` vytvoří vydání, jehož verze se odvodí z commitů.
- [evidence-ledger](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/evidence-ledger.v1.md): každé veřejné tvrzení je zaznamenané se zdroji, úrovní důkazů, mírou jistoty a datem revize, které ještě neuplynulo.
- [no-neuro-overreach](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/no-neuro-overreach.v1.md): žádná věta nesmí tvrdit, že signál, model nebo oblast mozku odhaluje, co člověk cítí.
- [medical-claims](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/medical-claims.v1.md): zjištění se uvádějí na úrovni skupin i s limity, nikdo se neposuzuje individuálně a každá výzkumná poznámka i rada nese klinické upozornění.

Všech šest je blokujících a jejich závislosti jsou výslovné: evidence-ledger závisí na verified-deployment, no-neuro-overreach na evidence-ledger a medical-claims na obou. Žádné z nich nemá blok `x-majordomus` a výpis pravidel u nich uvádí, že nemají validátor. Je to záměr a stojí to v každém souboru: Majordomus pravidla rozpozná, vypíše a načte do kontextu agenta, vynucují je však validátory projektu, joby v CI a revize. Pro čtení této případové studie je ten rozdíl podstatný. Když build shodí zakázaná formulace nebo tvrzení po datu revize, zachytil to [validátor obsahu](../commands/#validate-content) nebo [validátor ledgeru](../commands/#validate-claims) projektu, ne Majordomus.

Vynucování Majordomu žije v převzatém základu. Čtyři jeho pravidla v této dodávce viditelně pracovala. Scope-integrity nepovažuje práci mimo nárokované cesty za práci úlohy; vynucují ho check, finish a watch. Verification-integrity vyžaduje, aby dokončený výsledek měl ověřovací příkaz, který skončil nulou, se zaznamenaným návratovým kódem a dobou běhu; vynucuje ho finish. Note-integrity vyžaduje, aby každý výsledek nesl poznámku s oddíly, které daný výsledek potřebuje; vynucuje ho také finish. Enforcement-wiring, popsané výše, vynucuje doctor.

## Rozhodnutí a ADR

Pracovní rozhodnutí od trvalého oddělují dva mechanismy.

**Deník rozhodnutí** je lokální, jen se do něj přidává a zápis je levný. [`majordomus decision`](../commands/#majordomus-decision) zaznamená, co se rozhodlo, proč, co se odmítlo a kde jsou doklady. Zapsaly se čtyři položky:

1. <a href="#event-decision-1">Strukturovaná data se sestavují jako data v Teře a serializují přes json_encode</a>. Ručně psané JSON-LD v šablonách se escapuje jako HTML a rozbije se na uvozovkách. Odmítnuto: ručně psané řetězce JSON-LD a skript, který je vkládá v prohlížeči.
2. <a href="#event-decision-2">Náhledy odkazů jsou lokalizované podle jazyka a sitemapa uvádí každou jazykovou verzi</a>. Odmítnuto: jedna anglická náhledová karta pro všechny stránky a jazykové alternativy jen v HTML.
3. <a href="#event-decision-3">Validátory v Pythonu se testují přes pytest v projektovém virtuálním prostředí</a>. Odmítnuto: unittest ze standardní knihovny a globální instalace pytestu.
4. <a href="#event-decision-4">Důkazy se vedou jako datovaný ledger</a> hodnocených zdrojů a odstupňovaných tvrzení a validátory shodí build na zastaralých nebo nekonzistentních položkách. Odmítnuto: volné poznámky o důkazech na každé stránce a jediný soubor, který míchá bibliografická fakta s redakčním úsudkem.

První tři se zaznamenaly během jedné sekundy (11:08:30 až 11:08:31 UTC), krátce před handoverem. Rozhodnutí se tedy zapisovala ve chvíli, kdy se úloha chystala uzavřít, ne průběžně.

**Záznam architektonického rozhodnutí** je v Gitu a je trvalý. Čtvrté rozhodnutí bylo sepsáno jako [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md) s kontextem, rozhodnutím, odmítnutými alternativami a důsledky a ledger ho zaznamenává jako <a href="#event-adr-0001-proposed">navržené ve 12:55:12</a>. Agent ho nepřijal, protože přijetí je úkon člověka. Poslední handover té úlohy uvádí jako další krok přijetí nebo úpravu ADR-0001 a [`majordomus adr list`](../commands/#majordomus-adr) ho stále ukazuje jako návrh. Samotné rozhodnutí je na webu vidět: [stránka důkazů](@/evidence/index.cs.md) a [stránka metod](@/methods/index.cs.md) vykreslují hodnocení z ledgeru, který popisuje.

## Co dozor zachytil

<a href="#findings">Nálezy</a> na této stránce se generují ze záznamů, nepíšou se ručně. Exportní skript deklaruje, co hledat, a nález zveřejní, jen když ho potvrdí ledger, handover, checkpoint nebo data pipeline. Každá karta odkazuje na své doklady v časové ose. Popořadě:

- **Odchylka od rozsahu po přesunu souborů.** První úloha si nárokovala 20 cest, ale ne kořenové soubory přesunuté do adresářů pro dílo a statické soubory. Handover zaznamenává, že odchylku nahlásil [`majordomus watch`](../commands/#majordomus-watch). Úloha skončila jako partial 2 minuty 53 sekund po startu a restartovala se s rozsahem, který tyto soubory jmenoval.
- **Rozsah „.“ před prvním pushem.** Restartovaná úloha zadala jako rozsah jedinou tečku. Majordomus ji nečte jako celý repozitář, takže [`majordomus check`](../commands/#majordomus-check) nahlásil každý změněný soubor jako mimo rozsah. Úloha se v 10:39:39 restartovala s 26 výslovně vyjmenovanými cestami. První push přišel asi o tři minuty později a jeho pipeline prošla všemi sedmi joby.
- **Zadání, které přerostlo rozsah.** Když se práce rozrostla o workspace v Rustu, datové soubory a nástroje pro Python, handover zaznamenal, že nové cesty nejvyšší úrovně leží mimo nárokovaný rozsah. Nová úloha si nárokovala 31 cest.
- **Výjimka z rulesetu.** Checkpoint zapsaný po prvním pushi zaznamenává, že push prošel přes výjimku pro administrátora v rulesetu, který na `main` vyžaduje CI. Samotné nasazení zůstalo podmíněné závislostmi jobů ve workflow. Tohle se zaznamenalo, ne zabránilo.
- **Dokončení jen s kontrolou živého webu.** Obě úlohy uzavřené jako dokončené spustily jako ověřovací příkaz smoke test produkce a oba skončily kódem 0. Tři úlohy ukončené jako partial žádné dokončení netvrdily.
- **Neúspěšná kontrola referencí zastavila nasazení.** Tohle zachytilo CI, ne Majordomus. Běh 34842607207 selhal v jobu References (Crossref) a Deploy, Verify production i Release se přeskočily. Následovala oprava porovnávání názvů (commit 94d734c) a další běh publikoval ve 12:24:28 vydání v0.3.0, sedm minut po startu neúspěšného běhu.
- **Neúspěšné ověření produkce.** Opět CI. Běh 34860959250 nasadil build a pak selhal ve Verify production, když jeden z 84 prohlížečových testů proti živému webu vypršel; Release se přeskočil. Protože ověření živého webu potřebuje nasazení, zůstal neověřený build online až do dalšího běhu. Navazující commit udělal z tohoto testu deterministický a další běh, pro pozdější commit, který ho obsahoval, prošel a publikoval v0.6.0.
- **ADR ponechané člověku.** Popsáno v oddílu o rozhodnutích a ADR.

Tři události zmiňované v jiných popisech této dodávky mezi nálezy nejsou, protože je záznamy nepotvrzují: kontrola zdraví v pre-commit hooku, která měla upozornit, že README neodkazuje na bootstrap pro agenty, příkaz finish odmítnutý do doby, než existoval handover, a závislost pravidla, kterou resolver odmítal, dokud nebyla zapsána jako odkaz `id@version`. Odmítnutí se do ledgeru nezapisují a žádná z těch tří událostí se neobjevuje v handoveru, checkpointu ani commitu. Mohly se stát; tato stránka je nepočítá.

## Kontinuita při restartech a souběžných pracovnících

Restart úlohy byl v zaznamenaném čase levný. Mezi handoverem, ukončením jako partial a dalším startem ledger nikdy neukazuje víc než dvě sekundy. Začalo šest úloh a tři z nich byly restarty. Levné je dělalo to, že stav žil v souborech, ne v konverzaci agenta. Handover nese cíl, aktuální stav a další krok spolu s poli spočítanými z Gitu (větev, commit, čistý nebo změněný strom, změněné soubory), která autor psát nesmí. Politika navíc nechává hooky sezení zapsat briefing při startu epizody, odvozený checkpoint při kompakci konverzace a záznam pro navázání, když epizoda skončí s dosud aktivní úlohou.

Později během dne dodávka prověřila těžší případ: několik pracovníků na jednom checkoutu současně. Na konci snímku je aktivní jedna úloha. Začala ve 14:54:07 UTC a nárokuje si 31 cest, tedy celý pracovní strom. Uvnitř ní pracovali zároveň obsahoví agenti, druhé sezení Claude a hlavní sezení, každý s určením, které soubory jsou jeho. Tuto stránku napsal jeden z těchto pracovníků, který měl zakázáno úlohy startovat, checkpointovat, předávat nebo dokončovat a upravovat soubory ostatních.

Takové uspořádání odhaluje limit. Majordomus vymezuje práci po úlohách a po checkoutech. Uvnitř jednoho checkoutu sdílejí souběžní pracovníci aktivní úlohu a Majordomus nerozliší, kdo změnil který soubor. Koordinace vycházela z výslovného rozdělení cest v zadání každého pracovníka a z Gitu. Převzatý základ formuluje odpověď Majordomu jako principy: jeden pracovník, jeden rozsah, rozsah nárokovaný jiným worktree jako hranice a souběžná práce navzájem izolovaná. Tato dodávka je uvnitř jednoho checkoutu neuplatnila.

## Doklady o dodávce

Vše v tomto oddílu je odkazované a <a href="#timeline">časovou osu</a> lze vyfiltrovat jen na commity, běhy pipeline nebo vydání.

- **Commity.** Každý předmět commitu je Conventional Commit. První, plakát, nese čas 09:54:05 UTC, sekundu před vytvořením repozitáře na GitHubu; web následoval v 10:42:45.
- **Běhy pipeline.** První běh Pages začal v 10:43:02 a skončil v 10:45:45 se sedmi joby, které všechny prošly. Pozdější běhy narostly na deset jobů, jak do CI přibyly testy v Pythonu, job pro Rust a kontrola v Crossrefu. Dva z prvních sedmi běhů selhaly a obě selhání jsou uvedena i s tím, co následovalo.
- **Vydání.** Vydání v0.1.0 bylo publikováno v 10:45:42 po ověření živého webu: 51 minut 37 sekund po prvním commitu a 19 minut 19 sekund po inicializaci Majordomu. Vydání v0.2.0 až v0.5.0 následovala do 13:07:10, každé vytvořené jobem Release v běhu, jehož ověření produkce prošlo.
- **Dokončené úlohy.** Obě dokončené úlohy mají v ledgeru uložený ověřovací příkaz, návratový kód 0 a dobu běhu.

Dvě smyčky lze změřit přímo. Od commitu webu k publikovanému v0.1.0 uplynuly 2 minuty 57 sekund. Od startu běhu, který selhal na referencích, k publikovanému v0.3.0 uplynulo 7 minut 9 sekund. Primárními záznamy jsou [stránka vydání](https://github.com/korczis/catharsis-as-a-service/releases) a [běhy workflow Pages](https://github.com/korczis/catharsis-as-a-service/actions/workflows/pages.yml); tatáž data čte [`gh run list`](../commands/#gh-run-list).

## Co to stálo a co to nevyřešilo

**Tření.** Tři ze šesti úloh skončily jako partial a restartovaly se kvůli tomu, jak byl zadaný jejich rozsah. Dva z těchto restartů proběhly během prvních čtrnácti minut dozoru. Rozsah je nutné psát jako výslovné cesty nejvyšší úrovně a rozrostlé zadání v této dodávce znamenalo úlohu uzavřít a otevřít novou, což odpovídá principu převzatého základu nárokovat cesty při startu úlohy místo tichého rozšiřování rozsahu. Samotné záznamy stály pozornost: sedm checkpointů, čtyři handovery a čtyři rozhodnutí mezi 10:26 a 13:08 UTC a k tomu úloha, která následovala. A protože smlouva o dokončení odmítá výsledek completed bez úspěšného ověřovacího příkazu, nešlo úlohu uzavřít jako dokončenou dřív, než pipeline nasadila a živý web odpověděl.

**Co Majordomus nekontroloval.**

- Zda je obsah pravdivý, dobře podložený a bezpečně formulovaný. To patří validátorům projektu a recenzentovi.
- Zda je ověřovací příkaz přiměřený. Smlouva kontroluje, že příkaz proběhl a skončil nulou; volba smoke testu živého webu byla rozhodnutím agenta.
- Zda testy dávají smysl a zda je padající test nestabilní, nebo odhaluje skutečnou chybu.
- Kdo co udělal uvnitř jednoho checkoutu sdíleného souběžnými pracovníky.
- Šest projektových pravidel, která vypisuje, ale nevynucuje.

**Co záznamy ukázat nemohou.** Odmítnuté příkazy v ledgeru nejsou. Čas, který člověk strávil čtením, rozhodováním a psaním zadání, se nikde nezaznamenává. Doby závisí na hardwaru, síti a frontě CI. A protože vedle Majordomu běžely běžné pojistky (lokální validace, prohlížečové testy, brány CI a rulesety), jejich účinky tu oddělit nelze.

**Co se podle záznamů změnilo.** Každé tvrzení o dokončení v tomto projektu je svázané se zaznamenaným příkazem a jeho návratovým kódem. Chyby v rozsahu se ukázaly lokálně, před jakýmkoli pushem, a ne jako neúspěšné běhy pipeline. A stav potřebný k navázání práce ležel v souborech, které mohl přečíst nový pracovník, což je mimochodem i to, co umožnilo tuto případovou studii napsat.

## Jak to zopakovat

Záznamy jsou ve veřejném repozitáři s výjimkou `.ai/local/`, který checkout nikdy neopouští. Ve vlastním klonu je prozkoumáte takto:

1. Nainstalujte Majordomus z [majordomus.dev](https://majordomus.dev) a spusťte [`npm ci`](../commands/#npm-ci), aby byly hooky aktivní.
2. Zkontrolujte vrstvu příkazem [`majordomus doctor`](../commands/#majordomus-doctor), platná pravidla vypište příkazem [`majordomus rules list`](../commands/#majordomus-rules) a architektonická rozhodnutí příkazem [`majordomus adr list`](../commands/#majordomus-adr).
3. Historii pipeline přečtěte příkazem [`gh run list`](../commands/#gh-run-list) a životní cyklus úlohy v souboru [.ai/repo/workflows/task-lifecycle.md](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/workflows/task-lifecycle.md).
4. V checkoutu s vlastním ledgerem ho vypíše [`majordomus history`](../commands/#majordomus-history) a [`python3 scripts/export-case-study.py`](../commands/#export-case-study) znovu vytvoří snímek, ze kterého tato stránka vychází. S volbou pro kontrolu tentýž skript ověří commitnutý snímek bez lokálního stavu a bez přístupu k síti, a přesně tak s ním zachází CI.

Formát snímku, co obsahuje a co vynechává, popisuje [docs/CASE-STUDY.md](https://github.com/korczis/catharsis-as-a-service/blob/main/docs/CASE-STUDY.md). Jak vznikal zbytek webu, vysvětlují [technické články](../engineering/).
