+++
title = "Dodávka s AI pod dozorem: zadání, úlohy s rozsahem, hooky, CI a živé ověření"
description = "Jak jeden člověk řídil AI agenta pro programování pod dozorem Majordomu: druhy zadání, úlohy s vymezeným rozsahem, hooky pro commit a push, pipeline, živé ověření a vydání a ze záznamů doložené rozdělení práce."
date = 2026-09-14
weight = 2

[taxonomies]
tags = ["technika", "majordomus", "ai agenti", "dodávka softwaru"]

[extra]
kicker = "Technika 02"
kind = "technical"
summary = "Web napsal AI agent pro programování. Člověk, který ho řídil, nepsal kód; stanovoval cíle, rozšiřoval rozsah, vybíral z nabídnutých možností a ponechal si právo přijímat rozhodnutí. Mezi agentem a repozitářem stál Majordomus: každá změna běžela jako úloha s vymezeným rozsahem, commity a pushe procházely hooky a úlohu šlo uzavřít jako dokončenou, jen když uspěl ověřovací příkaz proti živému webu. Článek tuto smyčku rekonstruuje ze záznamů."
key_points = [
  "Ze 14. září 2026 je zaznamenáno šest dozorovaných úloh; tři skončily jako částečné a byly restartovány, dvě jako dokončené a jedna byla v době psaní stále aktivní.",
  "Hooky spouštějí kontrolu zdraví při každém commitu a smlouvu o dokončení při každém pushi; pipeline kontrolu dozoru zopakuje v CI dřív, než se cokoli nasadí.",
  "Člověk určoval rozsah a přijímal rozhodnutí; agent implementoval, testoval, zaznamenával rozhodnutí a navrhl záznam architektonického rozhodnutí, který stále čeká na lidské přijetí.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Co tento článek tvrdí a co ne

Tento web vytvořil AI agent pro programování (Claude Code) řízený jedním člověkem, s [Majordomem](https://majordomus.dev) jako dozorovou vrstvou. Tu větu lze číst dvojím způsobem. Podle prvního „web postavila AI“, což zakrývá práci člověka i omezení, díky nimž byl výsledek použitelný. Podle druhého „AI jen psala na klávesnici“, což zakrývá, jak velkou část návrhu udělal agent. Záznamy nepodporují ani jedno. Článek popisuje smyčku, která skutečně proběhla, a jako zdroje používá historii Gitu, ledger Majordomu a běhy GitHub Actions.

[Případová studie](../../pripadova-studie/) ukazuje tytéž záznamy jako interaktivní časovou osu. Výzkumná poznámka [Metoda: stavba artefaktu podloženého důkazy s Majordomem](@/research/method-majordomus/index.cs.md) podrobně popisuje první vydání. Tady jde o mechanismus: jak se ze zadání stane ověřené vydání a kde stojí jednotlivé pojistky.

## Zadání: od jednořádkové žádosti k bráně dokončení

Metodická poznámka třídí zprávy člověka v prvních fázích do pěti druhů: jednořádková žádost o založení projektu; výtvarné vedení plakátu s volbou mezi nabídnutými přístupy; tři strukturovaná prováděcí zadání rostoucího rozsahu; krátké pokyny během práce („nasaď“, „ověř v prohlížeči“, „vydávej automaticky“, „použij Majordomus a vynucuj ho“); a redakční vedení, například nahrazení propagačních textů psychologií podloženou zdroji.

Nejzajímavější jsou prováděcí zadání. Neurčovala šablony ani testovací případy. Určovala výsledky, omezení a především **co se počítá jako hotové**: číslované požadavky a výslovnou bránu dokončení. Pro agenta je tato forma důležitá, protože jinak ohlásí dokončení ve chvíli, kdy je kód napsaný. Brána typu „nasazeno, ověřeno proti živé URL, vydáno“ mění dokončení v něco, co může zkontrolovat stroj.

Rozsah se během práce měnil a záznamy to uvádějí. Checkpoint zapsaný v 11:09 UTC poznamenává: „User scope expanded mid-task: landing explainer of catharsis, research essays with citations, advice library, tags, illustrations, per-page previews, Majordomus method page with real timeline, Rust integration, command registry with links and test coverage, pytest, JS coverage, docs.“ Agent na rozšíření nereagoval tak, že by ho vstřebal do běžící úlohy; úlohu uzavřel, zapsal předávku a zahájil novou, jejíž rozsah pokrýval nové cesty.

## Úlohy s vymezeným rozsahem

Každá změna běžela jako úloha Majordomu zahájená příkazem [`majordomus start`](../../commands/#majordomus-start) se seznamem cest, na které smí práce sáhnout. Ledger, který vypíše [`majordomus history`](../../commands/#majordomus-history), zaznamenává ze 14. září 2026 šest úloh:

| Úloha | Start (UTC) | Konec (UTC) | Výsledek | Proč skončila |
|---|---|---|---|---|
| Web s CI/CD | 10:26:23 | 10:29:16 | částečný | soubory přesunuty mimo deklarovaný rozsah; restart |
| Web (rozsah `.`) | 10:29:16 | 10:39:39 | částečný | `.` nebyla chápána jako celý repozitář; restart |
| Web | 10:39:39 | 10:47:25 | dokončeno | v0.1.0 nasazena, ověřena a vydána |
| Boilerplate, náhledy, strukturovaná data | 10:50:57 | 11:10:10 | částečný | plánované nové cesty v kořeni; restart s širším rozsahem |
| Knihovna podložená důkazy, Rust, rejstřík | 11:10:11 | 13:08:34 | dokončeno | v0.5.0 nasazena, ověřena a vydána |
| Rozšíření webu | 14:54:07 | — | aktivní | v době psaní otevřená |

Tři úlohy ze šesti skončily jako částečné, a každá ze stejného důvodu: deklarovaný rozsah přestal odpovídat práci. Tak to má být. [`majordomus watch`](../../commands/#majordomus-watch) a [`majordomus check`](../../commands/#majordomus-check) hlásí odchylku mezi úlohou a změněnými soubory; předávka zapsaná v 10:29 UTC problém popisuje přímo („The first task scope omitted the pre-existing root files that were moved into artwork/ and static/ … so watch reports scope drift“) a uvádí i další krok („Restart the task with a scope covering the whole repository“).

Jedna výhrada ke zdrojům. Ledger Majordomu, checkpointy, předávky a záznam rozhodnutí leží v `.ai/local/`, který se podle pravidel nikdy necommituje. Citace z nich pocházejí z pracovní kopie, na které web vznikal; veřejné a nezávisle ověřitelné záznamy jsou historie Gitu, běhy Actions a vydání, na které článek odkazuje.

Restart je levný, protože stav je uložený mimo agenta. Před uzavřením úlohy agent zapíše předávku příkazem [`majordomus handover`](../../commands/#majordomus-handover) se třemi povinnými nadpisy: Objective, Current State a Next Action. Průběžné poznámky jdou přes [`majordomus checkpoint`](../../commands/#majordomus-checkpoint). Další úloha začíná z těchto záznamů, ne z toho, co si agent pamatuje z konverzace, a proto restart trvá sekundy. Tři částečné úlohy stály 2 minuty 53 sekund, 10 minut 23 sekund a 19 minut 13 sekund zaznamenaného času úloh a žádná z nich nic nepushnula.

## Rozhodnutí jsou záznamy, ne chat

Volby s trvalými důsledky se zaznamenávaly příkazem [`majordomus decision`](../../commands/#majordomus-decision). Ledger z toho dne obsahuje čtyři rozhodnutí: strukturovaná data se staví jako data Tery a serializují přes `json_encode`; náhledy odkazů jsou lokalizované pro každý jazyk a sitemap uvádí všechny jazykové verze; validátory v Pythonu se testují přes pytest v projektovém virtuálním prostředí; a návrh registru důkazů. Každý záznam rozhodnutí má stejná pole:

```text
Why: Hand-written JSON-LD inside HTML templates gets HTML-escaped and breaks on quotes;
     building the graph as template maps keeps escaping correct by construction
Rejected: hand-written JSON-LD strings; a client-side script injecting JSON-LD
Evidence: templates/partials/structured-data.html; scripts/validate-html.py parses every JSON-LD block
```

Největší rozhodnutí se stalo záznamem architektonického rozhodnutí [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md), „Evidence ledger with dated review for every public claim“. Jeho stav je `proposed`. Předávka zapsaná při vydání v0.5.0 uvádí přijetí jako první další krok pro člověka: „Accept or amend ADR-0001.“ Agent může architekturu navrhnout; přijmout ji je na člověku.

## Hooky: kontroly, na které nikdo nemusí myslet

V `.githooks/` jsou tři hooky Gitu a [`npm ci`](../../commands/#npm-ci) na ně Git nasměruje přes skript `prepare` v `package.json`:

- **commit-msg** spustí nad zprávou [`scripts/lint-commits.sh`](../../commands/#lint-commits). Conventional Commits tu nejsou stylová preference: počítá se z nich verze vydání.
- **pre-commit** vyžaduje Majordomus a spustí jeho kontrolu zdraví:

```sh
majordomus doctor || exit $?
```

- **pre-push** spustí smlouvu o dokončení v kontrolním režimu, takže push je odmítnut, dokud by aktivní úloha nesměla skončit:

```sh
majordomus finish --check || exit $?
```

[`majordomus doctor`](../../commands/#majordomus-doctor) si své místo zasloužil ještě před prvním commitem: nahlásil, že README neodkazuje na bootstrap soubor pro agenty, a chyba byla opravena lokálně. [`majordomus finish`](../../commands/#majordomus-finish) je smlouva, díky které má „dokončeno“ obsah. Úloha, která vydala v0.1.0, byla uzavřena se smoke testem živé verze jako ověřovacím příkazem; výsledek smlouvy v ledgeru uvádí každé vyhodnocené pravidlo (`scope-integrity: pass`, `blocker-resolution: pass` a další).

Hooky lze lokálně obejít, a proto kontrolu opakuje CI. Job `Majordomus supervision` nainstaluje zafixované vydání Majordomu, instalátor ověří jeho SHA-256, a spustí kontrolu zdraví nad pushnutým stromem. Ruleset repozitáře uvádí tento job spolu s kontrolou commitů, validací a end-to-end testy jako povinné kontroly pro `main`. Ruleset ale dovoluje administrátorovi repozitáře ho obejít a checkpoint po prvním pushi zaznamenává, že obejití bylo použito: přímé pushe do `main` jsou způsob, jak tato pipeline začíná. Ochrana, která na rulesetu nezávisí, je pořadí samotné pipeline, která nenasadí commit, jehož CI selhalo.

## CI, nasazení a živé ověření

Pipeline popisuje článek [Jak web vznikl](@/engineering/how-the-site-was-built/index.cs.md); pro dozor je podstatné její pořadí. `pages.yml` spustí CI, pak nasadí přesně ten artefakt, který CI ověřilo, pak ověří produkci a nakonec vydá. Projektové pravidlo [project.verified-deployment](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/verified-deployment.v1.md) stanoví měřítko pro hlášení: „A deployment is complete only when the Pages workflow's verify job has passed against the live URL returned by GitHub, and a release is cut only after that job.“

Je to pravidlo stejně pro hlášení agenta jako pro pipeline. Agent, který vidí zelený build a řekne „nasazeno“, se mýlí způsobem, který se snadno přehlédne. Tady agent sledoval běh přes [`gh run list`](../../commands/#gh-run-list) a checkpoint zapsaný po prvním pushi uvádí, na co čekal: „Pages run 34834554169 triggered (ci -> deploy -> verify -> release); watching it now.“ Dalšími kroky bylo prošetřit případný neúspěšný job, spustit smoke test a prohlížečové testy proti živé URL, potvrdit tag vydání a teprve pak uzavřít úlohu s živým ověřovacím příkazem.

Záznamy ukazují, že pravidlo platilo i při selhání. [Běh 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250) pro commit [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163) prošel všemi sedmi joby CI a nasadil web, ale jeden z 84 prohlížečových testů v produkci selhal. Job `Release` byl přeskočen a podle pravidla výše se commit nepočítal jako nasazený. Vydán byl až ve [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) v 15:43:36 UTC, poté co oprava prošla ověřením v [běhu 34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153).

## Vydání

Vydání je poslední job a nemá žádný ruční krok. [scripts/release.sh](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/release.sh) najde poslední tag `v*`, přečte předměty commitů od té doby, u `feat` zvýší minor verzi, jinak patch (zpětně nekompatibilní změny zvyšují minor, dokud je verze 0.x), a publikuje poznámky s živou URL a odkazem na běh pipeline. Tagy chrání ruleset, který zakazuje jejich mazání, přesouvání i úpravu, a do `main` nelze pushovat s přepsáním historie. Do doby psaní vyšlo 14. září 2026 šest vydání, od [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0) v 10:45:42 UTC po [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) v 15:43:36 UTC.

## Kdo co dělal

Připsat práci v sezení člověka s agentem je snadné udělat špatně, proto se tento výčet drží toho, co ukazují záznamy.

**Člověk** určil směr a hranice: samotný projekt, výtvarné vedení, zadání a jejich brány dokončení, rozšíření rozsahu během úloh zaznamenaná v checkpointech, pokyn učinit dozor povinným a redakční standardy pro psychologii. Člověku patří rozhodnutí, která předávka ponechává otevřená: přijetí ADR-0001 a revize českých pojmů ve slovníku, které agent označil za nestandardní. Čas, který člověk strávil čtením, přemýšlením a kontrolou, nikde zaznamenaný není, což je podstatné pro [Účtování času](@/engineering/time-accounting/index.cs.md).

**Agent** napsal kód, šablony, koncepty obsahu v obou jazycích, validátory, testy, workflow a dokumentaci; zvolil implementaci (komponenty Tera, schéma registru, strategii testování); nastavil rulesety repozitáře; spouštěl všechny příkazy; zapisoval checkpointy, předávky a rozhodnutí; a navrhl ADR. Commity nesou trailer `Co-Authored-By` s názvem modelu a trailer `Claude-Session` s identifikací sezení.

**Majordomus** nenapsal nic. Odmítal, zaznamenával a hlásil: odchylku od rozsahu, chybně zadaný rozsah, chybějící odkaz na bootstrap a smlouvu o dokončení. **Pipeline** toho dne odmítla dvakrát: jednou před nasazením (neshoda názvu zdroje s Crossrefem) a jednou před vydáním (selhání testu v produkci).

## Co z toho vyvodit nelze

Záznamy ukazují posloupnost kontrolovaných kroků, ne to, že dozor práci zrychlil nebo zlepšil oproti sezení bez dozoru. Druhé sezení ke srovnání neexistuje. Agent také udělal chyby, které dozorová vrstva nezachytila a pipeline ano; uvádí je článek [Testování statického webu](@/engineering/testing-a-static-site/index.cs.md). Záznamy podporují užší, ale stále užitečné tvrzení: každé „hotovo“ v tomto repozitáři je spojené s příkazem, návratovým kódem a časovým razítkem, které si čtenář může ověřit.
