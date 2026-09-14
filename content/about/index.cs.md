+++
title = "O projektu"
description = "Co je Catharsis as a Service™, proč vzniklo, na jakých principech stojí, jak je postavené a jak byla jeho realizace dozorovaná Majordomem."
+++

Catharsis as a Service™ je první dílo otevřené řady artefaktů Sig Nihl / Prismatic: hotových prací, které s lidskými stavy zacházejí tak, jak inženýři zacházejí se systémy. Pozorují je, pojmenovávají, měří, a stejně je neopraví.

## Co to je

Plakát a stránka. Plakát prodává noc kolektivního uvolnění. Stránka kolem něj tu noc instrumentuje: vstup, proces, výstup, stav. Obě čtení platí zároveň a dílo funguje jen tehdy, když ani jedno nevyhraje.

## Co to není

Není to akce, produkt ani kritika lidí, kteří tančí. Telemetrie je konceptuální; nic tady nikoho neměří. Žádná analytika, žádný tracker, žádná cookie.

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
