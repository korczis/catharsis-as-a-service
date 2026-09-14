+++
title = "Jak hodnotíte sílu důkazů?"
description = "Každé podstatné tvrzení na webu má záznam v rejstříku dokladů: úroveň dokladů A až E, samostatné hodnocení jistoty, zdroje, rozsah, výhradu a datum revize. Tvrzení po datu revize shodí build."
date = 2026-09-14
weight = 16

[taxonomies]
tags = ["doklady", "metody", "ověřování"]

[extra]
kicker = "Otázka 16"
short_answer = "Každé podstatné tvrzení má záznam v rejstříku dokladů: úroveň dokladů A až E podle designu zdrojů, samostatné hodnocení jistoty HIGH, MODERATE, LOW nebo UNKNOWN a k tomu rozsah, výhradu a zdroje. Tvrzení nikdy nedostane silnější hodnocení než jeho nejlepší zdroj. Každý záznam nese datum revize a tvrzení po tomto datu shodí build, dokud ho někdo znovu neposoudí."
related_questions = ["faq/how-this-was-built/index.md", "faq/why-an-artwork/index.md", "faq/is-this-medical-advice/index.md"]
read_next = ["evidence/index.md", "methods/index.md"]
+++

## Dva kroky, dvě různé otázky

Hodnocení probíhá ve dvou krocích a každý odpovídá na jinou otázku.

Nejprve se každý zdroj hodnotí podle designu. Metaanalýza nebo systematický přehled kontrolovaných studií je **úroveň A**. Jeden či více randomizovaných nebo kontrolovaných experimentů, obvykle s krátkodobými výstupy a specifickými vzorky, je **úroveň B**. Prospektivní, longitudinální nebo kvaziexperimentální studie včetně nekontrolovaných srovnání před a po jsou **úroveň C**. Průřezové, korelační či kvalitativní studie, narativní přehledy a teoretické práce jsou **úroveň D**. Klasické a historické texty, odborné stanovisko, projektové záznamy, prohlášení o zásadách a umělecký materiál jsou **úroveň E**.

Jeden důsledek stojí za vyslovení: přehled se hodnotí podle toho, co shrnuje, ne podle slova „metaanalýza" v názvu. Metaanalýza korelačních studií se hodnotí podle designu těchto studií.

Ve druhém kroku dostane každé tvrzení úroveň dokladů, která není silnější než jeho nejsilnější zdroj, a samostatné hodnocení jistoty. Úroveň popisuje druh studií za tvrzením. Jistota popisuje, jak dobře je tvrzení v dané formulaci podloženo.

## Čtyři hodnoty jistoty

- **HIGH** — tvrzení je v dané formulaci dobře podloženo a je nepravděpodobné, že by je další výzkum obrátil.
- **MODERATE** — tvrzení je podloženo, ale výsledky jsou omezené, nesourodé, sporné nebo nebyly plně znovu ověřeny.
- **LOW** — tvrzení stojí především na teorii nebo nepřímých dokladech a s novým výzkumem se může změnit.
- **UNKNOWN** — dostupné doklady na posouzení tvrzení nestačí.

Protože jsou obě hodnocení nezávislá, rozcházejí se užitečnými způsoby. Metaanalýza s nesourodými výsledky může podpořit tvrzení úrovně A držené se střední jistotou. Dobře replikovaná korelace může být úroveň D a přesto ospravedlnit vysokou jistotu, pokud tvrzení mluví o souvislosti, a ne o příčině. Právě v této podmínce se odehrává většina redakční práce: stejná data podpírají silné tvrzení o souvislosti a slabé tvrzení o příčině.

## Co obsahuje záznam a co vyprší

Každý záznam uvádí formulaci tvrzení v obou jazycích, jeho typ, úroveň dokladů, jistotu, zdroje, rozsah, nejdůležitější výhradu, stránky, kde se objevuje, a data poslední a příští revize. Bibliografické údaje jsou vedeny zvlášť v rejstříku referencí a ověřovány proti Crossref, protože citace a úsudek o zdroji zastarávají různým tempem.

Intervaly revizí závisejí na typu tvrzení. Tvrzení o klinických hranicích se revidují nejméně každých 180 dní, empirická tvrzení každých 365 dní a teoretická, historická, technická a umělecká každých 730 dní. Automatická kontrola běží každý týden a při každé změně; tvrzení nebo zdroj po datu revize shodí build, dokud je někdo znovu neposoudí a výsledek nezapíše do záznamu změn dokladů.

Právě to dělá ze zbytku víc než slib. Zastaralé tvrzení na stránce tiše neleží — zastaví vydání webu.

## Umění se označuje, nepovyšuje

Web je vedle knihovny i uměleckým dílem, a proto rejstřík označuje výroky podle typu. Tvrzení označené ARTISTIC patří uměleckému dílu a vyjadřuje tezi; nikdy není měřením kohokoli. Tvrzení označené EMPIRICAL referuje, co studie pozorovaly, se zdroji a limity. Viditelné označení chrání obě strany: umělecké dílo může používat jazyk dashboardů, aniž by se jeho čísla četla jako data, a výzkumné poznámky si od jeho rétoriky nevypůjčí falešnou autoritu.

Pokud nějaké tvrzení působí zastarale, přehnaně nebo špatně ozdrojovaně, stránka rejstříku nese odkaz pro nahlášení.
