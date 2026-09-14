+++
title = "Měří tento web moje emoce?"
description = "Ne. Čísla v uměleckém díle jsou umělecké hodnoty, web neobsahuje analytické skripty, sledovací prvky ani cookies a jeho zdrojový kód je veřejný, takže to lze ověřit, ne jen tomu věřit."
date = 2026-09-14
weight = 12

[taxonomies]
tags = ["soukromí", "umělecké dílo", "afektivní AI", "transparentnost"]

[extra]
kicker = "Otázka 12"
short_answer = "Ne. Každá metrika, stavová hodnota i graf v uměleckém díle jsou uměleckou hodnotou zvolenou k vyjádření vztahu, ne měřením kohokoli. Web neobsahuje žádné analytické skripty, sledovací prvky ani cookies, a protože je zdrojový kód veřejný, můžete si to ověřit místo toho, abyste tomu věřili. Poskytovatel hostingu může vést vlastní serverové logy, které tento projekt neovlivňuje."
related_questions = ["faq/can-emotions-be-measured/index.md", "faq/why-an-artwork/index.md", "faq/how-this-was-built/index.md"]
read_next = ["research/measuring-emotion/index.md", "artifacts/catharsis-as-a-service/index.md", "methods/index.md", "detection-sandbox/index.md"]
references = ["repository-2026", "stark-hoey-2021", "picard-1997"]
+++

## Co jsou čísla v uměleckém díle

Umělecké dílo si vypůjčuje slovník monitorovacího dashboardu: vstupní stav, synchronizace, kořenová příčina, graf, který stoupá a klesá. Nic z toho nejsou data. Všechny metriky, stavové hodnoty a grafy v uměleckém díle i obrázky úlevy jinde na webu jsou uměleckými či koncepčními hodnotami zvolenými k vyjádření vztahu. Byly navrženy tak, aby připomínaly telemetrii — právě proto všude nesou označení ARTISTIC a právě proto se nesmějí citovat jako zjištění.

Stejně funguje i simulace na stránce s metodikou: běží na vymyšlených vstupech a sama to o sobě říká. Nic na tomto webu nesnímá údaje o návštěvníkovi a nic se o něm neodvozuje.

## Co je web technicky

Je to statický web. Stránky se předem generují z Markdownu a šablon a servírují se jako soubory; na druhém konci není žádná aplikace, která by cokoli sbírala. Neobsahuje žádné analytické skripty, žádné sledovací prvky ani cookies.

Takové tvrzení je z těch, která by se neměla brát na slovo, a proto je udělané ověřitelným. Zdrojový kód je veřejný. Můžete si přečíst šablony i sestavené HTML, prohledat je na značky cizích skriptů a při načítání stránky otevřít v prohlížeči síťový panel a podívat se, na které servery se sáhne. Ověření je lepší než ujištění a tohle je ta podoba ujištění, kterou lze na ověření převést.

Jedno poctivé omezení tu je. Soubory servíruje poskytovatel hostingu a ten může v rámci provozu webového serveru vést vlastní serverové logy — časy požadavků, adresy, identifikaci prohlížeče. To je mimo kontrolu tohoto projektu a nelze to za poskytovatele slibovat.

## Proč web o emocích odmítá měřit

Rosalind Picardová vymezila afektivní informatiku jako výzkumný obor v roce 1997 a vzešla z ní seriózní práce. Vzešly z ní ale i systémy prodávané se slibem, že odvodí emoční stavy z obličejů, hlasů a fyziologických signálů. Stark a Hoey argumentují, že takové systémy stojí na sporných modelech emocí a na zástupných datech a že právě tyto volby — který model, který zástupný ukazatel — určují etické a společenské dopady toho, co vznikne. Jde o koncepční argument o celém oboru, ne o audit konkrétních produktů.

Pro tento projekt z toho plynou dva důvody. První je validita: syntézy o měření neopravňují odvozovat konkrétní emoční stav z jednoho zaznamenaného signálu, takže dashboard by tu vydával chybu za přesnost. Druhý je souhlas: kdo si čte esej o katarzi, nesouhlasil s tím, že bude analyzován, a umělecké dílo, které by to potichu dělalo, by předvádělo přesně to, co kritizuje.

Umělecké dílo si tedy ponechává rozhraní a měření zahazuje. Ručičky se hýbou proto, že tak rozhodl návrhář, a stránka to říká nahlas.
