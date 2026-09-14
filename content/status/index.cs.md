+++
title = "Stav"
description = "Revize sestavení, verze obsahu a stav registru důkazů: tvrzení podle úrovně, jistoty a typu, nejbližší revize a kontroly, které proběhnou při každé změně."
template = "status.html"

[extra]
kicker = "Stav"
intro = "Tato stránka se generuje při každém sestavení přímo z repozitáře: z commitu, ze kterého vznikla, z registru důkazů a z plánu revizí. Jakmile tvrzení překročí datum revize, sestavení selže dřív, než může být stránka zveřejněna."
checks = [
  { name = "Obsahové standardy", text = "Povinná metadata, délka popisu, odkaz z každého zmíněného příkazu do rejstříku a kontrola zakázaných formulací, například tvrzení, že signál rozpozná emoci." },
  { name = "Registr důkazů", text = "Každý zdroj je ohodnocen, žádné tvrzení nemá vyšší úroveň než jeho nejsilnější zdroj, každá výzkumná poznámka a rada je pokryta a žádné datum revize neuplynulo." },
  { name = "Literatura", text = "Pole rejstříku a citace offline; DOI, názvy a roky proti Crossrefu v průběžné integraci a každý týden." },
  { name = "Překlady", text = "Angličtina a čeština mají stejné stránky, stejnou strukturu metadat a stejné texty rozhraní." },
  { name = "Vygenerovaný web", text = "Jeden nadpis h1 na stránku, pořadí nadpisů, alternativní texty, kanonické a hreflang odkazy, náhledy odkazů, JSON-LD, interní odkazy, kotvy a sitemap." },
  { name = "Obsahové API", text = "Deterministický export do JSON, který čtou kontraktní testy v Rustu a klient pro příkazovou řádku." },
  { name = "Testy v prohlížeči", text = "Playwright na čtyřech velikostech obrazovky a v obou jazycích, lokálně před sloučením a po každém nasazení proti živému webu." },
  { name = "Dohled", text = "Kontrola stavu Majordomu při každém commitu a kontrakt dokončení při každém push; úkol se uzavře jen tehdy, když projde jeho ověřovací příkaz." },
  { name = "Aktuálnost důkazů", text = "Plánovaný týdenní běh zopakuje kontroly registru a Crossrefu a při propadlé revizi založí issue evidence-update." },
]
+++
