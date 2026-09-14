+++
title = "Catharsis as a Service™"
description = "Festivalový plakát, který na první pohled prodává euforii a na druhý ji diagnostikuje: opakování, synchronizace, výboj, dočasná úleva."
date = 2026-09-14
weight = 1

[extra]
title_lines = ["Catharsis", "as a Service™"]
kicker = "Diagnostika lidských systémů"
subtitle = "Endpoint přechodu emočního stavu"
endpoint = "POST /v1/catharsis"
status = "200 OK"
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
+++

Festivalový plakát, který na první pohled prodává euforii a na druhý ji diagnostikuje.

Fotografie industriálního rave, brutalistní typografie a telemetrická vrstva Prismatic sdílejí jednu plochu. Dav dostane své uvolnění, systém zaloguje úspěšnou odpověď a výchozí stav zůstane přesně tam, kde byl.
