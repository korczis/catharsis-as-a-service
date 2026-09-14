+++
title = "Jak web vznikl: Zola, komponenty Tera, Tailwind a obsahové API"
description = "Architektura dvojjazyčné statické publikace a její build pipeline od začátku do konce: na vstupu Markdown a TOML, na výstupu ověřené HTML a verzované JSON API, nasazené až po kontrole živé URL."
date = 2026-09-14
weight = 1

[taxonomies]
tags = ["technika", "architektura", "zola", "build pipeline"]

[extra]
kicker = "Technika 01"
kind = "technical"
summary = "Web generuje Zola 0.23.6 ze stránek v Markdownu a dat v TOML, styluje ho Tailwind CSS 4, interakci doplňují Alpine.js a Flowbite a knihovna se exportuje jako verzované JSON API, které čte crate v Rustu. Článek prochází jednotlivé vrstvy, důvody jejich volby a pipeline, která z commitu udělá ověřené vydání."
key_points = [
  "Obsah, data, texty rozhraní a šablony jsou oddělené: nový článek je dvojice souborů v Markdownu, ne úprava šablony, a všechny jazyky sdílejí tytéž šablony.",
  "Build má jeden vstupní bod s dvanácti seřazenými kroky; tentýž skript běží lokálně, v CI i před každým nasazením.",
  "Vydání vznikne až poté, co je nasazený web stažen z jeho skutečné URL, projde smoke testem a prohlížečovou sadou testů.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Co musí build dodat

Catharsis as a Service™ je dvojí věc zároveň: umělecké dílo (plakát a fiktivní „endpoint pro přechod emočního stavu“) a dvojjazyčná knihovna důkazů o katarzi. Knihovna předkládá širokému publiku psychologická tvrzení, a technika proto měla od začátku čtyři požadavky:

1. **Každá stránka anglicky i česky**, se shodnou strukturou, aby žádná jazyková verze nemohla nepozorovaně zaostat.
2. **Každé tvrzení dohledatelné** k datovanému a ohodnocenému záznamu v registru a ke zdrojům ověřeným v Crossrefu.
3. **Čitelnost bez JavaScriptu**, rychlost na telefonu a správné chování pod podcestou repozitáře, kterou servíruje GitHub Pages (`/catharsis-as-a-service/`).
4. **Nic není hotové, dokud to není živé**: nasazení je dokončené až po otestování produkční URL.

Vše vzniklo 14. září 2026 během jednoho pracovního sezení; práci odvedl AI agent pro programování řízený jedním člověkem. Časovou osu ukazuje [případová studie](../../pripadova-studie/), způsob řízení práce popisuje článek [Dodávka s AI pod dozorem](@/engineering/supervised-ai-delivery/index.cs.md). Tento článek se věnuje výsledku.

## Rozvržení zdrojů: obsah, data a texty

Repozitář odděluje čtyři druhy zdrojů a každý má jediné místo:

| Oblast | Kde je | Kdo ji čte |
|---|---|---|
| Stránky a bloky úvodní stránky | `content/**/index.md` a `index.cs.md` | Zola |
| Strukturované záznamy | `data/*.toml`: literatura, hodnocení zdrojů, tvrzení, slovník, rejstřík příkazů | šablony Zoly, validátory, exportér API |
| Texty rozhraní | `[translations]` v [zola.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/zola.toml) | `trans()` v šablonách |
| Prezentace | `templates/` a [styles/app.css](https://github.com/korczis/catharsis-as-a-service/blob/main/styles/app.css) | Zola, Tailwind |

Pravidlo za tímto rozdělením je v repozitáři zapsané jako [project.zola-source-of-truth](https://github.com/korczis/catharsis-as-a-service/blob/main/.ai/repo/rules/project/zola-source-of-truth.v1.md): „the next artifact must be a Markdown file pair, not a template edit“, tedy další artefakt má být dvojice souborů v Markdownu, nikoli úprava šablony. Šablony se nikdy nevětví podle jazyka; volají `trans(key=…, lang=lang)` a validátor překladů zastaví build, když klíč existuje jen v jednom slovníku nebo když mají dvě jazykové verze stránky odlišný tvar front matter.

Datové soubory jsou část, kterou většina statických webů nemá. Výzkumná poznámka cituje identifikátory z registru, například `kjaervik-bushman-2024`; bibliografický záznam, jeho hodnocení a tvrzení, která se o něj opírají, žijí v `data/`. Šablona identifikátory rozloží při buildu:

{% raw -%}
```text
{%- set registry = load_data(path="data/references.toml") -%}
...
{%- set ref = registry.references[id] %}
```
{%- endraw %}

Když bibliografická fakta leží v datech, a ne v textech stránek, jedna oprava se promítne do všech stránek, které zdroj citují, a validátor může celý registr porovnat s Crossrefem jedním průchodem. Návrh registru důkazů popisuje článek [Registr důkazů jako kód](@/engineering/evidence-ledger-as-code/index.cs.md).

## Zola 0.23.6 a komponenty Tera v2

Zola byla zvolena proto, že je to jediný statický binární soubor s vestavěnou podporou vícejazyčného obsahu, taxonomií, feedů, sitemapy a kontroly interních odkazů. Mezi Markdownem a HTML nestojí žádné běhové prostředí Node ani Ruby a verze je zafixovaná v `.zola-version`; CI stáhne právě toto vydání a před použitím ověří jeho otisk SHA-256.

Verze 0.23 přináší Tera v2, která nahrazuje makra **komponentami**: pojmenovanými šablonovými funkcemi s typovanými parametry a syntaxí volání podobnou JSX. První checkpoint v záznamu Majordomu pro tento projekt přechod výslovně zmiňuje („Tera v2 port: macros replaced by components“). Komponenta deklaruje své parametry a jejich typy:

{% raw -%}
```text
{% component library.tags(tags: array, lang: string) %}
{%- if tags | length > 0 %}
<ul class="tag-list" aria-label="{{ trans(key='nav_tags', lang=lang) }}">
```
{%- endraw %}

a šablona stránky ji volá jako element:

{% raw -%}
```text
{{ <library.cards pages={section.pages} lang={lang} /> }}
```
{%- endraw %}

Typované parametry znamenají víc, než se zdá. Chybějící nebo překlepnutý argument selže při buildu místo toho, aby se vykreslil prázdný řetězec, což je právě ten druh chyby, kvůli kterému zůstávají chyby šablon ve statických webech neviditelné. Komponenty jsou seskupené podle funkce, ne podle HTML elementů: `library` (karty, klíčové body, literatura, obrázky), `evidence` (štítky druhu, odznaky úrovně a jistoty, karty tvrzení), `discover` (pojmy ze slovníku a související čtení), `models`, `landing`, `artifact` a `posters`. Stránku, kterou čtete, vykresluje [templates/essay.html](https://github.com/korczis/catharsis-as-a-service/blob/main/templates/essay.html), tatáž šablona jako výzkumné a teoretické eseje; tato sekce jen nastavuje `kind = "technical"`, takže stránka nese štítek TECHNICKÉ místo EMPIRICKÉ.

## Styly: Tailwind CSS 4 a Flowbite, hostované lokálně

Tailwind 4 se konfiguruje v CSS, ne v konfiguračním souboru JavaScriptu. Vstupní soubor přesně určuje, které soubory skener tříd čte, načítá plugin Flowbite a definuje designové tokeny:

```css
@import 'tailwindcss' source(none);

@source '../templates';
@source '../static/js/app.js';
@source '../node_modules/flowbite/lib/esm/components';

@plugin 'flowbite/plugin';

@theme {
  --color-ink: #050505;
  --color-bone: #e9e4d8;
  --color-blood: #ef2929;
```

`source(none)` vypíná automatické vyhledávání, takže třída se do výsledku dostane jen tehdy, když se objeví v šabloně, v jediném skriptu, který přepíná třídy, nebo v komponentách Flowbite, které markup používá. Tokeny (inkoustová, kostní a krvavá barva; písma Anton, Barlow Condensed a JetBrains Mono) pocházejí z plakátu, takže knihovna i dílo působí jako jeden celek.

Žádný asset se nenačítá z CDN. Písma jsou hostovaná lokálně i s licencemi OFL a sedmnáctiřádkový skript [scripts/vendor.mjs](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/vendor.mjs) kopíruje zafixované balíčky Alpine a Flowbite z `node_modules` do `static/js/vendor/`. Web tedy nevysílá žádné požadavky třetím stranám, a právě díky tomu může registr důkazů uvádět, že nepoužívá analytiku, trackery ani cookies.

## Chování: Alpine a Flowbite, nikdy vlastníci obsahu

Interakci zajišťují dvě malé knihovny s přísně rozdělenými rolemi, které jsou zapsané v architektonickém pravidle: „One owner per piece of DOM state: Alpine or Flowbite, never both“, tedy každý kus stavu DOM má jediného vlastníka.

- **Flowbite** dodává mechaniky, u kterých se snadno pokazí přístupnost: modální okno, vysouvací panel, tooltipy a akordeon.
- **Alpine.js** dodává lokální stav: přepínač pohledu na stránce díla, tlačítko kopírování, panely tvrzení, které otevírají zdroje, interaktivní modely a stránku hledání.

Skripty se načítají odloženě a v pořadí, které zajistí, že stránkové skripty zaregistrují své komponenty Alpine dřív, než Alpine nastartuje:

{% raw -%}
```html
<script src="{{ get_url(path='js/vendor/flowbite.min.js', cachebust=true) }}" defer></script>
<script src="{{ get_url(path='js/app.js', cachebust=true) }}" defer></script>
<script src="{{ get_url(path='js/vendor/alpine.min.js', cachebust=true) }}" defer></script>
```
{%- endraw %}

Veškerý obsah je v HTML. Panel se zdroji na kartě tvrzení například skrývá vazba Alpine a pravidlo `.no-js` ho nechá otevřený, když skripty neběží. Prohlížečové testy načítají stránky s vypnutým JavaScriptem a ověřují, že to platí.

## Problém podcesty

GitHub Pages servíruje web projektu pod `/<repozitář>/`. Napevno zapsaná cesta `/assets/poster.png` funguje na počítači vývojáře a v produkci se rozbije. Projekt to řeší na třech místech:

- `base_url` v `zola.toml` je převzatá z API GitHubu a komentář to uvádí. Job nasazení ji porovná s URL, kterou vrací akce `configure-pages` od GitHubu, a pokud se liší, zastaví se.
- Šablony skládají každou URL přes `get_url`, `resize_image` nebo permalink, nikdy spojováním řetězců.
- [`npm run preview`](../../commands/#npm-run-preview) servíruje produkční build pod `http://127.0.0.1:4173/catharsis-as-a-service/` a prohlížečové testy běží proti této adrese, takže chyba v základní cestě selže před pushem, ne po něm.

## Obsahové API a klient v Rustu

Knihovna se publikuje i jako data. [`python3 scripts/export-api.py`](../../commands/#export-api) zapíše vedle webu adresář `api/v1/`: index, kolekce výzkumu a rad pro každý jazyk, literaturu, registr tvrzení, hodnocení zdrojů, slovník, changelog důkazů, rejstřík příkazů a vyhledávací index pro každý jazyk. Docstring exportéru uvádí omezení, díky kterému je testovatelný: „Output is deterministic: no timestamps, stable ordering“, tedy výstup je deterministický, bez časových razítek a se stabilním pořadím. Test v Pythonu exportuje dvakrát a porovná bajty.

Workspace v Rustu v `crates/` je spotřebitel. `caas-content` deserializuje export do typů a kontroluje invarianty, na které se jiné aplikace spoléhají; `caas-cli` je klient pro příkazovou řádku:

```rust
let library = Library::load("public/api/v1")?;
assert!(library.problems().is_empty());

for claim in library.claims_due_by("2027-03-31") {
    println!("{} {} {}", claim.id, claim.claim_type, claim.review_due);
}
```

Smyslem druhého jazyka je nezávislost. Exportér v Pythonu a typy v Rustu jsou napsané odděleně, takže pole přejmenované na jedné straně shodí testy kontraktu na druhé. CI vyexportuje API testovaného commitu a spustí proti němu [`cargo test --workspace`](../../commands/#cargo-test) vedle [`cargo clippy`](../../commands/#cargo-clippy), který každé varování považuje za chybu. CLI se spouští jako [`cargo run -p caas-cli`](../../commands/#caas-cli); jeho příkaz `claims list --due-by` prakticky ukáže, která tvrzení potřebují revizi do daného data. Kontrakt dokumentuje [docs/RUST-INTEGRATION.md](https://github.com/korczis/catharsis-as-a-service/blob/main/docs/RUST-INTEGRATION.md).

## Pipeline od začátku do konce

[`npm run build`](../../commands/#npm-run-build) je krátká cesta: přibalit knihovny, zkompilovat Tailwind, spustit Zolu, vyexportovat API. Podstatná je cesta [`npm run validate`](../../commands/#npm-run-validate): jediný bashový skript [scripts/validate.sh](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate.sh), jehož kroky se zastaví u prvního selhání:

```text
step toolchain zola_version
step assets npm run --silent assets
step javascript js_syntax
step i18n python3 scripts/validate-i18n.py
step content python3 scripts/validate-content.py
step references python3 scripts/check-references.py
step claims python3 scripts/validate-claims.py
step social python3 scripts/render-social.py --check
step zola-check zola check --skip-external-links
step zola-build zola build --base-url "$BASE_URL"
step api python3 scripts/export-api.py --out public --base-url "$BASE_URL"
step html python3 scripts/validate-html.py public "$BASE_URL"
```

První vydání procházelo sedmi z těchto kroků; ostatní přibyly s růstem knihovny ([historie validate.sh na GitHubu](https://github.com/korczis/catharsis-as-a-service/commits/main/scripts/validate.sh) ukazuje kdy). Kroky jsou seřazené od nejlevnějšího po nejdražší, takže chybějící překlad selže za sekundu, ještě před úplným buildem.

Na GitHubu řetězí [pages.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/pages.yml) čtyři fáze, z nichž každá čeká na úspěch předchozí:

1. **CI**, převzaté z [ci.yml](https://github.com/korczis/catharsis-as-a-service/blob/main/.github/workflows/ci.yml), takže brána před nasazením je stejná jako brána před mergem: Conventional Commits, dozor Majordomu, validace a build, testy v Pythonu, Rust, literatura proti Crossrefu a prohlížečové testy na náhledu pod podcestou.
2. **Nasazení** nahraje artefakt webu, který vytvořil validační job. Nasazení není druhý build, takže do produkce jdou přesně ty soubory, které prošly kontrolou.
3. **Ověření produkce** počká, až živý web servíruje nasazovaný commit, a pak proti skutečné URL spustí [`npm run smoke`](../../commands/#npm-run-smoke) a [`npm run test:production`](../../commands/#npm-run-test-production).
4. **Vydání** publikuje GitHub Release. Verze se počítá z předmětů commitů podle Conventional Commits od posledního tagu a poznámky odkazují na běh pipeline; [`scripts/release.sh --dry-run`](../../commands/#release-dry-run) stejný výpočet vypíše lokálně, aniž by cokoli publikoval.

Čekání ve třetím kroku se opírá o patičku, která vykresluje SHA commitu z prostředí buildu:

```sh
for attempt in $(seq 1 40); do
  if curl -fsS "${BASE_URL}?revision=${GITHUB_SHA}" | grep -q "$GITHUB_SHA"; then
    echo "production serves $GITHUB_SHA (attempt $attempt)"
    exit 0
  fi
  sleep 15
done
```

Bez něj by testy mohly projít proti předchozímu nasazení, zatímco CDN ještě servíruje staré soubory. Stejná metadata plní generovanou [stránku stavu](@/status/index.cs.md).

## Co architektura stála a co přinesla

Rozdělení na obsah, data a šablony stojí nepřímost. Kdo přidává výzkumnou poznámku, musí vědět, že její tvrzení patří do `data/claims.toml`, literatura do `data/references.toml` s hodnocením v `data/sources.toml` a příkazy do `data/commands.toml`. Validátory tuto znalost převádějí na chybové zprávy se souborem a řádkem, a jen díky tomu je rozdělení použitelné pro AI agenta i pro lidi.

Co přineslo, je vidět v záznamech. První pipeline nasazení, [běh 34834554169](https://github.com/korczis/catharsis-as-a-service/actions/runs/34834554169), prošla všemi sedmi joby a publikovala [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0). Do doby psaní tohoto článku následovalo téhož dne dalších pět vydání, každé až po živém ověření. Dvě selhání pipeline zaznamenaná toho dne se zastavila tam, kde to návrh předpokládá: jedno před nasazením, když kontrola Crossrefu odmítla název zdroje, a druhé po nasazení, ale před vydáním, když v produkci selhal prohlížečový test. Obě rozebírá článek [Testování statického webu](@/engineering/testing-a-static-site/index.cs.md) a časy uvádí [Účtování času](@/engineering/time-accounting/index.cs.md).
