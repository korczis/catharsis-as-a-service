+++
title = "Registr důkazů jako kód: tvrzení, zdroje a data revizí jako ověřovaná data"
description = "Jak je každé veřejné tvrzení webu zapsané jako data s typem, úrovní důkazů, mírou jistoty, zdroji a datem revize; jak to vynucují validátory a týdenní workflow; a jak stránky hodnocení vykreslují z registru, místo aby ho opakovaly."
date = 2026-09-14
weight = 3

[taxonomies]
tags = ["technika", "důkazy", "validace", "datový model"]

[extra]
kicker = "Technika 03"
kind = "technical"
summary = "Odkaz, který se v Crossrefu dohledá, ukazuje, že článek existuje, ne že podporuje větu, která ho cituje, ani že je ta věta stále aktuální. Web proto drží odděleně tři soubory: bibliografii ověřovanou proti Crossrefu, hodnocení každého zdroje a registr všech podstatných tvrzení s hodnocením a daty revize. Validátor zastaví build, když je tvrzení hodnoceno výš než jeho zdroje, když je interval revize příliš dlouhý, když stránka nemá žádné zaznamenané tvrzení nebo když datum uplynulo. Stránky hodnocení vykreslují z registru."
key_points = [
  "Bibliografická fakta, redakční hodnocení a veřejná tvrzení žijí v oddělených souborech TOML, protože se mění z různých důvodů a strojově ověřit lze jen to první.",
  "Validátor kóduje pravidla: tvrzení není nikdy silnější než jeho nejlepší zdroj, tvrzení o klinických hranicích se revidují nejpozději po 180 dnech a prošlé datum zastaví build.",
  "Šablony, stránka stavu, JSON API i klient v Rustu čtou tentýž registr, takže hodnocení je zapsané jednou a nemůže si mezi stránkami odporovat.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Problém, který bibliografie neřeší

První verze knihovny citovaly zdroje obvyklým způsobem: seznam literatury na každé stránce, u každé položky DOI, a validátor, který každé DOI, název a rok porovnal s Crossrefem. To zachytí vymyšlené nebo překlepnuté odkazy. Neodpovídá to ale na otázky, které má pozorný čtenář psychologického webu:

- Podporuje citovaná studie právě tuto větu, nebo nějakou podobnou?
- Jak silná je tato opora ve srovnání s tvrzením na vedlejší stránce?
- Koho studie zkoumala a zůstává věta v mezích této populace?
- Kdy naposledy někdo ověřil, že věta stále odpovídá literatuře?

Jsou to redakční úsudky a stárnou. Záznam rozhodnutí, který registr zavedl, uvádí konkrétní příklad: metaanalýza z roku 2024 o vzrušení a hněvu změnila, jak má znít tvrzení webu o ventilování. Tvrzení, ke kterému se nikdo nevrací, se nestane viditelně chybným; prostě přestane platit. Cílem návrhu bylo toto stárnutí zviditelnit a nechat na něm build selhat.

Rozhodnutí bylo v Majordomu zaznamenáno 14. září 2026 ve 12:26 UTC a sepsáno jako [ADR-0001](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/adrs/0001-evidence-ledger-with-dated-review-for-every-public-claim.md), „Evidence ledger with dated review for every public claim“. Do repozitáře se dostalo commitem [4cbb6fb](https://github.com/korczis/catharsis-as-a-service/commit/4cbb6fb84a94734d2a79ba0e12826d81b36830af) a vydáním [v0.4.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.4.0).

## Tři soubory, tři důvody ke změně

| Soubor | Obsahuje | Mění se, když | Kontroluje |
|---|---|---|---|
| [data/references.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/references.toml) | autory, rok, název, periodikum, DOI nebo URL | se citace přidá nebo opraví | Crossref, offline i online |
| [data/sources.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/sources.toml) | design, úroveň A–E, populaci, hodnocení v obou jazycích, data revize | se zdroj znovu přečte nebo přehodnotí | validátor registru |
| [data/claims.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/claims.toml) | výrok, typ, úroveň, jistotu, zdroje, rozsah platnosti, výhradu, stránky, data revize | se změní literatura nebo formulace | validátor registru |

Čtvrtý soubor, [data/evidence_changelog.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/evidence_changelog.toml), zaznamenává změny, nejnovější nahoře. ADR vysvětluje, proč hodnocení není polem v bibliografii: to „mixes facts Crossref can verify with judgements it cannot, and a single file would change for two unrelated reasons“, tedy míchá fakta, která Crossref ověří, s úsudky, které ověřit nemůže, a jeden soubor by se měnil ze dvou nesouvisejících důvodů.

Záznam tvrzení vypadá takto (zkráceno z registru):

```toml
[[claims]]
id = "expressive-writing-coherence"
claim_type = "empirical"
evidence_level = "B"
confidence = "MODERATE"
sources = ["pennebaker-beall-1986", "pennebaker-1997"]
used_in = ["research/what-is-catharsis/index.md", "research/crying-and-sharing/index.md",
           "advice/write-to-make-sense/index.md"]
last_reviewed = 2026-09-14
review_due = 2027-09-14
```

Vynechaná pole jsou ta, která vidí čtenář: `statement`, `scope` a `caveat`, každé jako inline tabulka s hodnotami `en` a `cs`. Výhrada zde uvádí, že se účinky mezi studiemi liší, že krátkodobý distres po psaní často stoupá a že abstrakt studie z roku 1986 nebylo možné znovu ověřit. Právě ta poslední věta je pro účel registru typická. Slabé místo důkazů neskrývá; zapisuje ho hned vedle tvrzení.

## Slovník: úroveň a jistota nejsou totéž

Registr používá dvě stupnice a jejich oddělení bylo záměrné.

- **Úroveň důkazů** (A až E) popisuje design nejlepší dostupné opory. Úroveň A je vyhrazená pro syntézy kontrolovaných studií; syntézy korelačních studií se hodnotí podle designu studií, které shrnují, a proto některé metaanalýzy mají úroveň D.
- **Míra jistoty** (HIGH, MODERATE, LOW, UNKNOWN) popisuje, jak jistý si web je, že je výrok v dané formulaci a rozsahu podložený. Historické tvrzení o Aristotelovi může mít úroveň E a vysokou jistotu; laboratorní zjištění může mít úroveň B a střední jistotu, protože se studie rozcházejí.

Changelog má vlastní malý slovník: `added`, `revised`, `downgraded`, `upgraded`, `retracted` a `reviewed`. Snížení hodnocení nebo stažení tvrzení je proto viditelná datovaná událost se shrnutím v obou jazycích, ne tichá úprava čísla, a uvádí identifikátory tvrzení, kterých se týkala.

**Typy tvrzení** určují pravidla revize: `empirical`, `theoretical`, `historical`, `clinical-boundary`, `technical` a `artistic`. Vymyšlená telemetrie díla je zapsaná jako tvrzení typu `artistic`, takže registr je i místem, kde web uvádí, která jeho vlastní čísla nejsou měření.

## Co validátor vynucuje

[`python3 scripts/validate-claims.py`](../../commands/#validate-claims) má 255 řádků Pythonu jen se standardní knihovnou. Jeho hlavička vyjmenovává selhání a každé odpovídá jednomu způsobu, jak by registr mohl potichu ztratit smysl:

- neznámý slovník (úroveň, jistota, typ nebo design mimo seznamy) a chybějící překlady;
- visící identifikátory a cesty: tvrzení citující zdroj bez hodnocení nebo stránka v `used_in`, která neexistuje;
- tvrzení hodnocené silněji než jeho nejlepší zdroj;
- interval revize delší, než pravidla dovolují;
- výzkumná poznámka, teoretická esej nebo rada, kterou nepokrývá žádné tvrzení;
- jakýkoli záznam, jehož datum revize uplynulo.

Intervaly jsou data ve skriptu, ne text v dokumentu:

```python
CLAIM_INTERVALS = {
    "clinical-boundary": 180, "empirical": 365, "theoretical": 730,
    "historical": 730, "technical": 730, "artistic": 730,
}
SOURCE_INTERVALS = {"classical": 730, "book": 730, "software": 730, "record": 730}
SOURCE_INTERVAL_DEFAULT = 365
```

Poctivost zajišťují dvě rozhodnutí. Zaprvé může build selhat jen kvůli datu. ADR to uvádí jako důsledek, ne jako chybu: „moving a date requires a review, recorded in the changelog“, posunutí data vyžaduje revizi zaznamenanou v changelogu. Zadruhé lze datum podstrčit. Skript přijímá `--today` a testy toho využívají, aby ukázaly, že vlastní registr repozitáře expiruje:

```python
def test_repository_ledger_expires_without_review():
    result = run([PY, "scripts/validate-claims.py", "--today", "2031-01-01"])
    assert result.returncode == 1
    assert "(stale)" in result.stdout
```

Ostatní testy v [tests/python/test_evidence.py](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/python/test_evidence.py) postaví v dočasném adresáři minimální registr a rozbijí ho vždy jedním způsobem: tvrzení úrovně A na zdroji úrovně C musí selhat s hláškou „stronger than its best source (C)“; tvrzení o klinické hranici s ročním intervalem musí selhat s „the maximum is 180“; výzkumná poznámka bez tvrzení musí selhat. Validátor, který nikdo neviděl selhat, nic nedokládá, proto má každé pravidlo test, který ho selhat přiměje.

## Týdenní kontrola, která nečeká na push

Registr ověřovaný jen při pushi expiruje potichu, kdykoli nikdo nepushuje. [evidence-freshness.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/evidence-freshness.yml) běží každé pondělí v 6:17 UTC, nezávisle na commitech:

```yaml
- name: Claims, sources and glossary are consistent and within their review dates
  run: python3 scripts/validate-claims.py --warn-days 30 | tee claims.txt
- name: References still resolve in Crossref with matching titles and years
  if: always()
  run: python3 scripts/check-references.py --online | tee references.txt
```

Když některý krok selže, workflow otevře issue se štítkem `evidence-update`, nebo přidá komentář k otevřenému, s chybovými řádky a pokyny, které končí větou „Dates move only after a review.“ V den, kdy workflow přibylo, bylo jednou spuštěno ručně ([běh 34846806810](https://github.com/korczis/catharsis-as-a-service/actions/runs/34846806810), 38 sekund, úspěch). Totéž porovnání s Crossrefem, které provádí [`python3 scripts/check-references.py --online`](../../commands/#check-references), je zároveň jobem CI a způsobilo první selhání pipeline toho dne; viz [Testování statického webu](@/engineering/testing-a-static-site/index.cs.md).

## Stránky hodnocení vykreslují, neopakují

Pravidlo v hlavičce komponenty pro důkazy je stručné: „Pages never restate a claim's grade by hand; they render it from the ledger.“ Šablona eseje spočítá cestu obsahu stránky a vyžádá si každé tvrzení, jehož `used_in` ji uvádí:

{% raw -%}
```text
{%- set ledger = load_data(path="data/claims.toml") -%}
{%- set_global found = [] -%}
{%- for c in ledger.claims %}{% if path in c.used_in %}{% set_global found = [...found, c] %}{% endif %}{% endfor -%}
```
{%- endraw %}

Každé tvrzení se vykreslí jako karta se štítkem druhu, odznakem úrovně a odznakem jistoty, s výrokem, rozsahem platnosti a výhradou v jazyce stránky, s daty revize a tlačítkem, které otevře ohodnocené zdroje. Tlačítko je rozbalovací prvek Alpine; bez JavaScriptu zůstane panel otevřený a prohlížečový test kontroluje oba stavy. [Stránka důkazů](@/evidence/index.cs.md) uvádí celý registr a [stránka stavu](@/status/index.cs.md) při buildu spočítá počty, poslední revizi a nejbližší splatné revize. Její šablona uvádí: „Nothing here is typed by hand.“

Protože je registr datový, exportuje se. JSON API obsahuje `claims.json`, `sources.json`, `glossary.json` a `evidence_changelog.json` a crate v Rustu nezávisle na validátoru v Pythonu znovu kontroluje dva invarianty: každý zdroj má hodnocení a žádné tvrzení není hodnocené výš než jeho nejlepší zdroj. CLI umí vypsat tvrzení splatná do určitého data přes [`cargo run -p caas-cli`](../../commands/#caas-cli), a tak by jiná aplikace mohla odmítnout zobrazit zastaralé tvrzení.

## Co to stálo a co to nedělá

Ve [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) obsahoval registr 50 tvrzení, 58 ohodnocených zdrojů a 54 pojmů slovníku, vše v obou jazycích. ADR cenu uvádí otevřeně: „Every new substantive claim costs a ledger entry in both languages; content without one fails CI.“ Paralelní obsahoví agenti popsaní v článku [Paralelní agenti v jednom pracovním stromu](@/engineering/parallel-agents-one-tree/index.cs.md) dodávali své záznamy do registru (literaturu, hodnocení, tvrzení, pojmy a řádky changelogu) jako soubory s návrhy, které musely projít validací, než se jejich stránky mohly sloučit.

Validátor nedokáže posoudit, zda je hodnocení správné. Může zkontrolovat, že úroveň existuje, že nepřesahuje zdroje a že se někdo zavázal k datu revize. Zda studie větu skutečně podporuje, zůstává na recenzentovi, a projektové pravidlo [project.evidence-ledger](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/evidence-ledger.v1.md) to ve své části o ověřování uvádí. Stupnice hodnocení je hrubá a zčásti věcí úsudku. Registr nezajistí, že tvrzení webu jsou správná. Zpřístupní ale jejich sílu, rozsah a stáří kontrole a zanedbání promění v selhání buildu místo toho, aby prošlo bez povšimnutí.
