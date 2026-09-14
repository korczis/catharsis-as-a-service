+++
title = "Metoda: stavba artefaktu podloženého důkazy s Majordomem"
description = "Jak tento web postavil AI agent pod dozorem Majordomu: naměřená časová osa prvního vydání, druhy zadání, co dozorová vrstva zachytila a co tvrdit nelze."
date = 2026-09-14
weight = 6

[taxonomies]
tags = ["metoda", "majordomus", "ověřování", "dodávka softwaru"]

[extra]
kicker = "Výzkumná poznámka 06"
kind = "technical"
summary = "Web se dostal z prázdného repozitáře na GitHubu k ověřenému vydání za 51 minut a 36 sekund a od inicializace Majordomu k tomuto vydání za 19 minut a 19 sekund. Tato poznámka uvádí zaznamenanou časovou osu, druhy zadání, které práci řídily, nálezy, které Majordomus nahlásil ještě před pushem, a limity jakéhokoli tvrzení o rychlosti."
key_points = [
  "Naměřeno ze záznamů repozitáře a pipeline: repozitář vytvořen 14. září 2026 v 09:54:06 UTC, první vydání v0.1.0 ověřeno a publikováno v 10:45:42 UTC.",
  "Majordomus před prvním pushem nahlásil dvě chyby rozsahu úlohy a jedno selhání bootstrapu; první pipeline nasazení prošla všemi sedmi joby.",
  "Kontrolní podmínka neexistuje, proto se neuvádí žádný násobek zrychlení; záznamy ukazují, kde se čas neztratil, a každé tvrzení o dokončení lze ověřit.",
]
figures = [
  { kind = "screens", id = "majordomus-cockpit", caption = "Koncepční obrazovky cockpitu Majordomu: pohledy na sezení, pravidla, worktrees, issues, testy, dokumentaci, milníky a využití modelů. Všechna jména, čísla a data v nich jsou ilustrativní a nepopisují tento projekt; jeho skutečné záznamy uvádí časová osa v této poznámce.", items = [
    { src = "assets/majordomus/cockpit-sessions.png", title = "Sezení", alt = "Koncepční obrazovka pohledu Sezení v cockpitu Majordomu: seznam pracovních sezení a časová osa jednoho sezení od začátku po aktualizaci dokumentace, se zdroji kontextu, které načetlo.", caption = "Každé sezení uchovává časovou osu, zdroje kontextu, rozhodnutí a předávku." },
    { src = "assets/majordomus/cockpit-rules.png", title = "Pravidla", alt = "Koncepční obrazovka pohledu Pravidla v cockpitu Majordomu: seznam vynucovaných pravidel repozitáře s pokrytím, detail jednoho pravidla, stav jeho validace a místa, kde se vynucuje.", caption = "Spustitelná pravidla s místy vynucení: příkazová řádka, CI, pre-commit hook." },
    { src = "assets/majordomus/cockpit-worktrees.png", title = "Worktrees", alt = "Koncepční obrazovka pohledu Worktrees v cockpitu Majordomu: paralelní větve se stavem, rozdíl změněných souborů, commity napřed a terminál.", caption = "Paralelní větve ve vlastních worktrees, každá navázaná na issue a sezení." },
    { src = "assets/majordomus/cockpit-issues.png", title = "Issues", alt = "Koncepční obrazovka pohledu Issues v cockpitu Majordomu: seznam issues a detail jednoho z nich s navázaným worktree, sezením, pull requestem, testy a dokumentací.", caption = "Issue propojené s prací, která ho implementuje a ověřuje." },
    { src = "assets/majordomus/cockpit-tests.png", title = "Testy", alt = "Koncepční obrazovka pohledu Testy v cockpitu Majordomu: počty úspěšných a neúspěšných testů, vývoj výsledků, pokrytí, kvalitativní brány a živý výstup testů.", caption = "Běhy testů, selhání a kvalitativní brány na jednom místě, propojené s issues a commity." },
    { src = "assets/majordomus/cockpit-docs.png", title = "Dokumentace", alt = "Koncepční obrazovka pohledu Dokumentace v cockpitu Majordomu: strom dokumentů a záznam architektonického rozhodnutí s kontextem, rozhodnutím a důsledky.", caption = "Dokumentace a architektonická rozhodnutí vedle pravidel, která naplňují." },
    { src = "assets/majordomus/cockpit-milestones.png", title = "Milníky", alt = "Koncepční obrazovka pohledu Milníky v cockpitu Majordomu: tři milníky s ukazateli postupu, graf kumulativního postupu, časová osa a závislosti.", caption = "Milníky s postupem, harmonogramem a závislostmi odvozenými z plánu issues." },
    { src = "assets/majordomus/cockpit-models.png", title = "Modely", alt = "Koncepční obrazovka pohledu Modely v cockpitu Majordomu: poskytovatelé AI modelů s využitím, latencí, rozpisem nákladů a živými požadavky.", caption = "Které modely se použily k čemu, s jakou latencí a za jakou cenu." },
  ] },
]
references = ["majordomus-2026", "repository-2026"]
+++

## Co vzniklo

Web je dvojjazyčná statická publikace generovaná nástrojem Zola, nasazená na GitHub Pages a při každé změně ověřená proti živé URL. Vznikl během jednoho pracovního sezení; vytvořil ho AI agent pro programování (Claude Code) řízený jedním člověkem a mezi agentem a repozitářem stál jako dozorová vrstva [Majordomus](https://majordomus.dev).

Tato poznámka dokumentuje proces se stejným nárokem, jaký výzkumné poznámky kladou na psychologii: uvést, co bylo naměřeno, oddělit to od interpretace a říct, co z toho vyvodit nelze.

## Zaznamenaná časová osa prvního vydání

Všechny časy jsou v UTC ze 14. září 2026 a pocházejí z historie Gitu, API GitHubu, ledgeru Majordomu a záznamů pipeline.

| Čas | Událost | Zdroj |
|---|---|---|
| 09:45 | Začátek pracovního sezení přestavbou plakátu | časová razítka lokálních souborů |
| 09:54:06 | Vytvořen repozitář na GitHubu; commit plakátu | API GitHubu, Git |
| 10:26:23 | Inicializace vrstvy Majordomus; start první dozorované úlohy | ledger Majordomu |
| 10:29:16 | Nahlášena odchylka od rozsahu po přesunu souborů; úloha restartována | ledger Majordomu |
| 10:39:39 | Chybně zadaný rozsah zachycen kontrolou před pushem; úloha restartována dřív, než proběhl jakýkoli push | ledger Majordomu |
| 10:42:45 | Commit webu; pre-commit hook spustil kontrolu zdraví Majordomu s nulou chyb | Git, výstup hooku |
| 10:43:02–10:45:45 | Pipeline Pages: 7 jobů, 2 minuty 43 sekund, všechny prošly | GitHub Actions |
| 10:45:42 | Vydání v0.1.0 publikováno po ověření živého webu | API GitHubu |
| 10:47:25 | Úloha uzavřena jako dokončená; ověřovacím příkazem byl smoke test živého webu (exit 0, 7 sekund) | ledger Majordomu |

Odvozené doby:

- od vytvoření repozitáře k prvnímu ověřenému vydání: **51 min 36 s**
- od inicializace Majordomu k prvnímu ověřenému vydání: **19 min 19 s**
- od pushe k ověřenému vydání: **2 min 57 s**

V době tohoto vydání web kontrolovalo 7 validačních kroků a 30 prohlížečových testů. Další fáze (náhledy odkazů a strukturovaná data, poté tato výzkumná knihovna a knihovna rad) proběhly ve stejné smyčce a jsou vidět v historii vydání repozitáře.

## Druhy zadání

Práci řídilo zhruba patnáct zpráv od jednoho člověka. Dělily se do pěti typů:

1. **Jednořádková žádost** o založení projektu na GitHubu.
2. **Výtvarné zadání** plakátu, po kterém následovala volba mezi třemi nabídnutými přístupy.
3. **Strukturovaná prováděcí zadání.** Tři dlouhé specifikace rostoucího rozsahu: statická stránka s dílem, interaktivní microsite a vícejazyčný publikační systém s desítkami číslovaných požadavků a výslovnou podmínkou dokončení.
4. **Krátké pokyny během práce:** nasadit, ověřit v prohlížeči, vydávat automaticky, použít Majordomus a vynucovat ho.
5. **Redakční směr:** zavést postupy HTML5 Boilerplate, zlepšit náhledy odkazů a dohledatelnost ve vyhledávačích a nahradit propagační texty seriózní psychologií se zdroji.

Žádná z těchto zpráv neurčovala detaily implementace, jako je syntaxe šablon nebo testovací případy. Ty byly rozhodnutím agenta a úkolem dozorové vrstvy bylo udržet je ověřitelné.

## Co přinesl Majordomus

Majordomus nepsal kód. Práci vymezoval a zaznamenával:

- **Úlohy s vymezeným rozsahem.** Každá změna běžela jako úloha s deklarovanými cestami. Když se soubory přesunuly mimo rozsah, [`majordomus watch`](../../commands/#majordomus-watch) nahlásil odchylku a úloha se restartovala se správným rozsahem. Když byl pozdější rozsah zadán chybně, [`majordomus check`](../../commands/#majordomus-check) před pushem nahlásil všechny soubory jako mimo rozsah; jinak by push odmítl pre-push hook.
- **Kontrola zdraví při každém commitu.** [`majordomus doctor`](../../commands/#majordomus-doctor) běží v pre-commit hooku. Před prvním commitem nahlásil, že README neodkazuje na bootstrap soubor pro agenty; chyba byla opravena dřív, než se dostala do repozitáře.
- **Smlouva o dokončení.** [`majordomus finish`](../../commands/#majordomus-finish) odmítne uzavřít úlohu jako dokončenou, pokud neprojde její ověřovací příkaz. U tohoto webu je to smoke test živé verze, takže „dokončeno“ znamená „nasazeno a zkontrolováno“, ne „napsáno“.
- **Kontinuita.** Checkpointy a handovery zaznamenaly aktuální stav a další krok při každém restartu úlohy, takže restart trval sekundy a opíral se o zaznamenaná fakta, ne o paměť agenta.
- **Pravidla v repozitáři.** Projektová pravidla jako „žádné tvrzení o nasazení bez ověření živého webu“ leží v `.ai/repo/rules/` vedle kódu, který řídí.

## Zrychlilo to vývoj?

Poctivá odpověď zní, že žádný násobek zrychlení uvést nelze. Proběhlo jedno sezení a žádné srovnatelné sezení bez dozoru, takže chybí kontrolní podmínka.

Záznamy ale ukazují, kde se čas neztratil. CI neodmítlo žádný push, žádné nasazení se nemuselo vracet a první běh pipeline prošel všemi sedmi joby. Tři chyby (dvě chyby rozsahu a selhání bootstrapu dokumentace) se staly lokálními nálezy místo neúspěšných běhů pipeline. Každá by stála nejméně jeden další cyklus pushe a čekání v délce několika minut a neúspěšné nasazení by stálo víc.

Větší účinek je na důvěryhodnost než na samotnou rychlost. Každé „hotovo“ v tomto projektu je podložené zaznamenaným příkazem a jeho návratovým kódem, což si čtenář může v repozitáři ověřit příkazem [`majordomus history`](../../commands/#majordomus-history).

## Limity této zprávy

- Časová osa začíná prvním zaznamenaným souborem; plánování, které proběhlo před ním, není zahrnuto.
- Doby závisí na nástrojích, hardwaru a latenci sítě v tomto sezení.
- Sezení se opíralo i o běžné pojistky nezávislé na Majordomu, včetně lokální validace, prohlížečových testů a průběžné integrace. Jejich účinky zde nejsou odděleny.
