+++
title = "Detekční pískoviště: co signály nerozhodnou"
description = "Pět umělých signálů, jedno prostředí a všechna čtení, která zároveň připouštějí. Změníte prostředí, signály zůstanou na místě a vedoucí výklad se změní — a přesně o to jde."
date = 2026-09-14
template = "sandbox.html"

[taxonomies]
tags = ["měření", "inference", "epistemologie", "simulace"]

[extra]
kicker = "Detekční pískoviště"
summary = "Funkční ukázka vzdálenosti mezi signálem a závěrem. Nastavíte pět hodnot, pískoviště z nich podle pravidel vypsaných vedle čísel odvodí čtyři veličiny a pak ukáže všechna čtení, která tyto veličiny připouštějí, seřazená i s aritmetikou, která je seřadila. Změňte prostředí z koncertu na mimořádnou událost a signály se nepohnou, zatímco vedoucí čtení ano. Nic se neměří, nezaznamenává ani neodesílá."
key_points = [
  "Vstupy jsou hodnoty, které nastavíte vy. Nic na této stránce nečte senzor a nic o vás se nepočítá, neukládá ani neodesílá.",
  "Odvozené veličiny nepřidávají poznání: každá jen jinak vyjadřuje vstupy podle pravidla, které je u ní napsané.",
  "Čtení se nikdy nevrací samo. Pískoviště vždy ukáže konkurující výklady a řekne, když vedoucí čtení není od dalšího odlišené.",
  "Tytéž signály v jiném prostředí dají jiné vedoucí čtení, protože prostředí dodává apriorní váhu, kterou senzory dodat nemohou.",
  "Váhy jsou ilustrativní. Byly zvoleny tak, aby byla vidět stavba úsudku, ne odhadnuty z nějakých dat.",
]
references = ["barrett-2019", "siegel-2018", "mauss-robinson-2009", "stark-hoey-2021", "hoemann-2020"]
assumptions = [
  "Srdeční frekvence se čte na škále 50–190 a lineárně se převádí na 0–100, aby ji bylo možné průměrovat s ostatními signály; zbylé čtyři jsou bezrozměrné škály 0–100.",
  "Vzrušení je průměr převedené srdeční frekvence, pohybu a hlasitosti; námaha je průměr převedené srdeční frekvence a pohybu; veličina synchronie je vstup sladění beze změny.",
  "Každé čtení má pevnou apriorní váhu pro dané prostředí a shodu spočtenou z odvozených veličin; zobrazený podíl je součin apriorní váhy a shody, normalizovaný přes všech pět čtení.",
  "Apriorní váhy i výrazy pro shodu jsou vymyšlené. Nesou směr — že hněv odpovídá vysokému vzrušení při nízkém sladění, že kolektivní čtení odpovídá vysokému vzrušení při vysokém sladění — a nic o velikosti.",
  "Dvě čtení, která se liší o méně než deset bodů, se hlásí jako neodlišená; ten práh je zvolený kvůli srozumitelnosti, ne odvozený z něčeho.",
]
limits = [
  "Tohle není klasifikátor a nesmí se tak používat. Řadí vymyšlené hypotézy podle vymyšlených vah, aby byla vidět stavba úsudku, ne aby určilo stav.",
  "Skutečné rozpoznávání afektu je těžší, ne snazší: pohyby obličeje nejsou napříč lidmi a kontexty spolehlivými ukazateli kategorií emocí a autonomní vzorce jednu kategorii emocí od druhé jasně neodlišují.",
  "Pět signálů je karikaturou toho, co by skutečný systém zaznamenával, a čtyři veličiny karikaturou toho, co by počítal. Bohatší systém má tentýž problém, jen méně čitelně.",
  "Nic zde neříká, co popisovaný člověk prožívá, proč to prožívá ani zda se v jeho situaci něco změnilo. To jsou otázky, na kterých záleží, a žádný signál z tohoto seznamu k nim nedosáhne.",
]

[extra.panel]
heading = "Pískoviště"
intro = "Nastavte signály, zvolte prostředí a čtěte panel zleva doprava: co jste nastavili, co z toho plyne podle pravidla, co by to mohlo znamenat a co říct nemůže."
unknown = [
  "Co člověk prožívá zevnitř; to žádná kombinace těchto signálů neobsahuje.",
  "Proč v takovém stavu je: příčina není vlastností těla a týž tělesný stav plyne i z neslučitelných příčin.",
  "Zda se v jeho situaci něco změnilo, což je otázka, o kterou jde celému tomuto webu, a právě k ní signály mlčí.",
  "Zda vůbec chce být pozorován, což je otázka souhlasu, ne měření.",
]

[extra.panel.labels]
figure = "Detekční pískoviště: pět umělých signálů, veličiny z nich odvozené, konkurující čtení, která připouštějí, a otázky, na které odpovědět nemohou."
banner = "Umělé vstupy · ilustrativní váhy · nic se neměří ani nezaznamenává"
nojs = "Pískoviště potřebuje JavaScript. Jeho pravidla jsou rozepsaná v předpokladech níže a argument, který předvádí, je v textu: tytéž signály připouštějí několik čtení a o tom, které vede, rozhoduje prostředí."
observed = "Co jste nastavili"
observed_note = "Tohle jsou hodnoty, které jste zvolili, ne údaje z přístroje. Web nic nezaznamenává a nic neodesílá."
kind_observed = "pozorováno"
kind_derived = "odvozeno"
kind_inferred = "vyvozeno"
kind_unknown = "neznámé"
context = "Prostředí"
context_concert = "Koncert"
context_protest = "Demonstrace"
context_sport = "Sportovní utkání"
context_emergency = "Mimořádná událost"
context_ritual = "Rituál"
signal_heart = "Srdeční frekvence (tepy/min)"
signal_movement = "Intenzita pohybu"
signal_vocal = "Hlasitost projevu"
signal_alignment = "Rytmické sladění s ostatními"
signal_reported = "Vlastní hodnocení aktivace"
reset = "Výchozí stav"
derived = "Co z toho plyne podle pravidla"
derived_arousal = "Index vzrušení"
derived_synchrony = "Index synchronie"
derived_effort = "Index fyzické námahy"
derived_gap = "Rozdíl tělo–výpověď"
rule_arousal = "průměr převedené srdeční frekvence, pohybu a hlasitosti"
rule_synchrony = "vstup sladění, beze změny"
rule_effort = "průměr převedené srdeční frekvence a pohybu"
rule_gap = "vzdálenost mezi indexem vzrušení a vlastním hodnocením"
inferred = "Co by to mohlo znamenat"
inferred_note = "Ukazují se všechna čtení, seřazená podle součinu apriorní váhy a shody. Podíl není pravděpodobnost, že stav nastal; je to váha tohoto modelu podle jeho vlastních vymyšlených čísel."
prior = "apriorní"
fit = "shoda"
reading_collective = "Vysoké kolektivní vzrušení"
reading_positive = "Možná pozitivní afekt"
reading_anger = "Možná hněv"
reading_fear = "Možná strach"
reading_exertion = "Fyzická námaha"
undecided = "Vedoucí čtení není odlišené od dalšího. Na těchto signálech pískoviště nerozlišuje nic."
separated = "Vedoucí čtení je před dalším, při těchto vymyšlených vahách a tomto prostředí."
alternatives = "Tytéž signály, čtené jinde"
alternatives_note = "Vstupy se nemění. Mění se jen prostředí a s ním apriorní váha, kterou senzory dodat nemohou."
unknown = "Co žádný zdejší signál nerozhodne"
vocabulary = "Šest slov použitých výše"
[extra.lenses.essential]
heading = "Co to ukazuje"
body = "Signály v sobě nenesou závěry. Panel vezme pět hodnot, které nastavíte, a ukáže zároveň všechna čtení, která připouštějí; když změníte jen prostředí, změní se vedoucí čtení. To je celý argument: totéž tělo, čtené jinde, znamená něco jiného, a senzory o tom místě nevědí nic."

[extra.lenses.practice]
heading = "Pro toho, kdo pracuje s lidmi"
body = "Nic zde nikoho neposuzuje a nic zde není screeningový nástroj. Pískoviště existuje proto, aby byly vidět meze usuzování, což je podstatné ve chvíli, kdy přístroj, aplikace nebo služba nabízí hlásit něčí emoční stav. Kde se shrnuje literatura, jde o zjištění na úrovni skupin s jeho populací a limity, a klinická hranice zůstává: tíseň, která přetrvává nebo zahrnuje myšlenky na sebepoškození, patří ke kvalifikovanému odborníkovi."

[extra.lenses.research]
heading = "Pravidla, celá"
body = "Každá odvozená hodnota je uvedenou funkcí vstupů a každý podíl je apriorní váha vynásobená shodou a normalizovaná. Apriorní váhy i shody jsou vymyšlené; nesou směr, ne velikost. Nic se neodhaduje z dat a žádný zdejší parametr nebyl k ničemu přizpůsoben."
rules = [
  { name = "Index vzrušení", rule = "průměr srdeční frekvence převedené z 50–190 na 0–100, pohybu a hlasitosti" },
  { name = "Index synchronie", rule = "vstup rytmického sladění, beze změny" },
  { name = "Index fyzické námahy", rule = "průměr převedené srdeční frekvence a pohybu" },
  { name = "Rozdíl tělo–výpověď", rule = "absolutní rozdíl mezi indexem vzrušení a vlastním hodnocením aktivace" },
  { name = "Podíl čtení", rule = "apriorní váha prostředí × shoda z odvozených veličin, normalizováno přes pět čtení" },
]

[extra.lenses.technical]
heading = "Implementace"
body = "Výpočet je čistý a deterministický: derive(signals) a hypotheses(derived, context) jsou funkce pouze svých argumentů, vystavené na window.caasSandbox, takže je test může zavolat bez stránky v prohlížeči. Alpine komponenta drží stav a ptá se jich; stav je v URL, takže nastavené pískoviště lze poslat odkazem."
model_label = "Identifikátor modelu"
implementation_label = "Implementace"
tests_label = "Testy"
state_label = "Stav v URL"

[extra.lenses.epistemic]
heading = "Jakého druhu je které číslo"
body = "Panel označuje každou svou část jedním ze šesti slov a právě ty nálepky jsou pointa. Co nastavíte, je pozorované jen v tom smyslu, že jste to zvolili. Co spočítají pravidla, je odvozené a nepřidává poznání. Co naznačují podíly, je vyvozené a může být mylné. Co nesou váhy, je ilustrativní. A nejdelší seznam na stránce je ten pod šestým slovem."

+++

## Proč pískoviště, a ne ukázka přesnosti

Systém, který hlásí emoční stav, udělal dvě oddělitelné věci: něco zaznamenal a něco usoudil. První je inženýrství, druhé je úsudek, a mezera mezi nimi je místo, kde žije skoro každé přehnané tvrzení o rozpoznávání emocí.

Tahle stránka tu mezeru rozebírá. Signály si nastavujete sami, takže se čtenáře nic netýká. Veličiny se počítají podle pravidel vypsaných vedle výstupů, takže se nic neschovává v modelu. A čtení se ukazují všechna najednou, seřazená, ale nikdy zredukovaná na jedno, protože poctivým výstupem takového úsudku je rozptyl, ne verdikt.

## Ta ukázka

Nastavte signály tak, jak by je věrohodně vyvolal koncert: vysoká srdeční frekvence, hodně pohybu, silné sladění s lidmi kolem. Přečtěte si seřazený seznam. Pak změňte jen prostředí na mimořádnou událost. Signály se nepohnuly ani o bod a vedoucí čtení se změnilo.

Na těle se nezměnilo nic. Změnila se apriorní váha, která plyne z toho, že víme, kde to tělo je, a tuhle váhu nemá k dispozici žádný senzor ze seznamu. Systém nasazený na pracovišti, ve škole nebo na stadionu dědí tentýž problém a obvykle ho skryje, protože jediná nálepka působí jako odpověď, kdežto seřazený rozptyl jako přiznání.

## Co o skutečné verzi říká výzkum

Pískoviště je karikatura a zjištění pod ní nejsou k detekci vlídnější než ta karikatura. Rozsáhlý přehled dospěl k závěru, že pohyby obličeje nejsou napříč lidmi a kontexty spolehlivými a specifickými ukazateli emočních stavů (Barrett a kol., 2019). Metaanalýza 202 studií zjistila, že autonomní odpovědi jednu kategorii emocí od druhé jasně neodlišovaly (Siegel a kol., 2018). A není kam ustoupit: neexistuje zlatý standard měření, prožitková, fyziologická a behaviorální měřítka se shodují jen mírně a nelze je považovat za zaměnitelná (Mauss a Robinson, 2009).

Systémy postavené na těchto signálech tedy stojí na konkrétních koncepčních modelech emocí a na zástupných datech a tyto volby určují, co systémy o lidech naznačují (Stark a Hoey, 2021). Když se opakované fyziologické vzorkování dělá pečlivě v každodenním životě, vzorce, které se u jednoho člověka opakují, se liší počtem i nálepkami, které k nim patří (Hoemannová a kol., 2020).

## Co si z toho odnést

Úsudek může být poctivý ve třech věcech naráz: co viděl, co spočítal a co pořád neví. Pískoviště vypisuje všechny tři a třetí seznam je nejdelší. To není selhání ukázky. To je její výsledek.
