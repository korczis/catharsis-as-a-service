+++
title = "Návody"
description = "Jak číst artefakt, sdílet ho, publikovat nové dílo, přidat jazyk, ověřit nasazení a pracovat pod Majordomem, i s důvody za každým krokem."
+++

Praktické návody pro čtenáře, pro ty, kdo dílo sdílejí, i pro toho, kdo bude publikovat další artefakt. Každý návod říká, co udělat a proč se to dělá právě takhle.

## Jak číst artefakt

Začněte plakátem, ne textem. První čtení je kampaň; nechte ji dopadnout dřív, než začnete hledat diagnózu.

1. Zobrazení **Prožitek** ukazuje přechod stavu jako posloupnost: vstup, proces, výstup.
2. Zobrazení **Diagnostika** ukazuje stavovou matici. HTTP status a stav problému si záměrně odporují.
3. Zobrazení **Surová data** říká totéž jako odpověď API, pro ty, kdo věří víc JSONu než plakátům.

Tabulka pozorovatelnosti používá umělecké hodnoty. Pruhy ukazují intenzitu, ne měření, a červené řádky jsou ty, které se nezměnily.

**Proč je to postavené takhle:** rozpor mezi `200 OK` a `problem_solved: false` je samotné dílo. Každé zobrazení ten rozpor vyjadřuje jiným jazykem, místo aby ho vysvětlovalo pryč.

## Sdílení a náhledy odkazů

Každá stránka nese metadata Open Graph a Twitter Card, takže messengery a sociální sítě ukážou pořádnou náhledovou kartu místo holé adresy.

- Anglické stránky používají anglickou náhledovou kartu, české stránky českou kartu s přeloženým podtitulem.
- Každá jazyková verze odkazuje na tu druhou přes `hreflang` a `og:locale:alternate`, takže sdílený český odkaz zůstane český.
- Vyhledávače dostávají strukturovaná data (WebSite, VisualArtwork, BreadcrumbList) a smějí zobrazit velký náhled obrázku.

Pokud chcete sdílet konkrétní jazyk, odkazujte přímo na něj: `/` pro angličtinu, `/cs/` pro češtinu. Anglická úvodní stránka přesune návštěvníka s českým prohlížečem při první návštěvě na českou verzi, ale přímý odkaz má vždy přednost.

**Proč:** náhled odkazu je často jediná část díla, kterou člověk uvidí. Měl by nést stejné napětí mezi prvním a druhým pohledem jako plakát, a to v jazyce čtenáře.

## Publikování nového artefaktu

1. Vytvořte `content/artifacts/<slug>/index.md` zkopírováním existujícího artefaktu a zachovejte stejnou strukturu front matter.
2. Vytvořte `content/artifacts/<slug>/index.cs.md` s přeloženým textem. Struktura se musí shodovat; mění se jen hodnoty.
3. Master plakátu dejte do `static/assets/` a nastavte na něj `extra.poster`. Responzivní verze WebP se generují při buildu.
4. Náhled spusťte přes `npm run dev`, potom `npm run validate` a `npm test`.
5. Commitněte s konvenční zprávou, například `feat(content): add <slug>`, a pushněte do `main`.

**Proč:** výpis, sitemapa, feedy, jazykové odkazy, náhledy i strukturovaná data se odvozují z těch dvou souborů. Není co dalšího upravovat, takže není na co zapomenout.

## Přidání jazyka

1. Do `zola.toml` přidejte `[languages.<code>]` s názvem, popisem a úplnou tabulkou `translations`.
2. Kód jazyka přidejte do `extra.locales`.
3. Ke každému obsahovému souboru přidejte soubor `*.<code>.md`.
4. Spusťte `npm run validate`; kontrola i18n vypíše každý chybějící soubor nebo řetězec.

Nemusí se měnit žádná šablona, skript ani workflow. Je to záměrné omezení návrhu, ne náhoda: šablony se nikdy nevětví podle jazyka, takže nový jazyk nemůže vyžadovat práci na šablonách.

## Ověření nasazení

Zelený build není nasazení. Pipeline bere jako jediný důkaz živou URL:

1. **validate** postaví web a zkontroluje překlady, odkazy, kotvy, metadata, strukturovaná data a základy přístupnosti.
2. **e2e** spustí prohlížečové testy proti lokální kopii servírované pod stejnou podcestou jako GitHub Pages, takže chyby v základní cestě selžou dřív, než se dostanou ven.
3. **deploy** odmítne publikovat, pokud Pages hlásí jinou základní URL, než pro jakou byl web postaven.
4. **verify** počká, až produkce servíruje nový commit, a pak proti živému webu spustí smoke test i celou sadu prohlížečových testů.
5. **release** označí verzi až po úspěšném verify.

Ruční kontrola:

```sh
npm run smoke            # každá stránka a asset živého webu
npm run test:production  # prohlížečové testy proti živé URL
gh run list --workflow pages.yml --limit 5
```

**Proč:** většina skutečných chyb statických webů (špatná podcesta, zastaralá CDN, chybějící asset) je v buildu neviditelná a na živé URL zjevná.

## Práce pod Majordomem

Tento repozitář dozoruje Majordomus. Postup při změně:

```sh
majordomus start "<úloha>" --scope content,templates
majordomus check                      # než prohlásíte pokrok
majordomus checkpoint < poznamka.md   # pokrok, který stojí za zaznamenání
majordomus finish --outcome completed --verify-command "npm run smoke"
```

Co přináší a proč na tom tady záleží:

- **Rozsah úlohy** zabrání tomu, aby změna obsahu potichu sáhla na pipeline, a náhodné úpravy zviditelní ještě před pushem.
- **Checkpointy a handovery** umožní komukoli, člověku i agentovi, navázat podle zaznamenaných faktů.
- **Smlouva o dokončení** znamená, že „hotovo“ vyžaduje úspěšný ověřovací příkaz, což je u tohoto webu smoke test živé verze.
- **Hooky** spouštějí `majordomus doctor` před každým commitem a `majordomus finish --check` před každým pushem. Když hook odmítne, přečtěte si nález: jmenuje soubor i pravidlo.

## Vydávání verzí

Vydání jsou automatická. Každý ověřený push do `main` vytvoří GitHub Release. Verze se odvozuje z commitů od posledního tagu: změna, která rozbíjí kompatibilitu, zvedne major verzi (dokud je projekt na 0.x, minor), `feat` zvedne minor, všechno ostatní patch.

**Proč:** časté vydávání je bezpečné jen tehdy, když je hlídané a mechanické. Zprávy commitů jsou vstupem pro verzi, a proto se kontrolují při commitu i znovu v CI.
