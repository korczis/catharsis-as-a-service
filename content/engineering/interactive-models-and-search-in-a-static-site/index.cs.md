+++
title = "Interaktivní modely a hledání ve statickém webu"
description = "Jak web bez serveru spouští simulace a hledání v prohlížeči čtenáře: modely v Alpine.js kreslené jako SVG včetně Kuramotova modelu synchronizace, hledání bez ohledu na diakritiku nad exportovaným indexem a náhledy pro sociální sítě vykreslené jednou a ověřované otiskem bez prohlížeče."
date = 2026-09-14
weight = 6

[taxonomies]
tags = ["technika", "simulace", "hledání", "alpine"]

[extra]
kicker = "Technika 06"
kind = "technical"
summary = "Tři funkce vypadají, jako by potřebovaly server, a nepotřebují ho. Pět interaktivních modelů běží jako malé komponenty Alpine.js, které z posuvníků přepočítávají cesty SVG, s pevným semínkem náhody, takže každý čtenář vidí stejný běh. Hledání jednou načte index JSON pro daný jazyk a výsledky řadí v prohlížeči bez ohledu na velikost písmen a diakritiku, přičemž české tvary slov páruje hrubým kmenem. Náhledy pro sociální sítě se vykreslují lokálně v headless Chromu a CI je ověřuje podle manifestu otisků bez spuštění prohlížeče. Článek vysvětluje každý návrh a jeho meze."
key_points = [
  "Modely jsou deterministické: generátor mulberry32 se semínkem a pevné časové kroky zajistí, že stejné vstupy vždy nakreslí stejné křivky, takže modely jsou testovatelné a jejich výstupy pro každého čtenáře opakovatelné.",
  "Hledání normalizuje text Unicode dekompozicí, odstraní kombinující znaménka a porovnává zkrácené kmeny, takže dotaz napsaný bez české diakritiky nebo v jiné velikosti písmen stále najde shodu.",
  "Náhledové obrázky jsou drahý produkt buildu, proto pipeline místo nového vykreslení kontroluje manifest otisků vstupů; stránka s chybějícím nebo zastaralým obrázkem neprojde validací.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Omezení

Všechno na tomto webu jsou statické soubory na GitHub Pages. Není tu server, který by spouštěl kód, databáze, kterou by šlo dotazovat, ani záměrně žádná služba třetí strany: web neposílá požadavky na jiné domény, nenastavuje cookies a nenačítá analytiku. Obsah musí zůstat čitelný i bez JavaScriptu. Tím odpadají obvyklá řešení tří funkcí, které knihovna potřebovala:

- interaktivní modely, ve kterých čtenář změní předpoklad a sleduje důsledek;
- hledání napříč oběma jazykovými verzemi a slovníkem;
- vlastní náhledový obrázek odkazu pro každou stránku v každém jazyce.

Každá z nich je postavená tak, aby se drahá nebo dynamická část odehrála buď v prohlížeči čtenáře, nebo jednou na počítači vývojáře, a aby build mohl výsledek zkontrolovat bez opakování práce.

## Pět modelů jako komponenty Alpine

[Stránka interaktivních modelů](@/models/index.cs.md) spouští pět simulací: smyčku úlevy, ventilování a vzrušení v čase, paměť vrcholu a konce, synchronizaci vázaných oscilátorů a alostatickou zátěž. Každá je komponentou Alpine.js definovanou v [static/js/models.js](https://github.com/korczis/catharsis-as-a-service/blob/main/static/js/models.js), skriptu o 344 řádcích, který se načítá jen na této stránce a zaregistruje se dřív, než Alpine nastartuje.

Rozdělení odpovědností je stejné jako jinde na webu ([Jak web vznikl](@/engineering/how-the-site-was-built/index.cs.md)): **obsah žije v Markdownu, chování v JavaScriptu.** Otázka každého modelu, vysvětlení, návod ke čtení grafu, předpoklady, meze, literatura a všechny popisky rozhraní jsou pole front matter v `content/models/index.md` a jeho české verzi. Šablona předá popisky komponentě jako JSON:

{% raw -%}
```html
<div class="model" data-requires-js data-model="synchrony" x-data="synchrony"
     data-labels="{{ l | json_encode }}">
```
{%- endraw %}

takže skript neobsahuje žádný text vázaný na jazyk a čtenář bez JavaScriptu stále dostane celé vysvětlení, předpoklady a meze, spolu s poznámkou, že interaktivní část potřebuje skripty.

Grafy jsou obyčejné SVG. Komponenta vystavuje vypočítané gettery a Alpine je váže na atributy cest a kruhů:

```js
const line = (values, max) =>
  values.map((value, index) => `${index ? 'L' : 'M'}${x(index, values.length).toFixed(1)},${y(value, max).toFixed(1)}`).join(' ');
```

Žádná knihovna pro grafy tu není. Každý graf na stránce obslouží viewBox 600 × 240, tři pomocné funkce a několik tříd CSS, takže vizuální jazyk odpovídá zbytku webu a celá funkce nepřidává jedinou závislost.

### Determinismus

Dva z modelů obsahují náhodu: zda se v epizodě změní příčina distresu a jaká jsou vlastní tempa oscilátorů. `Math.random()` by každé načtení stránky udělalo jiné, což je nepříjemné pro čtenáře, kteří si výsledky porovnávají, a ještě horší pro testy. Skript proto používá malý generátor se semínkem:

```js
// mulberry32: a small deterministic generator so every reader sees the same run for the same inputs.
const random = (seed) => {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};
```

S pevným semínkem a pevnými časovými kroky vytvoří stejné polohy posuvníků vždy stejné křivky. Prohlížečový test „interactive models respond to their inputs and stay labelled as illustrative“ proto může změnit vstup, ověřit změnu výstupu a potvrdit, že modely zůstávají označené; banner stránky zní „Ilustrativní modely · nejde o předpovědi o kterémkoli člověku“ v české verzi a „Illustrative models · not predictions about any person“ v anglické.

## Kuramotův model v prohlížeči

Model synchronizace je z pěti nejvýpočetnější. Kuramotův model popisuje populaci oscilátorů, z nichž každý má vlastní frekvenci a každý je přitahován k fázím ostatních. Pod kritickou silou vazby se fáze rozcházejí; nad ní se část populace sladí do společného rytmu. Web ho používá jako analogii kolektivního rytmu a uvádí to v registru i na stránce: jde o matematický model synchronizace obecně, ne o model tanečníků, davů nebo sbližování.

Implementace používá tvar středního pole, který se vyhne porovnávání každé dvojice oscilátorů. Komponenta nejprve změří parametr uspořádání, tedy délku *r* a úhel ψ průměru všech fází chápaných jako jednotkové vektory:

```js
measure() {
  const n = this.phases.length;
  const re = this.phases.reduce((sum, phase) => sum + Math.cos(phase), 0) / n;
  const im = this.phases.reduce((sum, phase) => sum + Math.sin(phase), 0) / n;
  this.order = Math.hypot(re, im);
  this.angle = Math.atan2(im, re);
},
```

Pak se každý oscilátor posune o jeden Eulerův krok rovnice dθᵢ/dt = ωᵢ + K·r·sin(ψ − θᵢ):

```js
this.phases = this.phases.map((phase, index) =>
  phase + DT * (this.tempos[index] + k * this.order * Math.sin(this.angle - phase)));
```

S nejvýš 40 oscilátory, časovým krokem 0,05 a dvěma kroky na snímek animace stojí jeden snímek několik set goniometrických výpočtů, což telefon zvládne s rezervou. Animace běží přes `requestAnimationFrame` a při pozastavení se zastaví; tlačítko „Krok“ posune model o 40 kroků najednou bez animace. Kruh s body a šipka pro *r* jsou prvky SVG navázané na fáze; druhé SVG kreslí nedávnou historii *r*.

Malé populace se nechovají jako teorie a stránka to místo zamlčení uvádí: se 4 až 40 oscilátory *r* kolísá a ani bez vazby téměř neklesne na nulu, protože ostrý práh matematické teorie platí pro velmi velké populace. Simulace, která by vypadala čistěji, než matematika dovoluje, by odporovala vlastnímu standardu webu pro výstupy podobné datům. Tvrzení modelu, včetně prahu vazby a jeho použití jen jako analogie, jsou záznamy v registru důkazů se zdroji Kuramoto (1984) a Strogatz (2000).

## Hledání bez vyhledávacího serveru

[Stránka hledání](@/search/index.cs.md) prohledává všechny stránky v aktuálním jazyce, včetně této, a všechny pojmy slovníku. Index vzniká při buildu, vytváří ho [`python3 scripts/export-api.py`](../../commands/#export-api) a zapisuje do `api/v1/search.en.json` a `search.cs.json`. Každá položka má URL, název, popis, sekci, kicker, štítky a nejvýš 1 500 znaků textu bez syntaxe Markdownu, odkazů a bloků kódu. Pojmy slovníku se stávají položkami, jejichž URL míří na kotvu pojmu na stránce slovníku.

[static/js/search.js](https://github.com/korczis/catharsis-as-a-service/blob/main/static/js/search.js) index jednou stáhne, předem normalizuje všechna pole a během psaní položky řadí. Většinu práce odvede normalizace:

```js
const normalize = (value) =>
  String(value ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase();

const stem = (term) => (term.length >= STEM_FROM ? term.slice(0, Math.max(STEM_MIN, term.length - STEM_TRIM)) : term);
```

`NFD` rozloží „č“ na „c“ a kombinující háček a regulární výraz kombinující znaménka odstraní, takže „přehodnocení“ a „prehodnoceni“ se porovnají jako shodné. Čeština silně skloňuje a dotaz „katarzi“ má najít stránky, kde stojí „katarze“. Plnohodnotný stemmer pro češtinu by byl velkou závislostí, a tak skript zkracuje: slovům o šesti a více znacích ubere poslední dva, ale nikdy je nezkrátí pod pět. „Katarze“ i „katarzi“ se tak stanou „katar“. Prohlížečový test na české stránce hledání zadává přesně tyto dva případy.

Řazení je vážené hledání podřetězců. Každé slovo dotazu musí někde najít shodu, jinak má položka nula bodů; shoda přidá 10 bodů v názvu, 5 v kickeru nebo štítcích, 3 v popisu a 1 v textu. Výsledky se řadí podle skóre, pak podle názvu, a omezí se na 50. Dotaz se zrcadlí do `?q=` přes `history.replaceState`, takže na hledání lze odkázat a historie prohlížeče se nezahltí.

Kompromisy jsou záměrné a viditelné. Zkracování nadměrně páruje krátké běžné kmeny. Prohledává se jen prvních 1 500 znaků textu stránky, což drží index malý, ale mine pozdní oddíly dlouhých esejí. Hledání netoleruje překlepy. Na oplátku nepřidává žádnou závislost ani službu, dotaz nikdy neopustí prohlížeč a celý index je souborem ve veřejném API, který si lze prohlédnout.

## Náhledy pro sociální sítě: vykreslit jednou, kontrolovat pořád

Odkaz sdílený v chatu nebo na sociální síti zobrazí náhledový obrázek. Jediný obrázek pro celý web by způsobil, že každá sdílená stránka vypadá stejně, a tak každá obsahová stránka v každém jazyce dostane vlastní kartu 1200 × 630 se svým názvem, sekcí a kickerem.

Vykreslení karet vyžaduje skutečný prohlížeč, protože návrh používá webová písma webu a český text. [`python3 scripts/render-social.py`](../../commands/#render-social) otevře [artwork/og.html](https://github.com/korczis/catharsis-as-a-service/blob/main/artwork/og.html) v headless Chromu s poli stránky jako parametry dotazu, pořídí snímek a ImageMagickem ho převede na progresivní JPEG, přičemž několik stránek vykresluje paralelně. Výstupní cesta kopíruje cestu obsahu: z `content/research/x/index.cs.md` se stane `static/og/research/x/index.cs.jpg`.

CI to rozumně dělat při každém pushi nemůže a ani nemusí. Skript zapisuje manifest, který pro každý obrázek uchovává otisk SHA-256 všeho, co určuje jeho pixely:

```python
digest = hashlib.sha256(json.dumps({**fields, "template": template_hash}, sort_keys=True).encode()).hexdigest()
```

kde `fields` jsou název, popisek sekce, kicker, červený řádek v patičce a jazyk a `template_hash` je otisk samotného `og.html`. S `--check` skript prohlížeč vůbec nepotřebuje. Přepočítá otisky ze souborů obsahu a selže, když stránka nemá obrázek, když se zaznamenaný otisk liší (upravil se název nebo se změnila šablona) nebo když obrázek nepatří žádné stránce. Tato kontrola je krok `social` v [`npm run validate`](../../commands/#npm-run-validate). Testy v Pythonu jí podstrčí chybějící i zastaralý náhled a ověří obě hlášky a prohlížečový test potvrdí, že vybrané stránky v obou jazycích mají odlišné URL `og:image` s odpovědí typu `image/jpeg`.

Jeden detail šablony ukazuje, proč vykreslování nezůstalo na obecném nástroji. Nadpisové písmo je zúžené a jeho verzálky těsně dosedají na řádek nad sebou, a české verzálky nesou diakritiku nad výškou verzálek:

```css
/* Czech capitals carry accents above the cap height; Anton needs extra leading so they clear the line above. */
:lang(cs) h1 { line-height: 1.24; padding-top: 0.08em; }
```

Podobná úprava je i na samotném webu: checkpoint z prvního vydání zaznamenává, že proklad českých nadpisů byl zvýšen na 1,2 „after measuring diacritic collisions“, tedy po změření kolizí diakritiky.

Schéma otisků má meze a stojí za to je uvést. Otisk pokrývá pole stránky a soubor šablony, ale ne soubory písem, které šablona načítá, ani verzi Chromu, která ji vykresluje. Změna písma by nechala všechny obrázky označené jako aktuální; nápravou je nové vykreslení s `--force`. Vykreslování je také vázané na počítač vývojáře s nainstalovaným Chromem a ImageMagickem; pipeline obrázky ověřuje, nevyrábí je.

## Společný vzorec

Všechny tři funkce sledují stejný vzorec. Drahou nebo dynamickou práci umístit tam, kde je nejlevnější: do prohlížeče čtenáře u modelů a hledání, jednou na pracovní stanici u obrázků. To, co práce potřebuje, exportovat jako prostá data, která si lze prohlédnout: front matter, index JSON, manifest otisků. A výsledku pak nevěřit, ale nechat ho ověřit buildem. Modely jsou dost deterministické na to, aby šly testovat, vyhledávací index je součástí verzovaného API s vlastními testy a náhledový obrázek nemůže zastarat, aniž by neprošel validací.
