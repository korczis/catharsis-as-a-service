+++
title = "O projektu"
description = "Co je Catharsis as a Service™ a proč vzniklo: motivace, psychologie a teorie v pozadí, principy, jak je postavené a jak byla jeho realizace dozorovaná Majordomem."

[extra]
figures = [
  { kind = "screens", id = "about-cockpit", caption = "Koncepční obrazovky cockpitu Majordomu pro pravidla a worktrees. Data jsou ilustrativní a nepopisují tento projekt.", items = [
    { src = "assets/majordomus/cockpit-rules.png", title = "Pravidla", alt = "Koncepční obrazovka pohledu Pravidla v cockpitu Majordomu: seznam vynucovaných pravidel repozitáře s pokrytím, detail jednoho pravidla, stav jeho validace a místa, kde se vynucuje.", caption = "Spustitelná pravidla s místy vynucení: příkazová řádka, CI, pre-commit hook." },
    { src = "assets/majordomus/cockpit-worktrees.png", title = "Worktrees", alt = "Koncepční obrazovka pohledu Worktrees v cockpitu Majordomu: paralelní větve se stavem, rozdíl změněných souborů, commity napřed a terminál.", caption = "Paralelní větve ve vlastních worktrees, každá navázaná na issue a sezení." },
  ] },
]
+++

Catharsis as a Service™ je první dílo otevřené řady artefaktů Sig Nihl / Prismatic: hotových prací, které s lidskými stavy zacházejí tak, jak inženýři zacházejí se systémy. Pozorují je, pojmenovávají, měří, a stejně je neopraví.

## Co to je

Plakát a stránka. Plakát prodává noc kolektivního uvolnění. Stránka kolem něj tu noc instrumentuje: vstup, proces, výstup, stav. Obě čtení platí zároveň a dílo funguje jen tehdy, když ani jedno nevyhraje.

## Co to není

Není to akce, produkt ani kritika lidí, kteří tančí. Telemetrie je konceptuální; nic tady nikoho neměří. Žádná analytika, žádný tracker, žádná cookie.

## Motivace

Projekt začal pozorováním jazyka. Úleva se nabízí slovníkem služeb: na požádání, opakovatelně, s předvídatelnou odezvou. Večer venku, playlist, místnost na křik nebo nákup se nabízejí jako způsob, jak naložit s tím, co bolí. Úleva je skutečná. Znepokojil nás tichý slib, který ji provází: že pocit uvolnění znamená, že se problém vyřešil.

Psychologie přesně tuto mezeru zkoumá už přes sto let, od katarzní metody Breuera a Freuda přes kontrolované experimenty s ventilací až po metaanalýzy regulace emocí. Její zjištění se ale málokdy dostanou tam, kde se uvolnění prodává. Dílo tu mezeru zviditelňuje; knihovna kolem něj vysvětluje, co víme, jak silně to víme a kde poznání končí.

## Psychologie v pozadí

Argument stojí na několika dobře prozkoumaných myšlenkách; každou vysvětluje vlastní poznámka s literaturou:

- **Katarze jako pojem** — její historie od Aristotela po klinickou praxi: [Co je katarze](@/research/what-is-catharsis/index.cs.md).
- **Ventilace** — proč vyjadřování hněvu skrze vzrušení hněv spíš živí: [Hypotéza ventilace](@/research/venting-hypothesis/index.cs.md).
- **Úleva versus vyřešení** — negativní posílení a proč úleva může problém udržovat: [Úleva není vyřešení](@/research/relief-is-not-resolution/index.cs.md).
- **Kolektivní zážitek** — synchronie, sbližování a kolektivní efervescence: [Kolektivní synchronie](@/research/collective-synchrony/index.cs.md) a [Hudba a regulace emocí](@/research/music-and-emotion-regulation/index.cs.md).
- **Měření** — co signály o stavu říct mohou a co ne: [Měření emocí](@/research/measuring-emotion/index.cs.md) a [stránka o metodách](@/methods/index.cs.md).

## Teorie a souvislosti

Pojmy jako přehodnocení, ruminace, vzrušení nebo alostatická zátěž vysvětluje [slovník pojmů](@/glossary/index.cs.md). Každé tvrzení webu je zapsané v [registru důkazů](@/evidence/index.cs.md) se zdroji, silou důkazů a datem, kdy se musí znovu ověřit. [Knihovna rad](@/advice/_index.cs.md) z těchto důkazů skládá odstupňovaná doporučení s výslovnými limity.

Koncepční obrazovky níže ukazují, jaký dozorový cockpit Majordomus vyvíjí. Jde o ilustrace s vymyšlenými daty; záznamy o tom, jak tento web skutečně vznikl, uvádí [poznámka o metodě](@/research/method-majordomus/index.cs.md).

## Proč řada

Jeden plakát je názor. Řada je metoda: stejná diagnostická gramatika (vstup, proces, výstup, stav) použitá na různé lidské rituály, aby byly vidět rozdíly mezi nimi. Web je postavený tak, aby další artefakt byla dvojice souborů Markdown, ne redesign.

## Principy

- **Dílo vede.** Rozhraní existuje, aby plakát zarámovalo, nikdy aby mu konkurovalo.
- **Poctivé přístroje.** Všechno, co vypadá jako data, je označené jako konceptuální, a stránka sama nic nesbírá.
- **Čitelné bez skriptů.** JavaScript přidává režimy zobrazení, prohlížeč díla a tlačítko pro kopírování; obsah je úplný i bez něj.
- **Dva jazyky, jedna struktura.** Angličtina a čeština jsou rovnocenná vydání a jejich shoda se kontroluje při každém buildu.
- **Tvrzení potřebují důkaz.** Nic se neoznačí za nasazené, dokud nebyla otestována živá URL.

## Jak je to postavené

Statické HTML generované nástrojem [Zola](https://www.getzola.org/) z Markdownu, styly v Tailwind CSS, Flowbite a Alpine.js pro těch pár interaktivních částí. Každý push do `main` projde validací, nasadí se na GitHub Pages, ověří se ve skutečném prohlížeči proti živé URL a vydá se s verzí odvozenou z commitů. Jednotlivé kroky i důvody za nimi vysvětlují [návody](@/guides/index.cs.md).

## Jak byla práce dozorovaná

Web postavil AI agent pro programování pod dohledem nástroje [Majordomus](https://majordomus.dev), dozorové vrstvy mezi agentem a repozitářem. Majordomus web nepsal. Zajistil, aby práce byla doložená a dohledatelná:

- **Úlohy s vymezeným rozsahem.** Každá změna běžela jako úloha s deklarovaným rozsahem. Když se soubory přesunuly mimo něj, [`majordomus watch`](../commands/#majordomus-watch) a [`majordomus check`](../commands/#majordomus-check) nahlásily odchylku ještě před pushem a úloha se znovu spustila se správným rozsahem, místo aby se odchylka přešla.
- **Kontinuita.** Checkpointy a handovery zaznamenaly, co se změnilo a co následuje, takže se na práci dalo navázat podle zaznamenaných faktů, ne podle paměti.
- **Smlouva o dokončení.** Úlohu lze uzavřít jako dokončenou, jen když projde její ověřovací příkaz. Tady je to smoke test proti živému webu, takže „hotovo“ znamená „živé a zkontrolované“.
- **Zapojené vynucování.** Hook `pre-commit` spouští [`majordomus doctor`](../commands/#majordomus-doctor), hook `pre-push` spouští [`majordomus finish --check`](../commands/#majordomus-finish) a CI spouští stejnou kontrolu dozoru při každém pushi i pull requestu.
- **Pravidla vedle kódu.** Projektová pravidla (ověření živého webu před jakýmkoli tvrzením, Zola jako zdroj pravdy, vydání jen z ověřeného `main`) leží v `.ai/repo/rules/` a verzují se spolu s kódem, který řídí.

Praktický výsledek: méně sebejistých tvrzení a víc ověřených.

## Práva

© 2026 Sig Nihl. Všechna práva vyhrazena; na dílo ani text se nevztahuje žádná otevřená licence. Písma (Anton, JetBrains Mono, Barlow Condensed) jsou šířena pod licencí SIL Open Font License 1.1.
