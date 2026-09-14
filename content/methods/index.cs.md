+++
title = "Metody: signály, inference a meze rozpoznání změny stavu"
description = "Jak lze uvažovat o zachycení změny stavu podobné katarzi: signály, příznaky, inference a kontext, výchozí hodnoty, sebevýpověď, cena chyb a etika, a proč každý krok zůstává nejistý. Nic na tomto webu nikoho neměří."
date = 2026-09-14
template = "methods.html"

[taxonomies]
tags = ["metody", "měření", "fyziologie", "nejistota", "etika"]

[extra]
kicker = "Metody"
summary = "Změna stavu člověka zanechává stopy v srdeční frekvenci, kožní vodivosti, pohybu, hlasu i sebevýpovědi, žádná z těchto stop však neurčuje, co člověk prožívá ani proč. Tato stránka sleduje řetězec od surového signálu k interpretaci, ukazuje, kde v jednotlivých krocích vzniká chyba, a vysvětluje, proč kombinace signálů neodstraní základní nejednoznačnost. Odděluje to, co zaznamená senzor, od toho, k čemu dospěje člověk nebo model, a popisuje slovník, který by poctivý systém potřeboval. Web nesbírá žádná fyziologická data a interaktivní model pracuje s vymyšlenými vstupy."
key_points = [
  "Každý závěr o emočním stavu prochází čtyřmi kroky, signálem, příznakem, inferencí a kontextem, a každý z nich přidává vlastní chybu.",
  "Metaanalýza 202 laboratorních studií zjistila, že autonomní reakce jednotlivé kategorie emocí jasně neodlišují (Siegel a kol., 2018), a ani pohyby obličeje nejsou spolehlivými a specifickými ukazateli (Barrett a kol., 2019).",
  "Sebevýpověď je nepostradatelná, ale závisí na tom, kdy je získána: zpětnému hodnocení dominují nejhorší a závěrečné okamžiky (Kahneman a kol., 1993), což se momentové vzorkování snaží omezit (Shiffman a kol., 2008).",
  "Signály mohou být nanejvýš v souladu se změnou stavu. Zda se změnily podmínky, které tíseň vyvolaly, neměří, a proto endpoint uměleckého díla odpovídá problem_solved: false.",
]
references = ["siegel-2018", "kreibig-2010", "barrett-2019", "poldrack-2006", "laborde-2017", "boucsein-2012", "robinson-clore-2002", "fredrickson-kahneman-1993", "kahneman-1993", "shiffman-2008", "kuppens-verduyn-2017", "wiltermuth-heath-2009", "tarr-2015", "kjaervik-bushman-2024", "picard-1997", "stark-hoey-2021"]

[[extra.detection_chain]]
id = "signal"
name = "Signál"
text = "Signál je to, co zaznamená přístroj: fyzikální veličina vzorkovaná v čase, bez jakéhokoli psychologického významu. Jeho průběh závisí na zařízení, jeho umístění, vzorkovací frekvenci a prostředí stejně jako na člověku."
example = "Surová kožní vodivost v mikrosiemensech vzorkovaná 32krát za sekundu senzorem na zápěstí nebo tříosý záznam akcelerometru."
risk = "Zde vznikají artefakty: uvolněná elektroda, pocení z horka, pohyb nebo vypadlé vzorky mohou vytvořit záznam, který vypadá jako fyziologická reakce, ale není jí."

[[extra.detection_chain]]
id = "feature"
name = "Příznak"
text = "Příznak je číslo vypočtené ze signálu, které ho shrnuje, například průměr, četnost událostí nebo index variability. Volba příznaku, časového okna, filtru a korekce artefaktů je už sama modelovým rozhodnutím."
example = "Počet kožních vodivostních reakcí za minutu nad zvolenou amplitudovou hranicí nebo RMSSD, index variability srdeční frekvence, vypočtený z pěti minut intervalů mezi údery."
risk = "Prahy, délka okna a pravidla korekce mění výslednou hodnotu; dva rozumné postupy zpracování mohou ze stejného záznamu dát různé příznaky."

[[extra.detection_chain]]
id = "inference"
name = "Inference"
text = "Inference převádí příznaky na popis člověka, například zvýšený arousal nebo pravděpodobnou fázi epizody. V tomto kroku se měření mění v interpretaci, ať ji provádí statistický model, nebo lidský pozorovatel."
example = "Model dospěje k závěru, že současný vzestup srdeční frekvence a četnosti kožních vodivostních reakcí je v souladu se zvýšenou fyziologickou aktivací."
risk = "Obrácená inference: vzorec, který stav často provází, je brán jako doklad tohoto stavu, přestože stejný vzorec provází i mnoho jiných stavů a činností."

[[extra.detection_chain]]
id = "context"
name = "Kontext"
text = "Kontext je vše ostatní, co je o situaci známo: co člověk dělá, kde, s kým, co se stalo předtím a co o tom sám říká. Bez něj zůstává většina závěrů z tělesných signálů nedourčená."
example = "Stejný vzestup srdeční frekvence zaznamenaný při chůzi do schodů, během hádky nebo na koncertě, když hudba graduje."
risk = "Kontext může chybět, být chybný nebo sám odvozený; model, který kontext odhaduje ze stejných signálů, nejistotu jen přesouvá, místo aby ji snižoval."

[[extra.temporal_model]]
id = "baseline"
name = "Výchozí stav"
text = "Obvyklé rozpětí hodnot daného člověka pro určitou denní dobu, polohu těla a situaci, vůči kterému se posuzuje každá změna."
observable = "Klidová srdeční frekvence a variabilita srdeční frekvence z opakovaných záznamů, typická úroveň kožní vodivosti, obvyklý pohyb, výchozí sebevýpověď."
caution = "I výchozí stav kolísá. Spánek, kofein, nemoc, léky, teplota a očekávání měření ho posouvají, takže jeden krátký záznam nemusí být reprezentativní."

[[extra.temporal_model]]
id = "activation"
name = "Aktivace"
text = "Odklon od výchozího stavu směrem k vyšší fyziologické aktivitě a bdělosti."
observable = "Rostoucí srdeční frekvence, častější kožní vodivostní reakce, rychlejší dech, více pohybu, výpovědi o napětí nebo vzrušení."
caution = "Aktivace není specifická: pohyb, strach, nadšení, hněv, horko i stimulanty vytvářejí překrývající se vzorce."

[[extra.temporal_model]]
id = "synchronization"
name = "Synchronizace"
text = "Ve sdílených situacích se pohyb a pozornost jednotlivců sladí se společným rytmem a s ostatními lidmi."
observable = "Korelovaný pohyb mezi lidmi, kroky nebo tleskání strhávané rytmem, společné zaměření, výpovědi o pocitu sounáležitosti se skupinou."
caution = "Sdílený pohyb může odrážet hudbu, choreografii, hustotu davu nebo konformitu. V experimentech je spojen se spoluprací a sbližováním, neukazuje však, co prožívá každý jednotlivec."

[[extra.temporal_model]]
id = "peak"
name = "Vrchol"
text = "Okamžik nejvyšší intenzity v rámci epizody."
observable = "Maximální srdeční frekvence nebo intenzita pohybu, shluk kožních vodivostních reakcí, hlasité projevy, momentové hodnocení nejvyšší intenzity."
caution = "Fyziologický, behaviorální a prožitý vrchol nemusí časově splývat a vrchol lze určit až poté, co hodnoty klesnou; vzpomínka na vrchol se navíc utváří až později při vybavování."

[[extra.temporal_model]]
id = "discharge"
name = "Vybití"
text = "Rychlý pokles intenzity po vrcholu, často prožívaný jako uvolnění."
observable = "Klesající srdeční frekvence, pomalejší dech, méně pohybu, smích nebo pláč, výpovědi o úlevě."
caution = "Klesající signál je v souladu s uvolněním, ale také s vyčerpáním, koncem hudby nebo prostě s tím, že si člověk sedl. Popisuje tělesnou aktivitu, ne to, co se uvolnilo, ani zda se něco vyřešilo."

[[extra.temporal_model]]
id = "recovery"
name = "Zotavení"
text = "Návrat k výchozímu stavu v řádu minut až hodin."
observable = "Srdeční frekvence a variabilita srdeční frekvence se blíží klidovým hodnotám, úroveň kožní vodivosti klesá, výpovědi o klidu nebo únavě."
caution = "Rychlost zotavení závisí na kondici, únavě, alkoholu, spánku a teplotě stejně jako na emočních procesech; rychlý návrat k výchozímu stavu není ukazatelem psychologického vyřešení."

[[extra.temporal_model]]
id = "post-state"
name = "Stav po epizodě"
text = "Stav po skončení epizody, včetně toho, zda původní potíž trvá."
observable = "Pozdější sebevýpověď, chování v následujících dnech, návrat stejné tísně, změny v situaci, do které se člověk vrací."
caution = "Pro vyřešení je tato fáze nejdůležitější a senzorům nejméně přístupná. Zda se změnily podmínky, které tíseň způsobily, žádný signál na této stránce neměří."

[extra.detection_matrix]
caption = "Co zaznamenává deset druhů údajů, s čím jsou jejich vzorce v souladu a co žádný z nich sám o sobě nemůže prokázat."
columns = { signal = "Signál", records = "Co se zaznamenává", consistent_with = "Je v souladu s", cannot_establish = "Nemůže prokázat", confounds = "Časté matoucí vlivy" }

[[extra.detection_matrix.rows]]
signal = "Srdeční frekvence"
records = "Počet úderů za minutu z elektrokardiogramu nebo optického senzoru na zápěstí."
consistent_with = "Změnami fyziologické aktivace, fyzické námahy nebo polohy těla."
cannot_establish = "Která emoce, pokud vůbec nějaká, je přítomna, ani zda je změna příjemná, nebo nepříjemná."
confounds = "Pohyb, vstávání, kofein, nikotin, alkohol, horko, horečka, léky, dehydratace, chyby optického senzoru při pohybu."

[[extra.detection_matrix.rows]]
signal = "Variabilita srdeční frekvence"
records = "Kolísání intervalů mezi po sobě jdoucími údery srdce, shrnuté indexy v časové nebo frekvenční oblasti."
consistent_with = "Změnami vagového (parasympatického) vlivu na srdce."
cannot_establish = "Konkrétní emoční stav ani schopnost člověka regulovat se na základě jednoho krátkého záznamu."
confounds = "Frekvence a hloubka dechu, poloha těla, fyzická aktivita, věk, kondice, délka záznamu, nepravidelné údery, volba korekce artefaktů."

[[extra.detection_matrix.rows]]
signal = "Elektrodermální aktivita"
records = "Změny elektrické vodivosti kůže dané činností potních žláz, jako pomalá úroveň a rychlé reakce."
consistent_with = "Sympatickou aktivací, orientací na něco nového nebo významného."
cannot_establish = "Zda je aktivace pozitivní, nebo negativní, ani k čemu se vztahuje."
confounds = "Okolní teplota a vlhkost, námaha, umístění a kontakt elektrod, velké rozdíly mezi lidmi, habituace na opakované podněty."

[[extra.detection_matrix.rows]]
signal = "Dýchání"
records = "Frekvence, hloubka a pravidelnost dechu z hrudního pásu nebo nosního senzoru, případně odhadnuté z jiných signálů."
consistent_with = "Změnami arousalu nebo námahy, mluvením, smíchem či pláčem."
cannot_establish = "Význam změny, protože zpěv, řeč i námaha mění dech přímo."
confounds = "Mluvení, zpěv, fyzická aktivita, poloha těla, vědomé ovládání dechu, onemocnění dýchacích cest."

[[extra.detection_matrix.rows]]
signal = "Pohyb a akcelerometrie"
records = "Zrychlení části těla, na které je senzor, z něhož se počítá intenzita aktivity a načasování kroků či dob."
consistent_with = "Úrovní fyzické aktivity, tancem, neklidem."
cannot_establish = "Proč se člověk hýbe; rozrušení i radost mohou vytvořit podobné záznamy."
confounds = "Umístění senzoru, jízda dopravními prostředky, strkání v davu, přecházení mezi místy."

[[extra.detection_matrix.rows]]
signal = "Synchronie pohybu mezi lidmi"
records = "Míra, do jaké jsou časové řady pohybu dvou či více lidí korelované nebo fázově sladěné."
consistent_with = "Sdíleným rytmem a koordinovanou činností, tedy podmínkami, které jsou v experimentech spojeny se sbližováním a spoluprací."
cannot_establish = "Že lidé prožívají totéž, cítí se si blízcí nebo prožívají cokoli konkrétního."
confounds = "Společný vnější rytmus, choreografie, omezení v davu, napodobování, nastavení okna a zpoždění v analýze."

[[extra.detection_matrix.rows]]
signal = "Prozodie hlasu"
records = "Výška, hlasitost, tempo řeči a kvalita hlasu v nahrané řeči."
consistent_with = "Změnami hlasového úsilí a arousalu nebo stylu mluvy."
cannot_establish = "Konkrétní emoci; prozodie nese také jazyk, nářečí, ironii, zdvořilost a zdravotní stav."
confounds = "Hluk v pozadí, vzdálenost mikrofonu, jazyk a přízvuk, nachlazení, únava, překřikování hudby."

[[extra.detection_matrix.rows]]
signal = "Pohyby obličeje"
records = "Polohy a pohyby obličejových svalů z videa, kódované lidmi nebo softwarem."
consistent_with = "Komunikačními projevy, pozorností, námahou a některými případy emocí."
cannot_establish = "Konkrétní vnitřní stav; podobné konfigurace provázejí různé emoce a často sdělují něco jiného než emoci (Barrett a kol., 2019)."
confounds = "Osvětlení, úhel hlavy, brýle, roušky, kultura, společenské normy projevu, mluvení, žvýkání, přimhouření očí v ostrém světle."

[[extra.detection_matrix.rows]]
signal = "Sebevýpověď (momentová)"
records = "Odpověď člověka, daná v danou chvíli, na otázky o tom, jak se cítí."
consistent_with = "Aktuálním popisem prožitku z pohledu člověka, v kategoriích, které otázka nabízí."
cannot_establish = "Fyziologický stav ani fakta o situaci; výpověď je popis, nikoli nezávislé ověření příčiny."
confounds = "Formulace otázky, hodnoticí škály, sociální žádoucnost, vliv samotného dotazování, neochota se svěřit, dostupná slova pro pocity."

[[extra.detection_matrix.rows]]
signal = "Kontextové záznamy (čas, místo, činnost)"
records = "Čas, poloha, činnost, společnost a události zaznamenané člověkem nebo systémem."
consistent_with = "Věrohodnými vysvětleními změny signálů, například cvičením nebo plánovaným vystoupením."
cannot_establish = "Jak člověk situaci prožíval ani zda je pro něj situace problémem."
confounds = "Chybějící nebo nepřesné záznamy, činnost odvozená místo nahlášené, ochrana soukromí, která oprávněně omezuje, co se zaznamenává."

[[extra.uncertainty]]
term = "je v souladu s"
meaning = "Používá se, když pozorování odpovídá určité interpretaci, ale odpovídalo by i jiným. Neznamená, že je tato interpretace nejpravděpodobnější."

[[extra.uncertainty]]
term = "je spojeno s"
meaning = "Používá se pro statistický vztah zjištěný napříč lidmi nebo situacemi. Neznamená příčinnost ani to, že vztah platí pro konkrétního jednotlivce."

[[extra.uncertainty]]
term = "naznačuje"
meaning = "Používá se, když několik nezávislých pozorování ukazuje stejným směrem a alternativy byly zváženy. Je slabší než závěr a mělo by uvádět, co by ho změnilo."

[[extra.uncertainty]]
term = "odvozeno s nízkou jistotou"
meaning = "Používá se pro výstup modelu, který stojí na předpokladech v dané situaci neověřených, například na neznámé výchozí hodnotě nebo chybějícím kontextu. Dává najevo, že by výstup neměl řídit rozhodnutí o člověku."

[[extra.uncertainty]]
term = "nedostatek důkazů"
meaning = "Používá se, když dostupná data nedokážou rozlišit mezi interpretacemi. Není to doklad toho, že stav chybí."

[[extra.uncertainty]]
term = "neměřeno"
meaning = "Používá se, když se otázkou nezabývá žádný signál v systému. Brání tomu, aby bylo mlčení vykládáno jako negativní výsledek."

[[extra.uncertainty]]
term = "neznámé"
meaning = "Používá se, když je hodnota vyžadována, například v odpovědi API, ale pro její vyplnění neexistuje platný podklad. Je lepší než výchozí hodnota, která vypadá jako data."

[[extra.uncertainty]]
term = "je v rozporu s"
meaning = "Používá se, když je některý zdroj v rozporu s interpretací, například když člověk uvádí klid, zatímco model odvozuje tíseň. Mělo by vést k přezkoumání modelu dříve, než padne jakýkoli závěr o člověku."

[extra.errors]
false_positive = { name = "Falešně pozitivní výsledek", text = "Systém ohlásí stav, který přítomen není, například označí člověka za v tísni nebo za zotaveného, i když takový není.", example = "Srdeční frekvence a kožní vodivost stoupnou, když někdo běží na vlak, a model epizodu označí za akutní tíseň.", cost = "Nevyžádaná pozornost nebo zásah, stigmatizace a ztráta důvěry; v institucích důsledky pro člověka kvůli stavu, který nikdy neměl." }
false_negative = { name = "Falešně negativní výsledek", text = "Systém neohlásí stav, který přítomen je.", example = "Člověk ve vážné tísni sedí nehybně a dýchá pomalu, jeho signály zůstávají blízko výchozí hodnoty a model hlásí, že se nic nezměnilo.", cost = "Přehlédnutá potřeba podpory a falešné uklidnění, zvlášť když výstup slouží k rozhodnutí, že se nikdo nemusí ptát." }

[[extra.architecture]]
component = "Statická publikace"
role = "Generuje dvojjazyčný web z Markdownu a šablon."
status = "implemented"
note = "Stránky jsou prosté soubory; o čtenáři se nic nepočítá."

[[extra.architecture]]
component = "Registr referencí s kontrolou v Crossrefu"
role = "Přiřazuje každou citaci jednomu záznamu s bibliografickými metadaty."
status = "implemented"
note = "Kontrola potvrzuje metadata, ne to, že tvrzení svůj zdroj věrně vystihuje; to zůstává redakčním úkolem."

[[extra.architecture]]
component = "Evidenční přehled s daty revizí"
role = "Zaznamenává, na kterých zdrojích která tvrzení stojí a kdy byla naposledy přezkoumána."
status = "implemented"
note = "Datum revize ukazuje, kdy bylo tvrzení ověřeno, ne že zůstane platné."

[[extra.architecture]]
component = "Verzované obsahové API"
role = "Zveřejňuje obsah webu jako verzované strojově čitelné soubory."
status = "implemented"
note = "Poskytuje pouze obsah a nepřijímá žádná osobní ani fyziologická data."

[[extra.architecture]]
component = "Klientská knihovna a CLI v Rustu"
role = "Čtou zveřejněný obsah a API z kódu nebo z terminálu."
status = "implemented"
note = "Využívají to, co web zveřejňuje, a nemají žádnou měřicí funkci."

[[extra.architecture]]
component = "Simulace detekčního modelu v prohlížeči"
role = "Ukazuje, jak by poctivý detekční model formuloval výstup pro vymyšlené vstupy."
status = "simulation"
note = "Běží celá ve stránce s hodnotami posuvníků, které nastaví návštěvník; nic se neodesílá, neukládá ani nepochází od skutečného člověka."

[[extra.architecture]]
component = "Kontextový modul kombinující signály se sebevýpovědí a situací"
role = "Poměřoval by signály s vlastní výpovědí člověka, situací a jeho historií."
status = "conceptual"
note = "Popsán na této stránce, aby bylo vidět, co by poctivá inference vyžadovala; není postaven a neexistuje žádný tok dat, který by ho mohl napájet."

[[extra.architecture]]
component = "Příjem fyziologických signálů"
role = "Přijímal by data z nositelných zařízení nebo jiných senzorů."
status = "not-planned"
note = "Záměrně vyloučeno: umělecké dílo je o instrumentaci a své publikum neinstrumentuje."

[[extra.architecture]]
component = "Individuální odvozování emocí nebo profilování"
role = "Přiřazoval by emoční stavy nebo rysy identifikovatelným lidem."
status = "not-planned"
note = "Vyloučeno z důvodu validity a souhlasu."

[[extra.architecture]]
component = "Analytika nebo sledování návštěvníků"
role = "Zaznamenávala by návštěvy, chování nebo identitu čtenářů."
status = "not-planned"
note = "Web nepoužívá žádnou analytiku, trackery ani cookies."

[extra.simulation]
banner = "Simulace · nejde o biometrickou analýzu"
heading = "Vyzkoušejte detekční model s vymyšlenými vstupy"
intro = "Posuvníky obsahují vymyšlené hodnoty, nikoli údaje z jakéhokoli zařízení, a nic z toho, co nastavíte, se nezaznamenává ani nikam neodesílá. Model na tyto hodnoty uplatní úvahy z této stránky a ukáže, jak by poctivý systém formuloval svůj závěr, včetně toho, co vědět nemůže."
inputs_label = "Vymyšlené vstupy"
output_label = "Výstup modelu"
reset = "Obnovit"
inputs = [
  { id = "heart_rate", label = "Změna srdeční frekvence oproti osobní výchozí hodnotě", unit = "tep/min", min = -10, max = 60, step = 1, value = 22 },
  { id = "eda", label = "Kožní vodivostní reakce za minutu", unit = "/min", min = 0, max = 20, step = 1, value = 8 },
  { id = "synchrony", label = "Synchronie pohybu s lidmi v okolí", unit = "%", min = 0, max = 100, step = 5, value = 70 },
  { id = "relief", label = "Úleva podle sebevýpovědi", unit = "/10", min = 0, max = 10, step = 1, value = 7 },
]
cause_label = "Člověk uvádí, že se příčina jeho tísně změnila"
out_activation = "Fyziologická aktivace"
levels = { low = "nízká", moderate = "střední", high = "vysoká" }
activation_note = "Aktivace není specifická: pohyb, nadšení, strach, hněv i horko tyto signály zvyšují."
out_phase = "Fáze, se kterou jsou vstupy nejvíce v souladu"
phases = { baseline = "Výchozí stav", activation = "Aktivace", peak = "Vrchol", discharge = "Vybití", recovery = "Zotavení" }
out_synchrony = "Sdílený pohyb"
synchrony_values = { low = "málo sdíleného pohybu", high = "silný sdílený pohyb" }
out_relief = "Úleva"
relief_values = { reported = "uvedena", not_reported = "neuvedena" }
out_cause = "Příčina vyřešena"
cause_values = { unknown = "neznámé: z těchto signálů nelze změřit", reported = "uvádí to člověk, neověřeno" }
out_confidence = "Jistota"
confidence_value = "NÍZKÁ"
confidence_note = "Bez ověřené osobní výchozí hodnoty, kontextu a opakovaných pozorování nemůže závěr o jednom člověku ze čtyř signálů přesáhnout nízkou jistotu."
problem_line = "problem_solved"
problem_values = { unknown = "unknown", false = "false" }

[extra.poster_figure]
id = "poster-methods"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/emoce-jsou-data.png", title = "Emoce jsou data", alt = "Plakát: EMOCE JSOU DATA. nad detailem tváře se zavřenýma očima, po níž stéká rudé světlo, a nad davem u zářící brány pódia; boční panely opakují vstup, proces a výstup díla a ukazují umělecký panel telemetrie.", caption = "Umělecký slogan, ne metoda: tato stránka vysvětluje, proč signály neukazují, co člověk cítí." },
]

+++

## Proč tato stránka existuje

Umělecké dílo na tomto webu představuje kolektivní katarzi jako službu i s telemetrií: vstupní stav, synchronizace, vybití, úleva. Jeho endpoint odpovídá `200 OK` s hodnotou `problem_solved: false`. Telemetrie je konceptuální. Žádné číslo na plakátu ani v dashboardu nebylo naměřeno na člověku a [Výzkumná poznámka 05](@/research/measuring-emotion/index.cs.md) vysvětluje, proč dílo odmítá své publikum měřit.

Toto odmítnutí vyvolává oprávněnou otázku. Kdyby někdo skutečně chtěl zjistit, zda proběhla změna stavu podobná katarzi, ať v davu na koncertě, na terapeutickém sezení, nebo v laboratoři, co by skutečné měření dokázalo podložit? Tato stránka na ni odpovídá tak pečlivě, jak to důkazy dovolují. Popisuje, jak by se signály z těla a ze sebevýpovědi daly převést na tvrzení o změně stavu, kde v každém kroku vzniká chyba a co žádná kombinace signálů nerozhodne.

Vše, co následuje, určují dva závazky. Zaprvé, měření a interpretace zůstávají oddělené: senzor zaznamená kožní vodivost a člověk nebo model z toho vyvodí něco o arousalu. Zadruhé, nic na tomto webu nikoho neměří. Web nesbírá žádná fyziologická data, nespouští žádnou analytiku a nenastavuje žádné trackery. Interaktivní část této stránky je simulace, která pracuje výhradně s hodnotami, jež si vymyslíte.

## Detekční model: signál, příznak, inference, kontext

Každé tvrzení typu „tento člověk prošel uvolněním“ stojí na řetězci čtyř kroků, který je znázorněn níže.

[Signál](../slovnik/#signal) je to, co zaznamená přístroj: napětí z elektrod, světlo odražené kůží zápěstí, zrychlení, akustický tlak. Signál má jednotky a vzorkovací frekvenci, ale žádný psychologický význam.

[Příznak](../slovnik/#feature) je veličina vypočtená ze signálu: průměrná srdeční frekvence za minutu, počet kožních vodivostních reakcí nad určitou hranicí, korelace mezi pohyby dvou lidí. Každý příznak v sobě nese rozhodnutí o časovém okně, filtru, prahu a způsobu odstranění artefaktů. Tato rozhodnutí jsou ve výsledném čísle zřídka vidět, a přesto ho mění.

[Inference](../slovnik/#inference) převádí příznaky na popis člověka: zvýšený [arousal](../slovnik/#arousal), pravděpodobnou fázi epizody, pravděpodobnou kategorii emoce. Právě zde se měření mění v interpretaci. Zda ji provádí natrénovaný klasifikátor, nebo výzkumník hledící na graf, na jejím logickém statusu nic nemění.

[Kontext](../slovnik/#context) je vše, co je o situaci známo a co v signálu není: co člověk dělal, kde, s kým, co záznamu předcházelo a co o tom sám říká. Kontext často rozhoduje mezi interpretacemi, které samotné příznaky neodliší.

Chyba vstupuje do každého kroku a sčítá se. Pohybový artefakt v signálu se stane falešnou špičkou v příznaku, ze špičky se stane odvozená „reakce“ a chybějící kontextový záznam dovolí vyložit tuto reakci jako strach, a ne jako náraz do senzoru. Pozdější kroky nedokážou obnovit informaci, kterou dřívější kroky ztratily. Mohou však slabému signálu dodat zdání autority tím, že mu přidělí sebejistou nálepku.

## Výchozí hodnota: bez ní nic nic neznamená

Srdeční frekvence 95 úderů za minutu je u člověka, který jde, nenápadná, zatímco u jiného, který sedí, je pozoruhodná. Fyziologické příznaky získávají význam pouze vzhledem k [výchozí hodnotě](../slovnik/#baseline): rozpětí hodnot typickému pro daného člověka za srovnatelných podmínek.

Užitečné výchozí hodnoty jsou individuální. Odhadují se z opakovaných záznamů téhož člověka, ideálně v podobnou denní dobu, v podobné poloze těla a při podobné úrovni aktivity. Fyziologické signály ovlivňuje bez jakékoli emoční změny řada běžných faktorů: cirkadiánní rytmus, stání místo sezení, nedávné jídlo, kofein a nikotin, alkohol, léky, nedostatek spánku, nemoc, okolní teplota a vlhkost i pouhé očekávání, že člověk bude měřen. Kožní vodivost například reaguje na teplotu a námahu stejně jako na psychické události a metodické příručky k [elektrodermální aktivitě](../slovnik/#electrodermal-activity) považují podmínky záznamu, umístění elektrod a rozdíly mezi lidmi za zásadní pro její interpretaci (Boucsein, 2012).

[Variabilita srdeční frekvence](../slovnik/#heart-rate-variability) se v psychofyziologii hojně používá, protože vypovídá o vagovém tonu srdce, tedy o podílu parasympatiku na řízení srdeční činnosti, a protože je levná, neinvazivní a snadno zaznamenatelná. Laborde, Mosley a Thayer (2017) přesto upozorňují, že tato snadná dostupnost nesmí zakrýt, jak snadno lze nálezy HRV mylně vyložit, a formulují doporučení pro plánování experimentů, analýzu dat a vykazování výsledků, aby byly závěry podložené a srovnatelné mezi laboratořemi.

Další komplikací je habituace. Reakce na opakovaný podnět mají tendenci slábnout, takže desátý hlasitý refrén večera může vyvolat menší kožní vodivostní reakci než první, i když posluchač oba okamžiky popisuje jako stejně intenzivní. Slábnoucí reakce v čase je tedy v souladu s vyhasínajícím prožitkem, ale také s nezměněným prožitkem a habituujícím tělem.

Skupinové normy zavádějí z příbuzného důvodu. Průměr populace popisuje, co je typické napříč lidmi, ne co je typické pro tohoto člověka. Klidová srdeční frekvence, úroveň kožní vodivosti i variabilita srdeční frekvence se liší podle věku, kondice, tělesné velikosti, zdravotního stavu a léků. Použití populačního prahu na jednotlivce mění běžné rozdíly mezi lidmi ve zdánlivé stavy a soustavně chybně označuje ty, kdo mají k průměru nejdál.

## Multimodalita: víc signálů, ne víc jistoty

Je-li jeden signál nejednoznačný, láká to zkombinovat jich několik. [Multimodalita](../slovnik/#multimodality) v některých ohledech skutečně pomáhá. Senzory s nezávislými zdroji artefaktů se mohou navzájem kontrolovat: akcelerometr ukáže, že vzestup srdeční frekvence se kryl s během, a mikrofon ukáže, že zrychlený dech se kryl se zpěvem. Kombinace modalit omezuje některé chyby, zejména technické.

Ústřední nejednoznačnost však neodstraní, a to ze dvou důvodů.

Prvním důvodem je, že matoucí vlivy bývají signálům společné. Tanec v teplé místnosti zvýší srdeční frekvenci, sníží její variabilitu, zvýší kožní vodivost, zrychlí dech a vytvoří pohyb, to vše najednou. Pět shodujících se signálů pak představuje pět pohledů na jednu příčinu, nikoli pět nezávislých dokladů o emoci.

Druhým důvodem je, že samotné fyziologické vzorce nemusejí být pro kategorie emocí specifické. Siegel a kolegové (2018) metaanalyzovali 202 studií, které měřily reaktivitu autonomního nervového systému při laboratorním navozování emocí u neklinických vzorků dospělých. Autonomní proměnné se sice měnily, vzorec velikostí účinku však jednu kategorii emocí od jiné jasně neodlišoval. Variabilita uvnitř kategorií byla značná a korekce na publikační zkreslení odhadované účinky dále snížila. Autoři dospěli k závěru, že nálezy jsou více v souladu s pojetím kategorií emocí jako proměnlivých populací jednotlivých případů než s pevnými autonomními „otisky“.

Otázka je předmětem skutečné odborné debaty. Starší přehled Kreibigové (2010), zahrnující 134 experimentálních publikací, dospěl k závěru, že autonomní reakce vykazují značnou specificitu, pokud se berou v úvahu podtypy jednotlivých emocí, a zdůraznil, že pro takové závěry je důležitá přesná terminologie zkoumaných stavů i pečlivá volba fyziologických ukazatelů. Oba přehledy se liší metodou i otázkami, které kladou. Pro účel této stránky je důležitější, co mají společné: oba popisují vzorce odhadnuté napříč mnoha účastníky při kontrolovaném navozování přesně vymezených stavů. Ani jeden nenabízí vzorec, který by bylo možné použít na jednoho člověka v nekontrolovaném prostředí a zjistit z něj, co tento člověk prožívá.

Pohyby obličeje, často přidávané jako „další modalita“, mají stejné omezení. Barrettová a kolegové (2019) zjistili, že lidé se v očekávaných emočních situacích skutečně usmívají, mračí nebo zamračeně hledí častěji, než by odpovídalo náhodě, ale že způsob vyjadřování emocí se výrazně liší napříč kulturami, situacemi i jednotlivci, že podobné konfigurace obličeje vyjadřují více než jednu kategorii emocí a že konfigurace, jako je zamračení, často sděluje něco jiného než emoční stav.

Za tím vším stojí problém [obrácené inference](../slovnik/#reverse-inference). Poldrack (2006) jej popsal pro zobrazování mozkové aktivity: usuzování, že proběhl určitý mentální proces, protože byla aktivní oblast s tímto procesem spojovaná. Takové závěry nejsou deduktivně platné, i když mohou přinést určitou evidenci, a jejich hodnotu omezuje to, jak selektivní pozorovaná aktivita je. Stejná logika platí pro tělesné signály. Arousal stoupá při strachu, ale i při radosti, námaze a v horku. Čím méně je signál selektivní, tím méně jeho přítomnost vypovídá o jakémkoli jednotlivém stavu, a přidání dalších neselektivních signálů žádný z nich selektivním neučiní.

## Sebevýpověď: nepostradatelná a nedokonalá

[Sebevýpověď](../slovnik/#self-report) je jediný přístup k tomu, jak se prožitek jeví zevnitř. Fyziologická data mohou ukázat, že se něco změnilo; jen člověk sám může říct, zda změna působila jako uvolnění, úzkost, nuda, nebo nic zvláštního, a zda byla její [valence](../slovnik/#valence) příjemná, nebo nepříjemná. Každý seriózní model katarze proto sebevýpověď potřebuje a musí s ní zacházet jako s měřením, které má vlastní chyby.

Robinson a Clore (2002) navrhli model dostupnosti pro emoční sebevýpovědi, postavený na rozlišení mezi emocí samotnou, která je epizodická, prožitková a vázaná na kontext, a přesvědčeními o emocích, která jsou sémantická, pojmová a od kontextu odpoutaná. Toto rozlišení pomáhá vysvětlit nesoulady, které se často objevují mezi výpověďmi o pocitech, jež člověk prožívá právě teď, a výpověďmi o pocitech, které aktuálně neprožívá, například jak se cítil minulý týden nebo jak se obvykle cítí na koncertech. Když prožitek už není přítomen, může výpověď více vycházet z toho, jak si člověk myslí, že se takové situace prožívají.

Zpětné výpovědi utváří také struktura epizody. Fredricksonová a Kahneman (1993) požádali účastníky, aby průběžně hodnotili filmové ukázky a poté každou ukázku zhodnotili jako celek. Délka ukázky měla na celková hodnocení jen malý vliv a hodnocení se chovala jako vážený průměr „snímků“ prožitku, jako by na délce nezáleželo. V příbuzném experimentu Kahneman a kolegové (1993) vystavili účastníky krátkému pokusu s bolestivě studenou vodou a delšímu pokusu, který k tomu přidal 30 sekund o něco méně studené, stále nepříjemné vody. Když si měli vybrat, který pokus zopakují, významná většina zvolila ten delší. Zpětnému hodnocení takových epizod často dominují nejhorší a závěrečné okamžiky. Noc, která skončí na vrcholu, si člověk bude spíše pamatovat jako obnovující víc, než by odpovídalo jejímu průběhu minutu po minutě.

Část tohoto problému řeší ekologické momentové hodnocení (EMA). Opakovaně zjišťuje aktuální prožitky a chování lidí v reálném čase a v jejich běžném prostředí, často v náhodně zvolených okamžicích, pomocí nástrojů od papírových deníků po elektronická zařízení a fyziologické senzory. Jeho cílem je minimalizovat zkreslení vybavováním a maximalizovat ekologickou validitu (Shiffman, Stone a Hufford, 2008). EMA neodstraňuje všechny zdroje chyb. Opakované dotazování může změnit, čeho si lidé všímají, nabídka odpovědí omezuje, co lze vypovědět, a lidé mohou odpovídat tak, jak to považují za přijatelné, zvlášť když vědí, že data uvidí někdo další. Tato poslední obava, sociální žádoucnost, je nejpalčivější právě tam, kde se monitorování emocí navrhuje nejčastěji: na pracovištích, ve školách a ve zdravotnictví.

Praktickým důsledkem je, že sebevýpověď a fyziologická data nejsou pravda a její zástupný ukazatel. Jsou to dvě nedokonalá měření různých stránek epizody a nesoulad mezi nimi je informací, ne šumem, který se má zprůměrovat.

## Časový model

Katarze, jak ji popisuje umělecké dílo, je spíše sled než stav. Časový model v tabulce níže dělí epizodu podobnou katarzi do sedmi fází: výchozí stav, aktivace, synchronizace, vrchol, vybití, zotavení a stav po epizodě. U každé fáze uvádí, co by se v zásadě dalo zaznamenat a proč toto pozorování interpretaci neprokazuje.

Model je heuristika pro uspořádání pozorování, nikoli empirický nález. Svůj rámec si vypůjčuje z výzkumu dynamiky emocí, který zkoumá trajektorie, vzorce a pravidelnosti, s nimiž prožitkové, fyziologické a behaviorální složky emocí v čase kolísají, procesy za tímto kolísáním a jeho důsledky pro duševní pohodu (Kuppens a Verduyn, 2017). Tento rámec je užitečný, protože pojímá emoční epizodu jako soubor časových řad, a ne jako jedinou nálepku. Neznamená, že každá epizoda prochází těmito sedmi fázemi, v tomto pořadí, nebo vůbec.

Pro celou tabulku platí tři výhrady. Fáze se určují zpětně: vrchol je vrcholem teprve tehdy, když hodnoty klesnou. Fyziologická, behaviorální a vypovídaná podoba fáze se mohou odvíjet v různých časových měřítkách a nemusejí se krýt. A synchronizace se týká jen sdílených situací; člověk, který pláče o samotě, může projít aktivací, vrcholem i vybitím zcela bez synchronizace.

Synchronizace si zaslouží bližší pohled, protože je to fáze pro kolektivní katarzi nejvíce specifická. Ve třech experimentech lidé, kteří předtím jednali synchronně s ostatními, více spolupracovali v následných skupinových ekonomických úlohách, i když spolupráce vyžadovala osobní oběť, a k tomuto účinku nebylo nutné vyvolat pozitivní emoce (Wiltermuth a Heath, 2009). Při skupinovém tanci synchronie i námaha nezávisle na sobě zvýšily práh bolesti, používaný jako zástupný ukazatel aktivity endorfinů, a posílily soudržnost skupiny (Tarr a kol., 2015). Tyto výsledky podporují chápání sdíleného pohybu jako smysluplné sociální proměnné. První z nich zároveň ukazuje, proč nemůže sloužit jako údaj o prožitku: sociální účinek synchronie nezávisel na pozitivních emocích. Podrobněji se této práci věnuje [Výzkumná poznámka 03](@/research/collective-synchrony/index.cs.md).

## Zachycená úleva neznamená vyřešenou příčinu

Endpoint uměleckého díla odpovídá `problem_solved: false`. Nejde o vtip na účet úlevy. Je to nejpřesnější tvrzení, jaké by telemetrie mohla učinit.

Předpokládejme, že všechny výše popsané kroky fungují dobře: kvalitní výchozí hodnota, čisté signály, rozumné příznaky, bohatý kontext a momentová výpověď o úlevě. Nejsilnějším obhajitelným závěrem by bylo, že byl pozorován vzorec v souladu s aktivací následovanou návratem k výchozímu stavu a že člověk uvedl pocit úlevy. To je tvrzení o změně stavu. Neříká nic o tom, zda se změnily podmínky, které tíseň vyvolaly, například konflikt, ztráta, dluhy, osamělost nebo nebezpečný domov. Tyto podmínky v signálu nejsou; neměří se. [Úleva a vyřešení](../slovnik/#relief-vs-resolution) jsou různé veličiny a [Výzkumná poznámka 04](@/research/relief-is-not-resolution/index.cs.md) popisuje mechanismy, od negativního posilování po paměť, kvůli nimž se snadno zaměňují.

Výzkum hněvu ukazuje, proč by viditelné vybití nemělo být zaměňováno s řešením. Kjærviková a Bushman (2024) metaanalyzovali 154 studií se 184 nezávislými vzorky a 10 189 účastníky, které testovaly činnosti ke zvládání hněvu. Činnosti snižující arousal, jako hluboké dýchání, všímavost a meditace, snižovaly hněv a agresi (Hedgesovo g = −0,63). Činnosti arousal zvyšující, jako bušení do pytle, běh nebo jízda na kole, byly celkově neúčinné (g = −0,02) a jejich výsledky byly heterogenní. Autoři dospěli k závěru, že nálezy nepodporují představu, že ventilování hněvu nebo jít si zaběhat jsou účinné způsoby jeho zvládání. Činnost zvyšující arousal tak může ve fyziologickém záznamu vytvořit výrazný vrchol a vybití, a přitom podle těchto dat v průměru hněv příliš nesnížit. Doporučení [Nechte hněv vychladnout](@/advice/let-anger-cool/index.cs.md) z toho vyvozuje praktické kroky.

Poctivý model má proto dva výstupy tam, kde dashboard má jeden. První, změnu stavu, lze odvodit s uvedenou mírou jistoty. Druhý, zda je příčina vyřešena, buď uvádí člověk sám a je neověřený, nebo je neznámý.

## Měření versus interpretace

Vezměme vymyšlený, ale realistický záznam srdeční frekvence. Z klidové hodnoty kolem 65 úderů za minutu stoupá během několika minut zhruba na 140, chvíli se tam drží, pak rychle klesne a během následující čtvrthodiny se ustálí kolem 75. Kožní vodivostní reakce jsou během vzestupu časté a poté řídké.

Zaznamenaný na koncertě je tento průběh v souladu s tancem, nadšením a davem, který prochází gradací a uvolněním. Zaznamenaný během panického záchvatu je v souladu s návalem strachu, zrychleným dýcháním a postupným zklidněním, jak záchvat odeznívá. Zaznamenaný při intervalovém běhu je v souladu s námahou a následným vyklusáním, zcela bez emoční epizody.

Měření je ve všech třech případech totožné. Liší se interpretace a tu neopravňuje záznam, nýbrž kontext: místo, akcelerometr ukazující běh nebo skákání, vlastní výpověď člověka, jeho historie. Bez kontextu je jediným obhajitelným výstupem popis měření, „srdeční frekvence stoupla zhruba o 75 úderů za minutu nad výchozí hodnotu a vrátila se k ní“, spolu s konstatováním, že příčina vzestupu není prokázána.

Tyto tři případy mají ještě něco společného. V každém z nich by systém, který by pokles srdeční frekvence označil jako „úlevu“, používal slovo patřící k prožitku k popisu veličiny patřící srdci. Na koncertě by se nálepka mohla náhodou shodovat s tím, co člověk říká. Po panickém záchvatu by byla zavádějící, protože strach se může vrátit. Po běhu by šlo o kategoriální omyl.

## Co jednotlivé signály mohou a nemohou říct

Detekční matice níže uvádí deset druhů údajů, z nichž by systém pro zachycení změn podobných katarzi mohl vycházet, od srdeční frekvence po kontextové záznamy. U každého odděluje, co se zaznamenává, s čím je zaznamenaný vzorec v souladu, co sám o sobě nemůže prokázat a jaké časté matoucí vlivy vytvářejí stejný vzorec z nesouvisejících důvodů.

Dvě vlastnosti matice jsou záměrné. Každá buňka „je v souladu s“ uvádí něco širšího než konkrétní emoci, protože výše shrnuté důkazy nepodporují spojování těchto signálů s konkrétními emocemi u jednotlivců. A poslední dva řádky, momentová sebevýpověď a kontextové záznamy, vůbec nejsou fyziologické. Jsou zařazeny proto, že bez nich jsou fyziologické řádky z velké části neinterpretovatelné, a proto, že mají vlastní meze: výpověď je popis, ne ověření, a záznam času a místa není popisem prožitku.

## Jak mluvit o nejistotě

Systém, který popisuje lidi, by měl používat slova, jejichž síla odpovídá jeho důkazům. Slovník níže se na celém webu používá jednotně a simulace na této stránce jej používá pro svůj výstup.

Výrazy tvoří hrubý žebříček. „Neměřeno“ a „neznámé“ označují, že pro tvrzení chybí jakýkoli podklad. „Nedostatek důkazů“ označuje data, která existují, ale nedokážou rozlišit mezi interpretacemi. „Je v souladu s“ a „je spojeno s“ označují slučitelnost a statistický vztah, aniž by naznačovaly příčinnost nebo platnost pro jednotlivce. „Naznačuje“ označuje sbíhání pozorování poté, co byly zváženy alternativy. „Odvozeno s nízkou jistotou“ označuje výstup modelu tím, čím skutečně je. „Je v rozporu s“ zaznamenává konflikt mezi zdroji, který by měl vést k prověření modelu dříve, než padne jakýkoli závěr o člověku.

Stejně důležité je, co slovník vynechává. Neobsahuje žádný výraz, který by signálu dovolil rozhodnout, co člověk prožívá, ani výraz pro model, který by měl přístup k lidskému prožitku, protože žádná metoda popsaná na této stránce by takové tvrzení nepodložila.

## Falešně pozitivní a falešně negativní výsledky

Každý klasifikátor dělá dva druhy chyb. [Falešně pozitivní výsledek](../slovnik/#false-positive) ohlásí stav, který přítomen není; [falešně negativní výsledek](../slovnik/#false-negative) přehlédne stav, který přítomen je. Oba jsou s příklady popsány níže.

Láká to shrnout systém jediným číslem přesnosti. To však zakrývá dvě skutečnosti: obě chyby mají zřídka stejnou cenu a jejich cena závisí na tom, kdo výstup používá a k čemu. Vezměme dvě nálepky, které by monitorovací systém mohl člověku přidělit po intenzivním večeru.

Falešná nálepka „zotaven“, tedy falešně negativní výsledek pro přetrvávající tíseň, může ukončit rozhovor, který měl pokračovat. Přítel, klinik nebo podpůrná služba, která nálepce důvěřuje, nemusí položit otázku, jež by odhalila, že člověk v pořádku není. Cenu nese ten, kdo potřeboval pomoc a nedostal ji.

Falešná nálepka „v tísni“, tedy falešně pozitivní výsledek, může vyvolat nevyžádanou pozornost, obavy nebo zásah. Na pracovišti nebo ve škole může přisoudit psychologický popis někomu, kdo nic nesdělil, s důsledky pro to, jak se s ním zachází. Cenu opět nese popisovaný člověk a roste tehdy, když má instituce nad ním moc.

Snížení rozhodovacího prahu, aby se zachytilo více skutečné tísně, přináší více planých poplachů; jeho zvýšení, aby se planým poplachům předešlo, přehlédne více tísně. Žádné nastavení neodstraní obojí. Volba prahu je proto rozhodnutím o tom, čí chyby jsou přijatelné. Mělo by padnout otevřeně, lidmi, kteří za důsledky odpovídají, a za účasti dotčených, ne být potichu vyladěno pro benchmark.

Důležité jsou i základní četnosti. Je-li hledaný stav ve sledované populaci vzácný, i systém s dobrou senzitivitou a specificitou vyprodukuje mnoho falešně pozitivních výsledků v poměru ke skutečně pozitivním. Plyne to z aritmetiky, ne z nějaké konkrétní studie, a je to další důvod k opatrnosti při plošném sledování davů, tříd nebo celých pracovních kolektivů.

## Kontextový modul

Předchozí oddíly se ke kontextu opakovaně vracejí. Stojí za to konkrétně popsat, co by komponenta kombinující signály s kontextem potřebovala, protože už samotný výčet ukazuje, proč ji tato stránka popisuje jako konceptuální.

Minimálně by potřebovala situaci: kde člověk je a co se kolem něj děje. Potřebovala by činnost: zda sedí, tančí, běží, mluví, nebo zpívá. Potřebovala by nedávnou historii, jako spánek, návykové látky, nemoc a to, co se ten den stalo dříve, a osobní výchozí hodnotu vytvořenou z opakovaných záznamů téhož člověka. Především by potřebovala vlastní výpověď člověka, získanou v danou chvíli, jeho vlastními slovy a se svobodou neodpovědět. A aby mohla říct cokoli o vyřešení, a ne jen o úlevě, potřebovala by informace o podmínkách, do nichž se člověk vrací, které žádný senzor nezaznamenává a které si lidé mají plné právo nechat pro sebe.

Každý z těchto vstupů je obtížné spolehlivě získat, jeho sběr je invazivní, nebo obojí, a několik z nich může pocházet jen od člověka samotného. Jakmile jsou k dispozici, většinu interpretační práce odvádí výpověď člověka a situace, nikoli senzory, a fyziologické signály se stávají podpůrnými údaji, a ne zdrojem závěru. To je správný vztah a je to důvod, proč kontextový modul není zkratkou k poznání toho, co lidé prožívají.

Na tomto webu je kontextový modul konceptuální: způsob, jak uvažovat o tom, co by poctivá inference vyžadovala. Není implementován a neexistuje žádný tok dat, který by ho mohl napájet.

## Etika a soukromí

Afektivní počítání, pojem, který zavedla Picardová (1997), je studium a návrh systémů, které rozpoznávají a interpretují lidské emoce a reagují na ně. Stark a Hoey (2021) vytvořili taxonomii pojmových modelů emocí a zástupných dat používaných při digitální analýze emočních projevů a argumentovali, že paradigmatům, která informatici vyvinuli nebo převzali z jiných oborů, nelze jen tak věřit, že poskytují objektivní pravdu o lidských emocích. To, jak jsou emoce pojímány, snímány, měřeny a převáděny na data, utváří etické a společenské důsledky výsledných systémů.

Z metod popsaných výše přímo vyplývá několik obav.

**Souhlas.** Fyziologické signály vznikají nepřetržitě a bezděčně. Člověk nemůže odmítnout mít srdeční tep tak, jako může odmítnout zveřejnit zprávu. Smysluplný souhlas s odvozováním emocí musí být konkrétní, informovaný a odvolatelný a v davu či na veřejném prostranství je obtížné ho získat.

**Omezení účelu.** Data sebraná k jednomu účelu, například ke sledování kondice, mohou posloužit k odvozování stresu, nálady nebo zdravotního stavu, s nimiž člověk nikdy nesouhlasil. Odpovědný systém sbírá jen to, co vyžaduje deklarovaný účel, a data k jinému účelu nepoužívá.

**Nesdělené stavy.** Hlavní riziko odvozování emocí nespočívá jen v tom, že se často mýlí, ale v tom, že si nárokuje přístup ke stavům, které se lidé rozhodli nesdělit. I závěr s nízkou jistotou může být, jakmile se zapíše do záznamu, považován za fakt o člověku.

**Mocenská nerovnováha.** Tentýž závěr znamená něco jiného podle toho, kdo ho má v rukou. Mezi přáteli může vést k laskavé otázce. V dashboardu zaměstnavatele, monitorovacím systému školy nebo modelu pojišťovny může ovlivnit hodnocení, kázeňská opatření nebo cenu, zatímco popisovaný člověk má jen malou možnost ho vidět, napadnout nebo opravit. Zvláštní pozornost si zaslouží použití na pracovištích a ve školách, protože účast tam v praxi málokdy bývá dobrovolná.

**Validita jako etická otázka.** Vzhledem k důkazům o autonomních a obličejových vzorcích není nasazení odvozování emocí se sebejistými nálepkami jen technickým přestřelením. Vystavuje lidi důsledkům založeným na tvrzeních, která metody nedokážou podložit.

Z těchto bodů vychází i postoj tohoto webu. Nesbírá žádná fyziologická ani osobní data. Nepoužívá žádnou analytiku, trackery ani cookies. Simulace na této stránce běží celá ve vašem prohlížeči s hodnotami, které si vymyslíte, a nic z toho, co zadáte, stránku neopustí.

## Technická architektura a stav implementace

Tabulka stavu níže uvádí komponenty tohoto projektu a u každé věcně označuje, zda je implementována, jde o simulaci, je konceptuální, nebo není plánována. Tato označení jsou součástí argumentu. Projekt, který kritizuje sebejistá tvrzení o lidech, by neměl dělat sebejistá tvrzení o sobě.

Implementována je publikační infrastruktura: statický web, registr referencí kontrolovaný vůči Crossrefu, evidenční přehled s daty revizí, verzované obsahové API a klientská knihovna a nástroj příkazové řádky v Rustu pro čtení zveřejněného obsahu. Žádná z těchto komponent nepřijímá data o čtenářích. Simulace v prohlížeči je výuková pomůcka, která uplatňuje úvahy z této stránky na vymyšlená čísla. Kontextový modul existuje jen jako výše uvedený popis. Příjem fyziologických signálů, individuální odvozování emocí nebo profilování a analytika či sledování návštěvníků plánovány nejsou a jejich absence je konstrukčním rozhodnutím, nikoli chybějící funkcí.

## Limity této stránky

Tato stránka je vzdělávací. Není klinickým doporučeným postupem, validovaným protokolem měření ani technickou specifikací a neměla by sloužit k posuzování emočního nebo duševního stavu kohokoli. Uvedené signály a matoucí vlivy jsou ilustrativní, nikoli vyčerpávající, časový model je heuristika, nikoli nález, a modelové příklady používají vymyšlené hodnoty. Shrnutí studií jsou záměrně stručná; kdo potřebuje podrobnosti, měl by nahlédnout do původních zdrojů v seznamu literatury, a [přehled důkazů](@/evidence/index.cs.md) ukazuje, jak jsou tvrzení na tomto webu hodnocena a přezkoumávána.

Pokud máte obavy o vlastní tíseň nebo o tíseň někoho jiného, nejvíce informací stále přinese rozhovor a u přetrvávajících nebo vážných potíží rozhovor s kvalifikovaným odborníkem. Žádný senzor nenahradí ani jedno.
