+++
title = "Testování statického webu: validátory, negativní testy, prohlížeče a kontrakty"
description = "Vrstvy kontrol mezi commitem a vydáním: seřazený validační skript, validátory v Pythonu testované na selhání, Playwright na náhledu pod podcestou i v produkci, testy kontraktu v Rustu a rejstřík příkazů, jehož každá položka se skutečně spouští."
date = 2026-09-14
weight = 4

[taxonomies]
tags = ["technika", "testování", "playwright", "validace"]

[extra]
kicker = "Technika 04"
kind = "technical"
summary = "Statický web nemá server, který by se mohl rozbít, a tak je lákavé testovat ho jen zběžně. Tento web ale publikuje hodnocená tvrzení ve dvou jazycích pod podcestou repozitáře a většina jeho chyb je tichá: chybějící překlad, zastaralé tvrzení, rozbitá kotva, URL assetu, která funguje lokálně, ale ne v produkci. Článek popisuje kontroly, které tyto chyby zachytí, zásadu, že každý validátor musí být viděn selhat, a tři selhání, která pipeline zaznamenala v den vzniku webu."
key_points = [
  "Validace běží ve dvanácti seřazených krocích od nejlevnějšího po nejdražší a tentýž skript hlídá lokální práci, CI i nasazení.",
  "Každý validátor v Pythonu má testy, které mu podstrčí záměrně rozbitá data a ověří přesnou chybovou hlášku, takže validátor, který by potichu propouštěl vše, by neprošel vlastní sadou.",
  "Prohlížečové testy běží pro každé vydání dvakrát: před nasazením na lokálním buildu servírovaném pod produkční podcestou a po nasazení na živé URL.",
]
figures = []
references = ["repository-2026", "majordomus-2026"]
+++

## Co se může ve statickém webu pokazit

Web v tomto repozitáři nemá databázi ani aplikační server, a přesto může být v produkci chybný mnoha způsoby bez jediné chybové hlášky:

- chybí česká verze stránky, nebo má jiný tvar front matter než anglická;
- text rozhraní existuje jen v jednom slovníku, takže šablona vykreslí prázdný popisek;
- tvrzení na stránce překročilo datum revize;
- literatura cituje DOI, jehož název už nesouhlasí;
- kotva na stránce nebo URL assetu je rozbitá, často jen pod podcestou `/catharsis-as-a-service/`;
- strukturovaná data nejdou načíst, nebo stránku popisují jako lékařský zdroj;
- příkaz uvedený v dokumentaci neexistuje, nebo existuje, ale žádný test ho nespouští;
- nasazení proběhlo, ale CDN stále servíruje předchozí build.

Každá položka tohoto seznamu má v repozitáři svou kontrolu. Článek prochází kontroly od nejrychlejší po nejpomalejší a pak selhání, která zaznamenaly. Pipeline, která je spouští, popisuje článek [Jak web vznikl](@/engineering/how-the-site-was-built/index.cs.md).

## Fáze 1: jeden seřazený validační skript

[`npm run validate`](../../commands/#npm-run-validate) spouští [scripts/validate.sh](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate.sh). Každý krok je obalený stejnou funkcí, která zaznamená PASS nebo FAIL, vypíše souhrnnou tabulku a u prvního selhání skončí:

```bash
step() {
  local name="$1"
  shift
  printf '\n── %s: %s\n' "$name" "$*"
  if "$@"; then
    RESULTS+=("$name|PASS")
  else
    RESULTS+=("$name|FAIL")
    report
    printf '\nRESULT %s FAIL\n' "$(dots RESULT)"
    exit 1
  fi
}
```

Kroky jsou v tomto pořadí: nástroje (verze Zoly musí odpovídat `.zola-version`), assety, syntaxe JavaScriptu, překlady, obsahové standardy, literatura, registr důkazů, náhledy pro sociální sítě, kontrola Zoly, build Zoly, export API a kontroly HTML nad vygenerovaným webem. Pořadí je záměrné. Kontrola překladů trvá hluboko pod sekundu a zachytí nejčastější autorskou chybu, a proto běží před buildem, který trvá mnohem déle.

Skript nemá žádnou volbu, jak krok přeskočit. Projektové pravidlo o nasazení říká „Validation is never bypassed to make CI pass: no `|| true` around a mandatory check, no `--no-verify`“ a job CI spouští stejný vstupní bod jako vývojář.

## Fáze 2: validátory v Pythonu testované na selhání

Validátory jsou malé skripty v Pythonu jen se standardní knihovnou a každý má jednu odpovědnost:

| Validátor | Zachytí |
|---|---|
| [validate-i18n.py](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate-i18n.py) | chybějící překlady obsahu, neshodu tvaru front matter, klíče rozhraní použité v šablonách, ale nedefinované |
| [`python3 scripts/validate-content.py`](../../commands/#validate-content) | chybějící pole výzkumných poznámek, délku popisu, zakázané formulace, neregistrované nebo neodkázané příkazy |
| [`python3 scripts/check-references.py --online`](../../commands/#check-references) | neznámé citace, články bez DOI; online neshodu názvu a roku s Crossrefem |
| [`python3 scripts/validate-claims.py`](../../commands/#validate-claims) | pravidla registru důkazů popsaná v článku [Registr důkazů jako kód](@/engineering/evidence-ledger-as-code/index.cs.md) |
| [`python3 scripts/render-social.py`](../../commands/#render-social) s `--check` | stránku bez náhledového obrázku, zastaralý obrázek, osiřelý obrázek |
| [validate-html.py](https://github.com/korczis/catharsis-as-a-service/blob/main/scripts/validate-html.py) | duplicitní id, chybějící alt, skoky v úrovních nadpisů, rozbité interní odkazy a kotvy, nevalidní JSON-LD, lékařské typy schématu, neúplná metadata náhledů |

Validátor je užitečný jen tehdy, když selže, kdy má, a validátor, který na repozitáři projde, o tom nic neříká. Docstring testovacího modulu zásadu uvádí: „Validators must pass on the repository and fail on the defects they exist to catch.“ Téměř každý validátor má proto v [tests/python](https://github.com/korczis/catharsis-as-a-service/tree/main/tests/python) dva druhy testů: jeden ho spustí na skutečném repozitáři a čeká úspěch, několik dalších postaví v dočasném adresáři minimální rozbitá data a ověří konkrétní hlášku:

```python
def test_content_rejects_wrong_registry_anchor(tmp_path):
    root = _content_fixture(tmp_path, "Run [`npm run validate`](../commands/#npm-test).\n")
    result = run([PY, str(ROOT / "scripts/validate-content.py"), "--root", str(root)])
    assert result.returncode == 1
    assert "must link to the registry anchor #npm-run-validate" in result.stdout
```

Přístup s testovacími daty vyžaduje, aby každý validátor přijímal argument `--root` nebo proměnnou prostředí `CAAS_ROOT`. Je to drobné omezení návrhu, které vyplývá z chuti psát negativní testy. Validátor registru přijímá i `--today`, díky čemuž může test ukázat, že tvrzení repozitáře bez revize v roce 2031 expirují.

[`npm run test:python`](../../commands/#npm-run-test-python) spouští sadu v projektovém virtuálním prostředí. Ve [v0.5.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.5.0) měla 40 testů.

## Fáze 3: rejstřík příkazů se spouští

Dokumentace se seznamy příkazů má sklon zastarávat, a proto je každý příkaz, který zmiňuje web, README nebo dokumenty, zapsaný v [data/commands.toml](https://github.com/korczis/catharsis-as-a-service/blob/main/data/commands.toml) se seznamem `verified_by`, který jmenuje joby CI nebo funkce pytest, jež ho spouštějí. Obsahový validátor odmítne příkaz v textu, který neodkazuje na svou položku. [tests/python/test_commands.py](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/python/test_commands.py) uzavírá smyčku z opačné strany: přečte soubory workflow a testovací moduly a selže, pokud jméno ve `verified_by` neexistuje.

```python
for reference in entry["verified_by"]:
    kind, _, name = reference.partition(":")
    if kind == "ci" and name not in jobs:
        problems.append(f"{entry['id']}: CI job '{name}' does not exist (known: {sorted(jobs)})")
    elif kind == "pytest" and name not in tests:
        problems.append(f"{entry['id']}: pytest '{name}' does not exist")
```

Tentýž modul příkazy skutečně spouští: linter commitů nad správnou a chybnou zprávou, skript vydání v režimu nanečisto, produkční build, vývojový server (dotazovaný, dokud neodpoví), `--help` pro každý podpříkaz Majordomu a čtení historie pipeline přes GitHub CLI. Testy, které potřebují externí nástroj, se lokálně přeskočí, když nástroj chybí, ale CI nastavuje `CAAS_REQUIRE_TOOLS=1` a pak chybějící nástroj test shodí. Bez tohoto přepínače by položka rejstříku mohla být „ověřená“ testem, který nikdy neběžel.

Každý odkaz na příkaz v tomto článku míří do tohoto rejstříku. Čtete výsledek kontroly, která to vynucuje.

## Fáze 4: Playwright pod produkční podcestou

[`npm test`](../../commands/#npm-test) spouští prohlížečové testy v [tests/site.spec.js](https://github.com/korczis/catharsis-as-a-service/blob/main/tests/site.spec.js). Bez `BASE_URL` si Playwright sám spustí server náhledu, takže testy běží proti produkčnímu buildu servírovanému pod stejnou podcestou jako GitHub Pages:

```js
const LOCAL_URL = 'http://127.0.0.1:4173/catharsis-as-a-service/';
const baseURL = process.env.BASE_URL || LOCAL_URL;
```

Několik bloků testů jsou smyčky přes jazyky, velikosti okna a stránky, takže spuštěných testů je víc než bloků. Sada kontroluje to, co vidí jen prohlížeč: stránky se vykreslí ve všech nastavených velikostech okna bez vodorovného přetečení; každá stránka je sama sobě kanonická se správnými alternativami `hreflang`; modální okno Flowbite drží fokus a vysouvací panel se zavírá; panely tvrzení otevírají zdroje s JavaScriptem a bez něj zůstávají otevřené; slovník má kotvy; simulace na stránce metod zůstává označená jako simulace; tiskové styly promění dílo v papírový dokument; stránky knihovny jsou `Article`, nikdy `MedicalWebPage`.

Prohlížečový test je také jediný spolehlivý test „čitelnosti bez JavaScriptu“. Jeden blok vytvoří kontext s vypnutým JavaScriptem a ověří, že obsah, navigace i zdroje tvrzení zůstávají dostupné.

Sada rostla s webem: 30 testů ve [v0.1.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.1.0), 72 úspěšných ve v0.5.0 podle předávky zapsané při jejím vydání a 84 v produkčním běhu pro commit [d2b3c47](https://github.com/korczis/catharsis-as-a-service/commit/d2b3c47608f29ece52f0e42045496f160a45c163).

## Fáze 5: tatáž sada proti produkci

Po nasazení job `Verify production` počká, až patička živého webu obsahuje SHA nasazovaného commitu, a pak spustí [`npm run smoke`](../../commands/#npm-run-smoke) a [`npm run test:production`](../../commands/#npm-run-test-production). Smoke skript stáhne každý vstupní bod, feed, náhledový obrázek a vlastní asset a porovná stavové kódy a atributy `lang`; prohlížečová sada pak beze změny běží proti živé URL.

Spouštět stejné testy dvakrát není nadbytečné. Náhled je HTTP server v Pythonu na linuxovém runneru; produkce je GitHub Pages za CDN s vlastními hlavičkami, cache a přesměrováními. Třetí z níže popsaných selhání prošlo na náhledu a selhalo v produkci.

## Fáze 6: testy kontraktu v Rustu

JSON API se testuje z druhého jazyka. [crates/caas-content/tests/contract.rs](https://github.com/korczis/catharsis-as-a-service/blob/main/crates/caas-content/tests/contract.rs) spustí exportér do dočasného adresáře, nebo přečte `CAAS_API_DIR`, když ho CI nastaví na export testovaného commitu, a ověří, že se typovaná knihovna načte a nemá problémy s integritou:

```rust
#[test]
fn the_exported_library_has_no_integrity_problems() {
    let problems = library().problems();
    assert!(
        problems.is_empty(),
        "integrity problems:\n{}",
        problems.join("\n")
    );
}
```

Crate CLI má vlastní testy, které spouštějí binárku `caas`. [`cargo test --workspace`](../../commands/#cargo-test), [`cargo clippy`](../../commands/#cargo-clippy) s varováními jako chybami a [`cargo fmt`](../../commands/#cargo-fmt) běží v jobu CI `Rust`. Ve v0.5.0 měl workspace 21 testů v Rustu.

## Co kontroly zachytily první den

Záznamy ukazují tři podstatná selhání a každé se zastavilo v jiné vrstvě.

**Nestabilní test tisku, zachycený lokálně.** Checkpoint zapsaný v 11:09 UTC uvádí „E2E was 36/37: print test read computed style once“. Sonda na náhledu ukázala, že tiskové styly se uplatnily, takže chyba byla v testu, který vypočtený styl přečetl jen jednou, místo aby na něj počkal. Test byl upraven tak, aby se dotazoval opakovaně. S tímto selháním se nic nepushnulo.

**Neshoda názvu s Crossrefem, zachycená v CI před nasazením.** Commit [51dde0b](https://github.com/korczis/catharsis-as-a-service/commit/51dde0bb4dba09c35fb4c0a835d764a497f3c5a3) přidal výzkumnou knihovnu. V [běhu 34842607207](https://github.com/korczis/catharsis-as-a-service/actions/runs/34842607207) selhal ve 12:17:36 UTC job `References (Crossref)` s hláškou:

```text
error: lieberman-2007: title differs from Crossref (0.42): 'putting feelings into words'
```

Citace byla správná, porovnání ne. Z chybové hlášky je vidět, že Crossref vrátil jen hlavní název, zatímco registr obsahoval celý název i s podtitulem, a validátor je porovnal tak, jak byly. Nasazení, ověření i vydání se přeskočily. Oprava [94d734c](https://github.com/korczis/catharsis-as-a-service/commit/94d734c78ffed85a02a447051992a2acac51926d) porovnává registrovaný název i jeho hlavní část s názvem z Crossrefu s podtitulem i bez něj a ponechá nejlepší shodu. Byla commitnuta ve 12:20:54 UTC a [v0.3.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.3.0) vyšla ve 12:24:28, 6 minut 52 sekund po skončení neúspěšného jobu.

**Rozdíl mezi prohlížeči, zachycený v produkci před vydáním.** Commit d2b3c47 přidal náhledy koncepčních obrazovek přímo na stránce. Všech sedm jobů CI prošlo, včetně celé prohlížečové sady na náhledu, a web se nasadil. V [běhu 34860959250](https://github.com/korczis/catharsis-as-a-service/actions/runs/34860959250) pak `Verify production` neprošel u jednoho z 84 testů, „concept screen preview: modified clicks keep the link to the original PNG“, kvůli vypršení času při čekání na novou kartu po kliknutí s klávesou Ctrl nebo Meta; opakovaný pokus Playwrightu selhal stejně. Job `Release` byl přeskočen. Navazující commit [93fd07f](https://github.com/korczis/catharsis-as-a-service/commit/93fd07f) příčinu vysvětluje: „on the Linux runner a Ctrl+click tab stayed on about:blank“. Test nyní ověřuje to, co stránka ovládá (kliknutí s modifikátorem a prostředním tlačítkem nejsou zrušena a neotevírají dialog), a ne to, jak konkrétní prohlížeč otevírá karty. Další pipeline, [běh 34863500153](https://github.com/korczis/catharsis-as-a-service/actions/runs/34863500153), prošla všemi deseti joby a [v0.6.0](https://github.com/korczis/catharsis-as-a-service/releases/tag/v0.6.0) vyšla v 15:43:36 UTC, 20 minut 12 sekund po skončení neúspěšného ověření.

U třetího případu stojí za to se zastavit. Web byl krátce živě s commitem, který neprošel ověřením, protože produkci lze testovat až po nasazení. Pravidlo, které projekt dodržuje, se týká tvrzení, ne bajtů na CDN: bez úspěšného ověřovacího jobu není vydání a nic se nehlásí jako nasazené.

## Co tyto testy nepokrývají

Žádná z těchto kontrol neposoudí, zda je věta o psychologii správná, zda je hodnocení férové nebo zda čeština zní přirozeně; to zůstává úkolem recenze a předávka z v0.5.0 uvádí revizi terminologie jako otevřenou. Sada neměří výkonnostní rozpočty a přístupnost se kontroluje přes konkrétní chování (držení fokusu, popisky, alternativní texty, pořadí nadpisů), ne úplným auditem. Pipeline má i strukturální slepé místo: chyba, která se projeví jen na GitHub Pages, se najde, až když je web živě. Zmírňuje to fakt, že ověření je automatické, běží během několika minut a nic se nevydá, dokud neprojde.
