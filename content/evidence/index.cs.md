+++
title = "Registr důkazů"
description = "Každé veřejné tvrzení tohoto webu s typem, úrovní důkazů, mírou jistoty, zdroji a datem revize a hodnocení každého zdroje. Jak se tvrzení hodnotí, jak se odděluje umění od důkazů a jak nahlásit problém."
date = 2026-09-14
template = "evidence.html"

[taxonomies]
tags = ["důkazy", "metody", "ověřování"]

[extra]
kicker = "Důkazy"
summary = "Registr důkazů uvádí každé podstatné tvrzení, které tento web činí, od zjištění na úvodní stránce po rady a umělecké dílo, spolu se zdroji, o které se opírá. Každý zdroj je hodnocen podle designu a zařazen do úrovní A až E; tvrzení nikdy nesmí mít vyšší úroveň než jeho nejsilnější zdroj. Míra jistoty je samostatný úsudek o tom, jak dobře je tvrzení v dané formulaci podložené. Každé tvrzení má datum revize a tvrzení po tomto datu zastaví sestavení webu, dokud není znovu posouzeno."
levels = [
  { level = "A", name = "Systematická syntéza", text = "Metaanalýza nebo systematický přehled kontrolovaných studií. Syntézy korelačních studií se hodnotí podle designu studií, které shrnují." },
  { level = "B", name = "Kontrolovaný experiment", text = "Jeden nebo více randomizovaných či kontrolovaných experimentů, obvykle s krátkodobými výsledky a specifickými vzorky." },
  { level = "C", name = "Longitudinální nebo kvaziexperimentální", text = "Prospektivní, longitudinální nebo kvaziexperimentální studie včetně nekontrolovaných srovnání před a po." },
  { level = "D", name = "Korelační, kvalitativní nebo teoretické", text = "Průřezové, korelační nebo kvalitativní studie, narativní přehledy a teoretické práce." },
  { level = "E", name = "Klasické, expertní nebo záznamy", text = "Klasické a historické texty, expertní názor, projektové záznamy, zásady a umělecký materiál." },
]
confidence = [
  { value = "HIGH", text = "Tvrzení je v dané formulaci dobře podložené a další výzkum jej pravděpodobně nezvrátí." },
  { value = "MODERATE", text = "Tvrzení je podložené, ale výsledky jsou omezené, heterogenní, sporné nebo nebyly plně znovu ověřeny." },
  { value = "LOW", text = "Tvrzení stojí hlavně na teorii nebo nepřímých dokladech a nový výzkum je může změnit." },
  { value = "UNKNOWN", text = "Dostupné doklady nestačí k posouzení tvrzení." },
]
claim_types = [
  { id = "empirical", name = "Empirické", text = "Výpověď o tom, co studie pozorovaly. Revize nejméně jednou za 365 dní." },
  { id = "theoretical", name = "Teoretické", text = "Definice, rámec nebo argument, který zjištění uspořádává, aniž by sám byl jedním zjištěním. Revize jednou za 730 dní." },
  { id = "historical", name = "Historické", text = "Výpověď o dějinách myšlenky nebo praxe. Revize jednou za 730 dní." },
  { id = "clinical-boundary", name = "Klinická hranice", text = "Výpověď o hranicích svépomoci a o tom, kdy je potřeba odborná pomoc. Revize jednou za 180 dní." },
  { id = "technical", name = "Technické", text = "Výpověď o fungování webu nebo metody měření podložená záznamy nebo metodologickou literaturou. Revize jednou za 730 dní." },
  { id = "artistic", name = "Umělecké", text = "Výpověď, která patří uměleckému dílu. Vyjadřuje tezi a není zjištěním. Revize jednou za 730 dní." },
]
review_policy = "Tvrzení o klinických hranicích se revidují nejméně jednou za 180 dní, empirická tvrzení jednou za 365 dní a teoretická, historická, technická a umělecká tvrzení jednou za 730 dní. Automatická kontrola běží každý týden a při každé změně; tvrzení nebo zdroj po datu revize zastaví sestavení webu, dokud je někdo znovu neposoudí a výsledek nezaznamená do changelogu důkazů."
report_label = "Nahlásit zastaralé nebo nesprávné tvrzení"

[extra.poster_figure]
id = "poster-evidence"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/vice-dat-lepsi-rozhodnuti.png", title = "Více dat. Méně iluzí. Lepší rozhodnutí.", alt = "Plakát: VÍCE DAT. MÉNĚ ILUZÍ. LEPŠÍ ROZHODNUTÍ. Člověk sedí u stolu s monitory před stěnou propojených fotografií a poznámek, vedle knih s nápisy evidence, context, perspective, truth a better questions; otevřenými dveřmi je vidět postavu mířící do rudých hor.", caption = "Stejná fakta, víc perspektiv, méně manipulace." },
]

+++

## Proč registr

Web, který tvrdí, že úleva není vyřešení, musí na vlastní výroky uplatňovat stejné měřítko. Napsat „výzkum ukazuje“ je snadné; mnohem těžší je říct, který výzkum, jakého designu, s jakými limity a kdy to naposledy někdo ověřil. Registr na tyto otázky odpovídá na jednom místě.

Každé podstatné veřejné tvrzení webu v něm má záznam: čtyři zjištění na úvodní stránce, odpovědi na časté otázky, klíčové body každé výzkumné poznámky, doporučení každé rady, výpovědi uměleckého díla i technická tvrzení o samotném webu. Každý záznam uvádí znění tvrzení, jeho typ, úroveň důkazů, míru jistoty, zdroje, rozsah platnosti, nejdůležitější výhradu, stránky, kde se objevuje, a data poslední a příští revize.

Bibliografická fakta a úsudek jsou oddělené. Registr referencí obsahuje názvy, autory a DOI ověřené v Crossrefu. Registr důkazů obsahuje hodnocení každého zdroje včetně designu, zkoumané populace a hlavního omezení a toto hodnocení je datované, protože úsudek může zastarat, i když citace nezastará.

## Jak se tvrzení hodnotí

Hodnocení probíhá ve dvou krocích.

Nejprve se každý zdroj zařadí podle designu. Metaanalýza randomizovaných studií má úroveň A, jediný kontrolovaný experiment úroveň B, longitudinální nebo nekontrolovaná studie před a po úroveň C, korelační, kvalitativní, narativně přehledové a teoretické práce úroveň D a klasické texty, projektové záznamy a umělecký materiál úroveň E. Metaanalýza, která shrnuje korelační studie, se hodnotí podle toho, co shrnuje, nikoli podle slova „metaanalýza“ v názvu.

Poté každé tvrzení dostane úroveň důkazů, která není vyšší než úroveň jeho nejsilnějšího zdroje, a samostatné hodnocení míry jistoty. Obě veličiny odpovídají na jiné otázky. Úroveň popisuje druh studie, o kterou se tvrzení opírá. Míra jistoty popisuje, jak dobře je tvrzení v dané formulaci podložené. Metaanalýza s heterogenními výsledky může podpořit tvrzení úrovně A se střední mírou jistoty. Dobře replikovaná korelace může mít úroveň D, a přesto opravňovat k vysoké jistotě, pokud tvrzení mluví o souvislosti, a ne o příčině.

Pokud nebylo možné získat abstrakt zdroje, registr to uvádí, neuvádí u něj velikost vzorku a snižuje míru jistoty tvrzení, která se o něj opírají. Pokud formulace na stránce zašla dál než její zdroje, registr zaznamená přísnější verzi a changelog revizi popíše.

## Úleva, vyřešení a hranice důkazů

Většina zde citovaného výzkumu měří krátkodobé výsledky ve specifických vzorcích: hněv několik minut po provokaci, blízkost po tanci, náladu po filmu. Takové doklady se hodí k otázkám o úlevě. K otázkám o vyřešení, které se odehrává během měsíců a v podmínkách, jež žádná laboratoř nenapodobí, se hodí mnohem méně. Když registr uvádí, že doklady nestačí, jde o zjištění o stavu literatury, nikoli o verdikt nad samotným zážitkem.

## Umění a důkazy na jednom webu

Web je zároveň uměleckým dílem i knihovnou a obě části používají odlišné druhy výpovědí. Registr je výslovně označuje. Tvrzení označené jako UMĚLECKÉ patří dílu: hodnoty telemetrie, stavový řádek a pole `problem_solved: false` vyjadřují tezi a nikdy nejsou měřením kohokoli. Tvrzení označené jako EMPIRICKÉ uvádí, co studie pozorovaly, se zdroji a limity. Teoretická, historická, technická a klinicky hraniční tvrzení leží mezi nimi a jsou rovněž označena.

Viditelné označení chrání obě strany. Dílo může používat jazyk dashboardů, aniž by se jeho čísla citovala jako data, a výzkumné poznámky lze číst, aniž by jim rétorika díla propůjčovala falešnou autoritu.

## Jak nahlásit problém

Pokud se vám tvrzení zdá zastaralé, nadsazené nebo špatně podložené, použijte odkaz pro nahlášení na této stránce. Užitečné hlášení uvádí tvrzení, vysvětluje, co je na něm špatně, a pokud možno cituje novější nebo lepší zdroj. Hlášení se ověřují podle původních publikací. Potvrzený problém vede k revizi, snížení hodnocení nebo stažení tvrzení a změna se zaznamená do changelogu důkazů s datem a důvodem.

Obsah tohoto webu je obecnou osvětou, nikoli lékařskou radou. Pokud distres přetrvává, narušuje každodenní život nebo zahrnuje myšlenky na sebepoškození, obraťte se na kvalifikovaného odborníka nebo na místní tísňové služby.
