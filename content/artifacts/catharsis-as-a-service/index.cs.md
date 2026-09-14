+++
title = "Catharsis as a Service™"
description = "Vizuální studie kolektivní katarze modelované jako transakce služby: opakování, synchronizace a výboj přinášejí dočasnou úlevu, zatímco výchozí stav zůstává nezměněn."
date = 2026-09-14
weight = 1

[extra]
title_lines = ["Catharsis", "as a Service™"]
kicker = "Diagnostika lidských systémů"
subtitle = "Endpoint přechodu emočního stavu"
endpoint = "POST /v1/catharsis"
status = "200 OK"
hero_line = "úleva zaznamenána ≠ příčina vyřešena"
poster = "assets/catharsis-as-a-service.png"
poster_alt = "Plakát Catharsis as a Service: monumentální industriální rave stage v rudém světle, hustý dav a anonymní postava uprostřed pod diagnostickou telemetrií."
sidebar_left = ["Pozorovat", "Propojit", "Uvažovat", "Jednat", "Opakovat"]
sidebar_right = ["Zvědavost", "Důkazy", "Kontext", "Perspektiva", "Lepší otázky"]
raw = '''
{
  "endpoint": "/v1/catharsis",
  "method": "POST",
  "input": {
    "emotional_state": "unresolved"
  },
  "process": [
    "repetition",
    "synchronization",
    "discharge"
  ],
  "output": {
    "relief": "temporary"
  },
  "status": 200,
  "problem_solved": false
}'''

[extra.diagnostic]
label = "Přechod stavu"
heading = ["Endpoint funguje.", "Problém trvá."]
input_label = "Vstup"
input = "nevyřešený emoční stav"
process_label = "Proces"
process = ["opakování", "synchronizace", "výboj"]
output_label = "Výstup"
output = "dočasná úleva"
problem_solved = false
status_cells = [
  { label = "HTTP status", value = "200 OK", alert = false },
  { label = "Přechod stavu", value = "Dokončen", alert = false },
  { label = "Úleva", value = "Dočasná", alert = false },
  { label = "Stav problému", value = "Nevyřešeno", alert = true },
]

[extra.crowd]
label = "Dav jako systém"
heading = "Dav nevyřešený stav neřeší."
sequence = ["Jednotlivé signály", "Synchronizace", "Kolektivní oscilace", "Výboj", "Dočasná rovnováha"]
body = ["Synchronizuje ho.", "Na krátkou chvíli se z individuálního šumu stává společný rytmus."]

[extra.observability]
label = "Pozorovatelnost"
heading = "Víc dat. Míň iluzí."
disclaimer = "Konceptuální metriky. Jde o umělecké hodnoty, ne o biometrické měření. Nic na této stránce nikoho neměří."
metrics = [
  { label = "Vstupní stav", value = "nevyřešený", level = 100, alert = true },
  { label = "Koherence", value = "stoupá", level = 64, alert = false },
  { label = "Synchronizace", value = "vysoká", level = 88, alert = false },
  { label = "Amplituda", value = "vysoká", level = 94, alert = false },
  { label = "Výboj", value = "zaznamenán", level = 100, alert = false },
  { label = "Úleva", value = "dočasná", level = 36, alert = false },
  { label = "Příčina", value = "beze změny", level = 100, alert = true },
]

[extra.terminal]
label = "Endpoint"
heading = "Stejní lidé. Jiné vzorce."
command = '''$ curl -X POST /v1/catharsis \
    -d emotional_state=unresolved'''
response = '''HTTP/1.1 200 OK

{
  "relief": "temporary",
  "problem_solved": false
}'''
mantra = ["Rave.", "Uvolnění.", "Reset.", "Znovu."]
closing = ["Některé problémy se vyřešit nedají.", "Dají se jen protancovat."]

[extra.editions]
id = "poster-editions"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/catharsis-edition-en.png", title = "Anglická edice", alt = "Plakát: CATHARSIS AS A SERVICE™, emotional state transition endpoint, nad rudě zářící branou pódia a hustým davem; levý panel uvádí input, process, output a problem_solved: false; dole POST /v1/catharsis → 200 OK a umělecký panel telemetrie.", caption = "Rave. Release. Reset. Repeat." },
  { src = "assets/posters/catharsis-edition-cs.png", title = "Česká edice", alt = "Plakát: CATHARSIS AS A SERVICE™ s podtitulem Endpoint přechodu emočního stavu; průmyslové věže s promítnutou dvojicí postav nad rudě osvětleným davem a panel Diagnostika s položkami individuální signály, synchronizace, kolektivní oscilace, výboj a dočasná rovnováha.", caption = "Stejní lidé. Jiné vzorce. Víc dat. Míň iluzí." },
  { src = "assets/posters/catharsis-edition-sign.png", title = "Signální edice", alt = "Plakát: CATHARSIS červeně a AS A SERVICE™ bíle nad pódiem s emblémy trojúhelníku v kruhu a transparenty same people different patterns a more data less illusions; postava před davem zvedá obě ruce; POST /v1/catharsis → 200 OK.", caption = "Některé problémy se vyřešit nedají. Dají se jen protancovat." },
]

+++

Vizuální studie, která na první pohled předkládá kolektivní euforii a na druhý její diagnózu.

Fotografie industriálního rave, brutalistní typografie a telemetrická vrstva Prismatic sdílejí jednu plochu. Dav dostane své uvolnění, systém zaloguje úspěšnou odpověď a výchozí stav zůstane přesně tam, kde byl.

## První pohled, druhý pohled

Z druhé strany ulice je to kampaň: stage v rudém světle, moře zvednutých rukou a titulek dost velký na to, aby něco sliboval. Tohle čtení je záměrné a není to past. Noc, kterou plakát inzeruje, je skutečná, a skutečná je i úleva.

Zblízka začne plakát sepisovat hlášení. Telemetrie pojmenuje vstup, proces a výstup. Stavový řádek hlásí úspěch: `200 OK`. Pod ním jedno pole odmítá spolupracovat: `problem_solved: false`.

## Proč API

Jazykem služeb popisujeme věci, které se mají konzumovat na požádání, opakovaně a se zaručenou odpovědí. Když katarzi schováme za endpoint, zviditelní se jedna nepohodlná vlastnost: transakce může proběhnout naprosto úspěšně, aniž by byl požadavek vyřešen. Endpoint dělá přesně to, co slibuje. Jen ten slib byl menší než potřeba.

## Úleva není řešení

Artefakt netvrdí, že tanec je k ničemu nebo že kolektivní uvolnění je falešné. Opakování, synchronizace a výboj jsou stará a účinná lidská technologie. Tvrzení je užší: dočasný přechod stavu a odstraněná příčina jsou dva různé výsledky a vyplatí se umět poznat, který z nich jste dostali.

## Proč je telemetrie konceptuální

Každá metrika na této stránce je umělecká hodnota. O nikom, kdo sem přijde, se nic neměří, nesbírá ani neodvozuje, a žádný analytický skript to nepopírá. Dílo o instrumentaci lidí by nemělo potichu instrumentovat vlastní publikum.

## Jak s ním pracovat

- **Jako zrcadlo:** po příští noci, která jako by něco spravila, se zeptejte, které pole se doopravdy změnilo.
- **Jako začátek rozhovoru:** surová odpověď je dost krátká na citaci a dost konkrétní na nesouhlas.
- **Jako designová reference:** euforie a diagnóza na jedné ploše, aniž by jedna rušila druhou.
