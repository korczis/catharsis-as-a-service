+++
title = "Paralelní agenti v jednom pracovním stromu: rozdělení práce, návrhy a commity po cestách"
description = "Jak několik AI pracovníků rozšiřovalo web současně v jediném pracovním stromu Gitu: obsahoví agenti, kteří píší jen vlastní soubory a sdílená data navrhují, hlavní sezení, které slučuje, souběžné sezení, které commituje po cestách, a co podle záznamů selhalo."
date = 2026-09-14
weight = 5

[taxonomies]
tags = ["technika", "ai agenti", "paralelní práce", "git"]

[extra]
kicker = "Technika 05"
kind = "technical"
summary = "Po pátém vydání se práce rozvětvila. Hlavní sezení vyslalo obsahové agenty psát nové výzkumné poznámky, teoretické eseje, modely a pojmy slovníku; druhé, nezávislé sezení pracovalo na tomtéž checkoutu a commitovalo své změny. Nikdo nepoužil větve. Článek popisuje konvence, díky nimž to fungovalo, od vlastnictví souborů a souborů s návrhy po jediného slučovatele a commity po explicitních cestách, a uvádí selhání, která ukazují historie Gitu, běhy pipeline a soubory."
key_points = [
  "Obsahoví agenti vlastní adresáře, nikdy sdílené soubory: stránky zapisují rovnou do svých cest, zatímco přírůstky do sdíleného registru přicházejí jako soubory s návrhy, které jeden slučovatel připojí po kontrole identifikátorů a syntaxe.",
  "Souběžné sezení commitovalo na stejném stromu jmenovitě po cestách; jeden jeho commit přidal šest tvrzení do souboru registru, který v tu chvíli obsahoval desítky dalších necommitnutých tvrzení, a žádné z nich do commitu nezahrnul.",
  "Sdílený strom je často rozpracovaný, proto pracovníci validují své změny a vykreslují v soukromé kopii; celorepozitářové validátory selhávají na nedokončených souborech jiných pracovníků.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Proč jeden strom, a ne větve

Obvyklou odpovědí na paralelní práci v Gitu jsou větve, jedna na pracovníka, slučované přes pull requesty. 14. září 2026 se web rozšiřoval jinak: několik AI pracovníků zapisovalo současně do jedné pracovní kopie `main`. Důvod byl praktický. Práce byla převážně přírůstková (nové stránky, nové záznamy v registru), pipeline vydává každý ověřený push do `main` a člověk, který práci řídil, chtěl mít rostoucí výsledek na jednom místě.

Jeden strom odstraní konflikty při slučování v gitovském smyslu a nahradí je jiným problémem: dva pracovníci mohou současně zapisovat do stejného souboru, pracovník může commitnout cizí rozpracovanou změnu a každá celorepozitářová kontrola vidí rozpracovanou práci všech. Článek popisuje, jak se to řešilo a co se pokazilo. Uvádí jen to, co ukazují záznamy: historii Gitu a trailery commitů, běhy GitHub Actions, ledger Majordomu a soubory v pracovní kopii. Totéž období na časové ose ukazuje [případová studie](../../pripadova-studie/).

## Kdo pracoval

V záznamech se objevují tři druhy pracovníků.

**Hlavní sezení.** Všechny commity od plakátu po [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) nesou stejný trailer `Claude-Session`. Toto sezení zahájilo dozorovanou úlohu, která byla v době psaní stále aktivní, zaznamenanou ve 14:54:07 UTC s cílem „Extend the site: more research and advice, per-page social previews, search and glossary cross-linking, second artifact Closure as a Service“.

**Obsahoví agenti vyslaní hlavním sezením.** V Gitu se vůbec neobjevují, protože commitovat nesměli. Jejich práce je vidět jako nové adresáře v pracovní kopii (výzkumné poznámky, teoretické eseje, stránka interaktivních modelů) a jako soubory s návrhy v soukromém odkladišti hlavního sezení, jeden adresář na agenta. I tento článek je výstupem takového agenta.

**Souběžné sezení.** Commity [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163), [93fd07f](https://github.com/korczis/catharsis-as-a-service/commit/93fd07f) a [2125f1e](https://github.com/korczis/catharsis-as-a-service/commit/2125f1e) nesou jiný trailer `Claude-Session` než commity hlavního sezení. Vznikly na tomtéž checkoutu během aktivní úlohy hlavního sezení, zatímco strom obsahoval necommitnutou práci hlavního sezení i obsahových agentů.

## Rozvětvení: zadání, které určuje vlastnictví

Obsahový agent dostane zadání a to nese pravidla souběhu. Zadání této sekce je typické. Vyjmenovává jediné soubory, které agent smí vytvořit (index sekce a jeden adresář na článek, v obou jazycích), jmenuje soubory, na které nesmí sáhnout („templates, scripts, data/*.toml, zola.toml, tests or other content; other workers … edit those“), zakazuje operace s Gitem a zapisovací příkazy Majordomu a říká, kam patří návrhy: do adresáře v odkladišti.

Pravidla se dají shrnout do jedné zásady: **agent zapisuje jen do cest, do kterých nezapisuje nikdo jiný.** Výzkumná poznámka má vlastní adresář, takže dva agenti píšící dvě poznámky se nikdy nedotknou stejného souboru. Většina rozvětvení je tak bez konfliktů už svou konstrukcí, bez jakéhokoli zamykání.

Výjimkou jsou soubory, na kterých závisí každá stránka:

- `data/references.toml`, `data/sources.toml`, `data/claims.toml`, `data/glossary.toml` a `data/evidence_changelog.toml`, protože každé podstatné tvrzení potřebuje záznam v registru ([Registr důkazů jako kód](@/engineering/evidence-ledger-as-code/index.cs.md));
- `data/commands.toml`, protože každý příkaz zmíněný v textu potřebuje položku v rejstříku;
- `zola.toml`, protože v něm žijí texty rozhraní.

## Návrhy a jediný slučovatel

Pro sdílená data píší agenti **návrhy**: soubory TOML ve stejném tvaru jako cíl, obsahující jen jejich přírůstky. Odkladiště hlavního sezení obsahuje z rozvětvení toho dne čtyři takové adresáře s názvy odpovídajícími práci (`expand`, `expand-glossary`, `expand-models`, `expand-theory`), každý s některými ze souborů `references.toml`, `sources.toml`, `claims.toml`, `glossary.toml` a `changelog.toml`.

Uplatňuje je krátký skript ve stejném odkladišti, `merge_expand.py`. Jeho docstring uvádí kontrakt:

```text
Merge agent proposal files (scratchpad/expand*/{references,sources,claims,glossary,changelog}.toml)
into <root>/data/*.toml by appending TOML text. Entries whose id already exists are skipped and reported.
```

Opakované spuštění je bezpečné díky třem detailům:

1. **Identifikátory se kontrolují před připojením.** Literatura, hodnocení, tvrzení nebo pojem, jejichž id už existuje, se přeskočí a vypíše se o tom řádek, takže dva agenti citující stejný článek nevytvoří duplicitní klíč, který by TOML odmítl.
2. **Každý blok musí projít parserem samostatně** (`tomllib.loads(block)` před zápisem), takže chybný návrh selže dřív, než se dostane do sdíleného souboru.
3. **Changelog se vkládá na začátek**, protože registr vede changelog od nejnovějšího, a po sloučení skript znovu načte všech pět datových souborů.

Sloučení připojuje text, místo aby data znovu serializovalo. Zachová tak komentáře, nadpisy sekcí a formátování ručně udržovaných souborů a diff k revizi obsahuje přesně přidané záznamy. Hlavní sezení pak nad sloučeným stromem spustí validátory a teprve tam vyjdou najevo problémy, které agent sám vidět nemohl (například id, které jiný agent použil pro jiný článek).

Tady je jediné místo, kde se práce řadí za sebou: mnoho agentů navrhuje, jedno sezení slučuje. Výsledek ukazuje changelog důkazů v pracovní kopii, například záznam o tvrzeních a třech zdrojích přidaných pro stránku interaktivních modelů.

## Souběžné sezení na stejném stromu

Souběžné sezení návrhy nepoužívalo. Pracovalo přímo ve stromu a commitovalo své změny, a commity ukazují jak: jmenovitě po cestách, ne vším, co se změnilo.

- **d2b3c47** (15:14:22 UTC) změnil pět souborů: `static/js/app.js`, `styles/app.css`, `templates/components/library.html`, `tests/site.spec.js` a `zola.toml`. V době psaní obsahují čtyři z nich (`styles/app.css`, komponenta knihovny, prohlížečové testy a `zola.toml`) další necommitnuté změny jiných pracovníků a ty součástí commitu nejsou.
- **2125f1e** (15:38:00 UTC) rozšířil výzkumnou poznámku o měření emocí a přidal osm zdrojů a šest tvrzení. Commitnutý `data/claims.toml` obsahuje 56 tvrzení, tedy 50 z v0.5.0 plus vlastních šest. Když autor tohoto článku několik minut před tímto commitem spočítal tvrzení ve sdílené pracovní kopii, soubor jich měl už 86; počítání po commitu našlo 92, tedy stejných 86 plus šest nových. Zbylých 36 záznamů zůstalo necommitnutých.

Druhý případ je těžší. Souběžné sezení commitlo část souboru, který měnili i jiní pracovníci, a výsledkem v `main` je registr konzistentní se stránkami commitnutými současně. Záznamy neříkají, jakým mechanismem Gitu byly připraveny jen tyto záznamy. Ukazují výsledek: obsah commitu odpovídá jeho zprávě.

Obě sezení běžela pod stejnými hooky: `commit-msg` kontroluje předmět a `pre-commit` spouští [`majordomus doctor`](../../commands/#majordomus-doctor). Ledger Majordomu v tomto období zaznamenává jedinou aktivní úlohu, kterou zahájilo hlavní sezení. Jednotkou dozorové vrstvy je pracovní strom a jeho úloha, ne sezení, takže commity souběžného sezení spadaly do rozsahu úlohy, kterou nezahájilo. Rozsah té úlohy uváděl všechny cesty v kořeni repozitáře, takže soubory souběžného sezení v něm ležely; při užším rozsahu by je [`majordomus check`](../../commands/#majordomus-check) nahlásil jako odchylku.

## Co se pokazilo

Záznamy z této fáze ukazují čtyři problémy. Žádný neznamenal ztracenou změnu a všechny plynou ze sdílení jednoho stromu.

**Celorepozitářové validátory selhávají na nedokončených souborech jiných pracovníků.** Když vznikal koncept tohoto článku, [`python3 scripts/validate-content.py`](../../commands/#validate-content) nad sdíleným stromem hlásil FAIL kvůli souborům, které tento agent nevlastní. Validátor překladů hlásil `content/about/index.cs.md: [extra] structure differs from en`, tedy stránku, kterou v tu chvíli upravoval jiný pracovník. Ve sdíleném stromu červený validátor pracovníkovi neříká, že je chybná *jeho* změna. Obsahoví agenti proto mají pokyn ignorovat chyby v souborech, které nevlastní, a když potřebují čisté vykreslení, postavit si soukromou kopii repozitáře.

**Commit může projít CI a přesto selhat v produkci.** d2b3c47 prošel všemi sedmi joby CI a nasadil se. V [běhu 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250) selhal jeden prohlížečový test v produkci a vydání bylo přeskočeno. Příčinu a opravu popisuje článek [Testování statického webu](@/engineering/testing-a-static-site/index.cs.md). Tady je podstatné, jak dlouho selhání zůstalo otevřené: oprava 93fd07f byla commitnuta 14 minut 28 sekund po skončení neúspěšného jobu. Mezitím živý web servíroval neověřený commit a ostatní pracovníci dál zapisovali do stromu.

**Dva commity osm sekund po sobě znamenají jeden běh pipeline.** 93fd07f a 2125f1e byly commitnuty v 15:37:52 a 15:38:00 UTC. Workflow Pages má skupinu souběhu s `cancel-in-progress: true` a seznam běhů ukazuje jediný běh, [34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153), pro poslední commit. Běh prošel a [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) vydala d2b3c47, opravu i obsahovou změnu společně. Je to správné chování, protože poznámky k vydání uvádějí všechny commity od posledního tagu. Znamená to ale také, že oprava a nesouvisející obsahová změna se ověřují, a buď vydají, nebo nevydají, společně.

**Dříve, před rozvětvením: odchylka od rozsahu.** Ráno, kdy pracovalo jediné sezení, skončily tři dozorované úlohy jako částečné, protože deklarovaný rozsah přestal odpovídat měněným souborům; viz [Dodávka s AI pod dozorem](@/engineering/supervised-ai-delivery/index.cs.md). S více pracovníky na jednom stromu byl rozsah úlohy hlavního sezení nastaven na všechny cesty v kořeni, což tato přerušení odstraní. Znamená to ale také, že dozorová vrstva už neodlišuje soubory jednoho pracovníka od souborů druhého.

## Co vydrželo a co by se muselo změnit

Konvence, které vydržely, jsou dost jednoduché na to, aby se vešly do zadání: vlastni adresář, sdílená data navrhuj, slučovat nech jedno sezení, commituj po cestách, validuj vlastní soubory, vykresluj v kopii. Do doby psaní se neztratila žádná práce a žádný commit nesmíchal změny jednoho pracovníka se změnami druhého: každý commit po rozvětvení obsahuje soubory a záznamy, které popisuje jeho zpráva, a každý prošel stejnou pipeline jako vše ostatní.

Aby to fungovalo pro víc než hrstku pracovníků, musely by se změnit dvě věci. První je připisování práce. Git ani ledger Majordomu nezaznamenávají, který obsahový agent vytvořil kterou stránku, a adresáře s návrhy, které by to ukázaly, jsou soukromé soubory v odkladišti, jež sezení nepřežijí. Druhou je izolace. Selhání sdíleného stromu popsaná výše, validátory zatížené nedokončenou prací a opravy vydávané společně s nesouvisejícími změnami, jsou přesně to, čemu mají zabránit oddělené worktrees a větve. Bootstrap soubor pro agenty v repozitáři už popisuje konvenci worktrees pro další práci. Její použití by každému pracovníkovi dalo čistý strom a vlastní běh pipeline, za cenu slučování.
