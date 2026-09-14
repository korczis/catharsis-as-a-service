+++
title = "Účtování času: co měří záznamy, co naznačuje odhad a proč je nelze přímo srovnat"
description = "Poctivé účtování času u webu, který za jeden den postavil AI agent pod dozorem: naměřené časy z Gitu, pipeline a ledgeru Majordomu, označený odhad stejného rozsahu pro lidský tým zdola nahoru a důvody, proč nejde o kontrolované srovnání."
date = 2026-09-14
weight = 7

[taxonomies]
tags = ["technika", "čas", "odhad", "dodávka softwaru"]

[extra]
kicker = "Technika 07"
kind = "technical"
summary = "Web dosáhl prvního ověřeného vydání 51 minut a 36 sekund po vytvoření repozitáře a pátého, jehož rozsah se zde odhaduje, 3 hodiny 13 minut a 4 sekundy po něm. Osm běhů pipeline zabralo 33 minut reálného času; dva selhaly a byly napraveny za 6 minut 52 sekund a za 20 minut 12 sekund. Průhledný odhad zdola nahoru klade stejný rozsah, postavený lidským týmem se stejnými kontrolami, zhruba na 345 až 730 člověkohodin. Obě čísla měří různé věci, kontrolní podmínka neexistuje a vlastní čas člověka nebyl zaznamenán. Článek uvádí obojí i s předpoklady a popisuje, co by vyžadovalo skutečné měření."
key_points = [
  "Naměřeno: repozitář vytvořen v 09:54:06 UTC; v0.1.0 v 10:45:42; v0.5.0 ve 13:07:10; v0.6.0 v 15:43:36. Od pushe k ověřenému vydání uběhlo v šesti úspěšných bězích 2 min 40 s až 5 min 03 s.",
  "Odhadnuto a jako odhad označeno: 345–730 člověkohodin pro rozsah v0.5.0, sestaveno ze čtrnácti pracovních položek s uvedenými předpoklady a 10–20 % na koordinaci.",
  "Žádný násobek zrychlení se neuvádí: uplynulý čas agenta a lidské úsilí jsou různé jednotky, laťka kvality se liší, čas lidského řízení není zaznamenán a jediný případ nemá kontrolu.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Otázka a past

Kdo slyší, že web jako tento vznikl za den, ptá se, kolik času se tím ušetřilo. Je to férová otázka a snadno se na ni odpoví špatně. Špatná odpověď vezme hodiny na hodinách, porovná je s odhadem, jak dlouho by to trvalo „týmu“, vydělí a zveřejní poměr. Takový poměr srovnává měření s názorem, míchá uplynulý čas s úsilím a přehlíží, že oba produkty nemusí být stejně dobré.

Tento článek odděluje tři věci a drží je odděleně:

1. **Měření** ze záznamů: historie Gitu, API GitHubu (repozitář, vydání, běhy workflow a jejich joby) a ledger Majordomu. Každé číslo je propojené se zdrojem nebo reprodukovatelné.
2. **Odhad**, výslovně označený, úsilí, které by stejný rozsah stál lidský tým, sestavený zdola nahoru tak, aby šlo každý předpoklad zpochybnit řádek po řádku.
3. **Důvody, proč obojí nelze spojit** do jednoho násobku, a co by vyžadovalo skutečné měření.

Výzkumná poznámka [Metoda: stavba artefaktu podloženého důkazy s Majordomem](@/research/method-majordomus/index.cs.md) podrobně popisuje první vydání a [případová studie](../../pripadova-studie/) interaktivně ukazuje celou časovou osu. Tento článek pokrývá celý den tak, jak byl zaznamenán k 15:47 UTC.

## Část A: co měří záznamy

### Milníky

Všechny časy jsou v UTC ze 14. září 2026.

| Čas | Událost | Zdroj |
|---|---|---|
| 09:45 | Začátek pracovního sezení (přestavba plakátu) | časová razítka lokálních souborů podle metodické poznámky; nezávisle neověřitelné |
| 09:54:06 | Vytvořen repozitář na GitHubu | API GitHubu, `created_at` |
| 10:26:23 | Inicializace Majordomu; první dozorovaná úloha | ledger Majordomu |
| 10:45:42 | [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0): dvojjazyčný web, CI/CD, živé ověření | seznam vydání |
| 11:13:28 | [v0.2.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.2.0): postupy HTML5 Boilerplate, náhledy, strukturovaná data | seznam vydání |
| 12:24:28 | [v0.3.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.3.0): výzkumná knihovna, rady, rejstřík příkazů, API pro Rust | seznam vydání |
| 12:58:21 | [v0.4.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.4.0): registr důkazů, metody, slovník, stav | seznam vydání |
| 13:07:10 | [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0): registr v API, klient v Rustu, dokumentace | seznam vydání |
| 13:08:34 | Úloha uzavřena jako dokončená; do 14:54:07 není zaznamenána žádná dozorovaná úloha | ledger Majordomu |
| 15:43:36 | [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0): náhledy obrazovek, oprava, rozšířená výzkumná poznámka | seznam vydání |

Odvozené doby:

- od vytvoření repozitáře k prvnímu ověřenému vydání: **51 min 36 s**;
- od vytvoření repozitáře k v0.5.0: **3 h 13 min 04 s**;
- od vytvoření repozitáře k v0.6.0: **5 h 49 min 30 s**, přičemž toto okno zahrnuje 1 h 45 min 33 s bez zaznamenané dozorované úlohy.

Do tohoto okna spadá deset commitů, šest vydání, čtyři zaznamenaná rozhodnutí a jeden navržený ADR.

### Čas dozorovaných úloh

Ledger Majordomu, který vypíše [`majordomus history`](../../commands/#majordomus-history), zaznamenává začátek a konec každé úlohy. Do v0.5.0 připadá na pět úloh **2 h 38 min 38 s**. Tři úlohy, které skončily jako částečné a byly restartovány (chyby rozsahu popsané v článku [Dodávka s AI pod dozorem](@/engineering/supervised-ai-delivery/index.cs.md)), z toho tvoří 32 min 29 s. Čas úloh je doba, kdy agent pracoval pod deklarovanou úlohou. Neukazuje, kolik z ní strávil člověk čtením, rozhodováním nebo psaním.

### Běhy pipeline

Každý push do `main` spustí workflow Pages. Tabulka uvádí všechny běhy toho dne: reálný čas od vytvoření do dokončení, součet trvání jobů, které běžely (joby běží paralelně, proto je součet vyšší), a dobu od vytvoření běhu po publikované vydání. Data vypíše [`gh run list`](../../commands/#gh-run-list).

| Běh | Commit | Výsledek | Reálný čas | Čas jobů | Od pushe k vydání |
|---|---|---|---|---|---|
| [34834554169](https://github.com/korczis/catharsis-as-a-service/actions/runs/34834554169) | 9bc6897 | úspěch | 2:43 | 3:02 | 2:40 (v0.1.0) |
| [34836842423](https://github.com/korczis/catharsis-as-a-service/actions/runs/34836842423) | 54a31a2 | úspěch | 3:06 | 3:24 | 3:02 (v0.2.0) |
| [34842607207](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842607207) | 51dde0b | selhání: literatura | 1:29 | 3:03 | žádné |
| [34842946706](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842946706) | 94d734c | úspěch | 3:25 | 4:57 | 3:21 (v0.3.0) |
| [34845982889](https://github.com/korczis/catharsis-as-a-service/actions/runs/34845982889) | 4cbb6fb | úspěch | 4:17 | 6:01 | 4:14 (v0.4.0) |
| [34846771284](https://github.com/korczis/catharsis-as-a-service/actions/runs/34846771284) | f2890f4 | úspěch | 5:02 | 6:46 | 4:59 (v0.5.0) |
| [34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250) | d2b3c47 | selhání: ověření produkce | 8:01 | 8:44 | žádné |
| [34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153) | 2125f1e | úspěch | 5:07 | 6:15 | 5:03 (v0.6.0) |
| **Celkem** | | 6 úspěšných, 2 neúspěšné | **33:10** | **42:12** | |

Pipeline narostla ze sedmi jobů na deset, když s výzkumnou knihovnou přibyly joby pro Python, Rust a Crossref, a prohlížečová sada narostla z 30 na 85 testů, proto jsou pozdější běhy delší. Týdenní workflow důkazů bylo navíc jednou spuštěno ručně (38 sekund).

### Selhání a náprava

| Selhání | Zjištěno | Oprava commitnuta | Ověřené vydání | Od zjištění k vydání |
|---|---|---|---|---|
| Porovnání názvu s Crossrefem ([podrobnosti](@/engineering/testing-a-static-site/index.cs.md)) | 12:17:36 | 12:20:54 | 12:24:28 (v0.3.0) | 6 min 52 s |
| Test kliknutí s modifikátorem v produkci | 15:23:24 | 15:37:52 | 15:43:36 (v0.6.0) | 20 min 12 s |

Ani jedno selhání se nedostalo do vydání. Druhé nechalo na živém webu zhruba dvacet minut neověřený commit, protože produkci lze testovat až po nasazení.

### Co měření nezahrnují

- Plánování, přemýšlení a psaní zadání před prvním zaznamenaným souborem.
- Čas člověka. Žádný záznam neukazuje, kdy člověk četl, rozhodoval nebo byl pryč; jedinou mezí je samotné okno.
- Čas po přečtení záznamů: položky k revizi, které předávka z v0.5.0 ponechává otevřené (přijetí ADR-0001, revize označených českých pojmů ve slovníku), a případné přepracování, které vyvolají.
- Využití modelů a jeho cenu, které nejsou součástí záznamů repozitáře.

## Část B: odhad pro lidský tým

**Tato část je odhad, ne měření.** Ptá se, kolik člověkohodin by zkušený tým (webový vývojář, technický autor s psychologickým vzděláním, český redaktor a na částečný úvazek DevOps a vývojář v Rustu) potřeboval na rozsah [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) se stejnými automatickými kontrolami, pokud začne s hotovým plakátem. Použita je v0.5.0, protože její rozsah lze změřit z otagovaného stromu a uzavírala dozorovanou úlohu; pozdější práce je vyloučena na obou stranách.

Sloupec rozsahu je naměřen z repozitáře v commitu [f2890f4](https://github.com/korczis/catharsis-as-a-service/commit/f2890f4fa20f0f92db790477b1460c2e774bbe44). Počty slov nezahrnují front matter. Rozpětí hodin jsou úsudkem autora a předpoklady uvádějí, odkud se berou. Čtenář, který nesouhlasí s tempem, může řádek přepočítat.

| # | Pracovní položka | Rozsah ve v0.5.0 (naměřeno) | Předpoklad za rozpětím | Min. (h) | Max. (h) |
|---|---|---|---|---|---|
| 1 | Anglický obsah s přečtenými zdroji | 32 anglických souborů, asi 19 300 slov; 10 výzkumných poznámek, 10 rad | 150–300 slov za hodinu včetně čtení abstraktů a kontroly formulací proti zdrojům | 65 | 130 |
| 2 | Česká verze | 32 českých souborů, asi 17 100 slov | 250–375 slov za hodinu při profesionální adaptaci s psychologickou terminologií | 45 | 70 |
| 3 | Hodnocení zdrojů | 58 zdrojů, každý s dvojjazyčným hodnocením | 0,5–1 h na zdroj: najít abstrakt, určit design, napsat oba jazyky | 29 | 58 |
| 4 | Registr tvrzení | 50 tvrzení s rozsahem, výhradou a daty ve dvou jazycích | 15–30 min na tvrzení, když jsou zdroje ohodnocené | 13 | 25 |
| 5 | Slovník | 54 dvojjazyčných pojmů s křížovými odkazy | 9–18 min na pojem | 8 | 16 |
| 6 | Designový systém, šablony a komponenty | 2 053 řádků šablon, 2 472 řádků CSS, dva jazyky | zkušený front-end vývojář zhruba 50–100 hotových řádků za hodinu včetně responzivity a přístupnosti | 40 | 80 |
| 7 | Interakce | integrace Alpine a Flowbite, 381 řádků JavaScriptu webu, varianty bez JS | málo kódu, vysoké náklady na testy a přístupnost | 12 | 24 |
| 8 | Metadata a SEO | JSON-LD, lokalizované náhledy, feedy, jazykové alternativy v sitemapě | známé vzory, ověření pro každý jazyk | 8 | 16 |
| 9 | Validátory a exportér API | 1 601 řádků Pythonu a shellu v adresáři skriptů | 35–65 řádků za hodinu u testovaných nástrojů | 24 | 48 |
| 10 | Testovací sady | 40 testů pytest s testovacími daty; 23 bloků Playwright se 72 spuštěnými testy | převažují testovací data a nestabilita prohlížečů | 24 | 48 |
| 11 | Crate v Rustu a CLI | 1 182 řádků, 21 testů | typovaný kontrakt, CLI a testy kontraktu | 16 | 32 |
| 12 | CI/CD a nastavení repozitáře | tři workflow a složená akce (352 řádků), skript vydání, rulesety, Pages | včetně ladění živého nasazení | 12 | 24 |
| 13 | Dozorová vrstva, pravidla, ADR, dokumentace | 6 projektových pravidel, 1 ADR, 5 dokumentů, README | psaní a zapojení, ne vývoj nástroje | 10 | 20 |
| 14 | Produkční pipeline díla | skript vykreslení plakátu, sada ikon, lokalizované náhledové karty | bez uměleckého konceptu | 8 | 16 |
| | **Mezisoučet** | | | **314** | **607** |
| | Koordinace, revize a integrace | | 10–20 % mezisoučtu pro tým čtyř až pěti lidí | 31 | 121 |
| | **Odhad celkem** | | | **≈ 345** | **≈ 730** |

Při 40 hodinách týdně to je zhruba 9 až 18 člověkotýdnů. Rozpětí je široké záměrně. Největší položky, obsah a hodnocení zdrojů, závisejí na tom, jak pečlivě se zdroje čtou, a právě tam by lidský odborník mohl vytvořit jiný a možná lepší produkt.

Několik úsudků táhne odhad opačnými směry:

- **Dolů:** zkušený tým s opakovaně použitelným startovním projektem pro Zolu, hotovou knihovnou validátorů nebo překladovou pamětí by byl rychlejší v řádcích 6, 8, 9 a 2. Některé položky by bez agenta, který je udělá levně, možná vůbec nevznikly (test kontraktu v druhém jazyce, spouštěný rejstřík příkazů), a tým by je oprávněně vynechal.
- **Nahoru:** rozpětí předpokládají málo přepracování. Vlastní záznamy agenta přepracování ukazují (tři restarty úloh, dvě selhání pipeline, nestabilní test tisku) a lidský tým by měl své vlastní. Dvojjazyčné revizní cykly, zpětná vazba zadavatele a čekání mezi lidmi v tabulce nejsou.

## Část C: proč tato čísla nelze dělit

Je lákavé postavit 3 h 13 min proti 345–730 člověkohodinám a uvést násobek. Tento článek to nedělá, a to z pěti důvodů.

**1. Různé jednotky.** Uplynulý čas je reálný čas, během kterého pracoval agent, někdy i několik agentů najednou, zatímco člověk řídil a kontroloval. Člověkohodiny jsou úsilí sečtené přes lidi. Paralelní lidská práce by zkrátila kalendářní dobu odhadu beze změny hodin a paralelní agenti dělají s měřením totéž.

**2. Žádná kontrolní podmínka.** Existoval jeden projekt, postavený jednou. Není lidský tým, který by postavil stejný rozsah, není druhé sezení agenta bez dozoru a není opakování. Jediný případ může ukázat, že něco je možné. Neukáže, jak velký je účinek.

**3. Laťka kvality není prokazatelně stejná.** Odhad předpokládá, že lidský tým splní stejné automatické kontroly, a automatické kontroly nejsou celá kvalita. Registr uvádí, že designy zdrojů byly ověřeny podle publikovaných abstraktů a že dva zdroje bez dostupného abstraktu jsou označené jako neověřené. Lidský odborník, který čte plné texty, by potřeboval víc času a mohl by hodnotit jinak. Revize české terminologie a přijetí ADR jsou stále otevřené. Kde je produkt agenta slabší, srovnání mu lichotí; kde je důkladnější, než by se tým obtěžoval být (každý příkaz spuštěný v testu), srovnání ho znevýhodňuje.

**4. Čas lidského řízení není zaznamenán.** Člověk psal zadání, rozšiřoval rozsah, volil mezi možnostmi a kontroloval výstup. Nic z toho není změřené. Pokud byl člověk přítomen celé okno, je jeho úsilí oknem shora omezené; pokud ne, je menší. V každém případě do srovnání patří a chybí v něm.

**5. Odhadce není nezávislý.** Odhad sepsal zpětně AI agent téhož druhu, jako byl ten, který práci odvedl, a znal výsledek. Ukotvení na známém výsledku je věrohodné zkreslení oběma směry. Počty řádků a slov jsou navíc slabou náhražkou úsilí: sedmnáctiřádkový skript na přibalení knihoven a validátor o 255 řádcích nestojí úměrně své délce.

Záznamy podporují užší tvrzení. Rozsah v0.5.0, naměřený výše, dosáhl ověřeného vydání asi tři hodiny po vytvoření repozitáře. Každé vydání v tomto okně prošlo stejnými automatickými kontrolami a obě selhání tyto kontroly zachytily a byla napravena během minut. Při jakémkoli rozumném čtení tabulky odhadu jde o velký rozdíl v uplynulém čase. Jak velký, v podobě, která by obstála před kritikou, jediný nekontrolovaný případ říct nemůže.

## Co by vyžadovalo skutečné měření

Obhajitelné srovnání dodávky s AI pod dozorem a běžné dodávky by potřebovalo přinejmenším:

1. **Pevný, předem zaregistrovaný rozsah a bránu přijetí.** Stejné zadání a stejný validační skript a testovací sadu jako definici hotového, dohodnuté před začátkem práce.
2. **Srovnávací větve.** Lidský tým, agenta řízeného člověkem bez dozorových nástrojů a agenta s dozorem, ideálně na několika projektech různého druhu a s přidělením tak, aby tentýž člověk neřídil dvě větve stejného projektu.
3. **Úsilí, ne jen uplynulý čas.** Měření lidské pozornosti (řízení, revize, čekání) ve všech větvích a vedle toho výpočetní čas a náklady agentů.
4. **Zaslepené hodnocení kvality.** Nezávislí odborníci hodnotící vzorky obsahu (přesnost tvrzení vůči zdrojům, přiměřenost hodnocení, kvalitu češtiny), aniž by věděli, která větev je vytvořila, a k tomu audit přístupnosti.
5. **Výsledky po vydání.** Chyby nalezené v týdnech po vydání, zmeškaná data revizí a náklady první podstatné změny, protože udržovatelnost je místem, kde uspěchaná práce obvykle vystaví účet.

Do té doby je poctivým shrnutím dvojice čísel s jejich označením: naměřené tři hodiny a třináct minut k ověřené v0.5.0 a odhadovaných 345 až 730 člověkohodin, které by stejný rozsah stál lidský tým. Nejde o čísla téhož druhu.
