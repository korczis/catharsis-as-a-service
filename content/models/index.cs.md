+++
title = "Interaktivní modely: co v čase dělají úleva, vzrušení, paměť a synchronie"
description = "Pět interaktivních modelů, které se počítají ve vašem prohlížeči z hodnot, jež nastavíte, ukazuje, jak úleva posiluje návyk, jak vzrušení ovlivňuje hněv, jak paměť váží vrcholy a konce, jak se rytmy sladí a jak se hromadí stresová zátěž."
date = 2026-09-14
template = "models.html"
slug = "modely"

[taxonomies]
tags = ["modely", "simulace", "teorie", "úleva", "synchronie"]

[extra]
kicker = "Interaktivní modely"
summary = "Řada argumentů na tomto webu se týká procesů, které se odvíjejí v čase: úlevy, jež pomine, hněvu, který odeznívá, vzpomínek, které nadržují koncům, rytmů, jež se sladí, a stresu, který se hromadí. Tato stránka převádí pět takových myšlenek do malých modelů, které můžete spustit a měnit. Každý model otevřeně uvádí svá pravidla a předpoklady, takže je vidět, odkud jeho chování pochází. Vstupy jsou vymyšlené, výstupy ilustrativní a nic zde nepopisuje ani nehodnotí žádného skutečného člověka."
banner = "Ilustrativní modely · nejde o předpovědi o kterémkoli člověku"
key_points = [
  "Každé číslo na této stránce se počítá ve vašem prohlížeči z hodnot, které nastavíte; žádné nepochází od člověka, ze zařízení ani z dat studie.",
  "Každý model převádí jednu myšlenku z výzkumu na několik výslovných pravidel, aby je bylo možné prozkoumat, obměňovat a zpochybnit.",
  "Tam, kde model vychází z empirických zjištění, sledují jeho křivky jejich směr, nikoli velikost ani časový průběh.",
  "Model, který se chová věrohodně, není dokladem, že se tak chovají lidé; doklady jsou v citovaných studiích, nikoli v křivkách.",
]
references = ["rescorla-wagner-1972", "hayes-1996", "kjaervik-bushman-2024", "bushman-2002", "kahneman-1993", "fredrickson-kahneman-1993", "kuramoto-1984", "strogatz-2000", "wiltermuth-heath-2009", "tarr-2015", "mcewen-1998"]

[[extra.models]]
id = "relief-loop"
title = "Smyčka úlevy"
question = "Co se děje s nutkáním opakovat úlevné chování, když příčina tísně zůstává stejná, a co se změní, když se změní samotná příčina?"
explanation = "Negativní posílení upevňuje chování, které odstraní nepříjemný stav, bez ohledu na to, zda se chování dotkne jeho zdroje. Model to zjednodušuje na jedinou veličinu, nutkání opakovat, která po každé epizodě vzroste o podíl vzdálenosti, jež ještě zbývá k maximu, úměrně velikosti úlevy. Tato aktualizace ve zjednodušené podobě přebírá tvar Rescorlova–Wagnerova modelu podmiňování, v němž učení koriguje rozdíl mezi naučeným a možným. Dokud příčina trvá, vrací se tíseň před každou epizodou na stejnou výchozí úroveň, takže návyk může sílit, aniž se změní to, na co reaguje. Vyzkoušejte silnou úlevu bez šance na změnu a potom úlevu ponechte a zvyšte šanci, že se příčina změní."
reading = "Každá epizoda má dvě hodnoty tísně: úroveň před úlevným chováním a nižší úroveň hned po něm; rozdíl mezi nimi je úleva. Úroveň před každou epizodou zůstává rovná, dokud se příčina nezmění. Křivka nutkání ukazuje, jak silně je chování naučené, od nuly po maximum."
assumptions = [
  "Tíseň před každou epizodou je pevně 70 ze 100, dokud příčina trvá, a 20 poté, co se změnila.",
  "Úleva je v každé epizodě stejně velká a do další epizody zcela odezní.",
  "Nutkání roste o 15 % zbývající vzdálenosti k maximu, násobeno úlevou dělenou 100; po změně příčiny klesá o 10 % za epizodu.",
  "O tom, zda se příčina změní, rozhoduje v každé epizodě náhodný los s pevným semínkem, takže stejné nastavení dává vždy stejný průběh.",
]
limits = [
  "Rescorlovo–Wagnerovo pravidlo vzniklo pro pavlovovské podmiňování; použít jeho tvar pro návyk vyhledávat úlevu je analogie, nikoli aplikace ověřeného modelu.",
  "Ve skutečném životě se úleva liší od případu k případu a příčiny se jen zřídka mění náhodou: mění se jednáním, oporou a okolnostmi, z nichž model nezachycuje nic.",
  "Tíseň i nutkání jsou vymyšlené veličiny, nikoli skóre z jakéhokoli dotazníku.",
]
references = ["rescorla-wagner-1972", "hayes-1996"]
labels = { relief = "Úleva za epizodu", change = "Šance, že se příčina v epizodě změní", episodes = "Epizoda", distress_before = "Tíseň před", distress_after = "Tíseň po", urge = "Nutkání opakovat", resolved = "Příčina se změnila v epizodě", never = "Příčina se během 30 epizod nezměnila", reset = "Obnovit", chart = "Spojnicový graf za 30 epizod, který ukazuje tíseň před každou epizodou a po ní na škále 0 až 100 a naučené nutkání opakovat, se značkou u epizody, v níž se příčina změnila, pokud se změnila." }

[[extra.models]]
id = "venting-arousal"
title = "Ventilace a vzrušení v čase"
question = "Jak by se mohl po provokaci během půl hodiny měnit hněv, když člověk klidně čeká, snižuje vzrušení, nebo ho zvyšuje bušením do pytle?"
explanation = "Teorie katarze předpovídala, že prudké vyjádření hněvu ho vyčerpá. V experimentu však bušení do boxovacího pytle při myšlenkách na člověka, který hněv vyvolal, zanechalo účastníky rozzlobenější a agresivnější než nečinnost (Bushman, 2002). Metaanalýza 154 studií zjistila, že činnosti snižující vzrušení zmírňovaly hněv a agresi (g = −0,63), kdežto činnosti vzrušení zvyšující neměly celkově žádný účinek (g = −0,02) (Kjærvik a Bushman, 2024). Model kreslí křivky ve směru těchto zjištění: hněv s časem odeznívá, rychleji odeznívá při snížení vzrušení a při zvýšení vzrušení neodeznívá o nic rychleji než při čekání, přičemž samotné vzrušení zůstává déle vysoko. Porovnejte hodnotu hněvu po deseti minutách u všech tří činností."
reading = "Vodorovná osa ukazuje minuty od provokace. Hněv a vzrušení jsou zobrazeny na ilustrativní škále bez jednotek, takže srovnání nesou tvary křivek, nikoli čísla. Hodnota po deseti minutách nabízí jeden bod, v němž lze činnosti porovnat."
assumptions = [
  "Všechny tři činnosti začínají hned po provokaci ze stejné úrovně hněvu.",
  "Hněv klesá exponenciálně s časovou konstantou 10 minut při čekání, 5 minut při pomalém dýchání a 11 minut při bušení do pytle.",
  "Při zvyšování vzrušení vzrušení nejprve stoupá a pak pomalu klesá; hněv a vzrušení se počítají odděleně, bez vzájemné zpětné vazby.",
  "Tvary odrážejí pouze směr publikovaných účinků; velikosti účinků nebyly převedeny na minuty.",
]
limits = [
  "Žádná zde citovaná studie tyto křivky neměřila minutu po minutě; časové konstanty jsou vymyšlené, aby byl směr zjištění viditelný.",
  "Souhrnné účinky zakrývají heterogenitu: studie činností zvyšujících vzrušení se lišily a průměr nepopisuje, jak se mění hněv konkrétního člověka.",
  "Model se týká hněvu po provokaci. Neříká nic o smutku ani strachu, ani o pohybu obecně, který má jiné doložené přínosy.",
]
references = ["kjaervik-bushman-2024", "bushman-2002"]
labels = { activity = "Činnost", waiting = "Klidné čekání", calming = "Snižování vzrušení (pomalé dýchání)", venting = "Zvyšování vzrušení (bušení do pytle)", minutes = "Minuty od provokace", anger = "Hněv (ilustrativní)", arousal = "Vzrušení (ilustrativní)", at_ten = "Hněv po 10 minutách", chart = "Spojnicový graf za 30 minut od provokace, který ukazuje ilustrativní hněv pro zvolenou činnost a při zvyšování vzrušení také ilustrativní křivku vzrušení, s vyznačenou hodnotou hněvu po 10 minutách." }

[[extra.models]]
id = "peak-end"
title = "Vrchol a konec ve vzpomínce na nepohodlí"
question = "Proč si člověk může delší nepříjemnou epizodu pamatovat jako méně nepříjemnou než kratší, která obsahovala méně nepohodlí celkem?"
explanation = "Zpětnému hodnocení nepříjemných epizod obvykle dominuje nejhorší a závěrečný okamžik, zatímco délka hraje jen malou roli (Fredrickson a Kahneman, 1993). V experimentu se studenou vodou se výrazná většina účastníků rozhodla zopakovat delší pokus, který končil 30 sekundami o něco méně studené, stále bolestivé vody, a nikoli kratší pokus bez tohoto konce (Kahneman a kol., 1993). Model staví průměr a součet všech okamžiků vedle odhadu podle vrcholu a konce, tedy průměru nejvyššího a posledního okamžiku. Nastavte vysoký závěrečný okamžik, přidejte mírnější a sledujte, jak součet roste, zatímco odhad podle vrcholu a konce klesá."
reading = "Sloupce ukazují nepohodlí jednotlivých okamžiků v pořadí. Průměr a součet popisují celou epizodu, kdežto odhad podle vrcholu a konce používá jen dva její okamžiky. Přidání závěrečného okamžiku s hodnotou 3 odhad sníží, pokud je dosavadní poslední okamžik vyšší než 3, a zvýší, pokud je nižší."
assumptions = [
  "Zapamatované nepohodlí je přiblíženo prostým průměrem vrcholu a závěrečného okamžiku.",
  "Všechny okamžiky trvají stejně dlouho a nepohodlí se hodnotí od 0 do 10.",
  "Součet všech okamžiků zastupuje to, kolik nepohodlí člověk skutečně prožil.",
]
limits = [
  "Vzorec vrcholu a konce popisuje tendenci napříč účastníky laboratorních pokusů s filmovými ukázkami a studenou vodou; není vzorcem pro paměť jednoho člověka a jeho použití na noční akce nebo životní události je extrapolací.",
  "Rozhodnutí epizodu zopakovat není totéž jako mít z ní užitek; model ukazuje, jak se paměť může odchýlit od prožitku, nikoli který prožitek je lepší.",
]
references = ["kahneman-1993", "fredrickson-kahneman-1993"]
labels = { moment = "Okamžik", discomfort = "Nepohodlí", average = "Průměr všech okamžiků", peak_end = "Odhad podle vrcholu a konce", total = "Celkové nepohodlí", add = "Přidat mírnější závěrečný okamžik", remove = "Odebrat poslední okamžik", reset = "Obnovit", chart = "Sloupcový graf nepohodlí od 0 do 10 pro každý okamžik v pořadí, s referenčními čarami pro průměr všech okamžiků a pro odhad podle vrcholu a konce a s celkovým nepohodlím uvedeným vedle." }

[[extra.models]]
id = "synchrony"
title = "Synchronie spřažených oscilátorů"
question = "Jak silné musí být vzájemné působení rytmů s různými vlastními tempy, aby se sladily do společného kroku?"
explanation = "Kuramotův model popisuje populaci oscilátorů, z nichž každý má vlastní frekvenci a každý je přitahován k fázím ostatních. Je-li vazba slabá vzhledem k rozptylu vlastních frekvencí, fáze se rozcházejí; nad určitou prahovou hodnotou se část populace zachytí ve společném rytmu, zatímco zbytek se dál rozchází (Kuramoto, 1984; Strogatz, 2000). Parametr uspořádání r shrnuje stav celé skupiny: blíží se 0, když jsou fáze rozptýlené po kruhu, a je 1, když se všechny oscilátory pohybují spolu. Začněte bez vazby a pomalu zvyšujte K, pak rozšiřte rozptyl temp a sledujte, o kolik silnější vazba je potřeba."
reading = "Každá tečka je jeden oscilátor, který obíhá kruh vlastním tempem. Hodnota r je délka průměru poloh všech teček chápaných jako šipky ze středu: krátká, když jsou tečky rozptýlené, dlouhá, když se shlukují. Sledujte r v čase, nikoli v jediném okamžiku, protože kolísá."
assumptions = [
  "Každý oscilátor je spřažen se všemi ostatními stejně, jedinou silou vazby K.",
  "Vlastní tempa jsou náhodně vybrána z rozmezí, jehož šířku určuje rozptyl.",
  "Každý oscilátor je popsán pouze fází; amplituda, únava a vnější šum jsou vynechány.",
]
limits = [
  "Při 4 až 40 oscilátorech hodnota r kolísá a ani bez vazby téměř nikdy neklesne na 0; ostrý práh matematické teorie platí pro velmi velké populace.",
  "Jde o matematický model synchronizace obecně, nikoli o model tanečníků, davu nebo sounáležitosti; experimenty, které spojily synchronní pohyb se spoluprací a blízkostí, zkoumaly lidi, nikoli oscilátory.",
]
references = ["kuramoto-1984", "strogatz-2000", "wiltermuth-heath-2009", "tarr-2015"]
labels = { coupling = "Síla vazby K", count = "Počet oscilátorů", spread = "Rozptyl vlastních temp", order = "Synchronie r", play = "Spustit", pause = "Pozastavit", step = "Krok", reset = "Obnovit", chart = "Animovaný kruh s jednou tečkou za každý oscilátor, která se pohybuje vlastním tempem, a s údajem o synchronii r mezi 0 a 1." }

[[extra.models]]
id = "allostatic-load"
title = "Alostatická zátěž a zotavení"
question = "Kdy se opakovaný stres hromadí, místo aby pominul, a jak to mění tempo zotavení?"
explanation = "Stresové reakce pomáhají tělu zvládat nároky, ale McEwen (1998) popsal, jak opakovaná aktivace nebo reakce, které se nevypínají účinně, mohou nést kumulativní cenu, již nazval alostatickou zátěží. Model tuto myšlenku převádí na jednoduché účetnictví: každý stresor přidá 10 jednotek a každý den se zotavením odebere pevné procento aktuální zátěže. Když stresory zátěž přidávají rychleji, než ji zotavení odebírá, zátěž roste, dokud se neustálí na vyšší úrovni, nebo při pomalém zotavení stoupá celé týdny. Ponechte počet stresorů beze změny a měňte jen zotavení, potom postupujte naopak."
reading = "Vodorovná osa ukazuje týdny a křivka zátěž v libovolných jednotkách. Nejvyšší zátěž za 12 týdnů je uvedena zvlášť. Křivka, která se zplošťuje, znamená, že denní zotavení dohnalo denní přírůstek; neznamená, že zátěž zmizela."
assumptions = [
  "Všechny stresory jsou stejné a každý přidá stejných 10 jednotek.",
  "Zotavení každý den odebere stejné procento aktuální zátěže bez ohledu na to, co ji vyvolalo.",
  "Stresory přicházejí po všech 12 týdnů stejným týdenním tempem, bez přestávek a bez krizí.",
]
limits = [
  "Alostatická zátěž je koncepční rámec, jehož měření je stále předmětem debat; zdejší jednotky neodpovídají žádnému biomarkeru, skóre ani zdravotnímu riziku.",
  "Skutečné stresory se liší velikostí, významem i ovlivnitelností a zotavení závisí na spánku, opoře, zdraví a zdrojích, které model nezachycuje.",
]
references = ["mcewen-1998"]
labels = { frequency = "Stresory za týden", recovery = "Zotavení za den", weeks = "Týden", load = "Nahromaděná zátěž (libovolné jednotky)", peak = "Nejvyšší zátěž", chart = "Spojnicový graf nahromaděné zátěže v libovolných jednotkách za 12 týdnů pro zvolený počet stresorů za týden a denní míru zotavení, s vyznačenou nejvyšší zátěží." }
+++

## Proč modely a proč nejde o předpovědi

Mnoho argumentů v této knihovně se týká času. Úleva přichází teď, ale potíž, která ji vyvolala, se může zítra vrátit. Hněv odeznívá různě rychle podle toho, co člověk dělá. Večer si pamatujeme podle jeho nejlepších či nejhorších okamžiků, ne podle délky. Dav se sladí do rytmu postupně a stres, z něhož se člověk nezotaví, se hromadí týdny. Text tyto procesy popisuje větu po větě; model umožňuje sledovat, jak se odvíjejí, a měnit jejich podmínky.

Modelem se zde rozumí malý soubor výslovných pravidel, která se opakovaně uplatňují na čísla. Jeho hodnota je v průhlednosti. Každý předpoklad je zapsán, takže je vidět, proč křivka stoupá nebo se zplošťuje a která volba daný efekt vytvořila. Pokud s některým předpokladem nesouhlasíte, je nesouhlas přesný: můžete jmenovat pravidlo, které považujete za chybné.

Průhlednost má svou cenu. Modely na této stránce jsou záměrně jednoduché a jejich čísla jsou vymyšlená. Nejsou přizpůsobeny datům, nebyly ověřeny na ničím prožitku a nepředpovídají, co se stane vám ani komukoli jinému. Připomíná-li křivka něco, co jste zažili, ukazuje ta podobnost jen to, že pravidla takový průběh vytvořit dokážou. Neukazuje, že právě tato pravidla jsou důvodem, proč se to stalo vám.

## Jak modely používat odpovědně

Berte každý model jako myšlenkový experiment s připojenou kalkulačkou. Pomáhají tři zvyklosti.

Měňte vždy jen jednu věc. Každý model má dva nebo tři vstupy a nejjasnější poznatky přinese, když ostatní necháte beze změny. Hledejte prahy, kde malá změna jednoho vstupu změní celý průběh, a rozmezí, kde se nic podstatného neděje.

Čtěte předpoklady dříve než graf. Seznam u každého modelu uvádí, co je pevně dané, co zjednodušené a co vynechané. Nápadný výsledek často závisí právě na některém z předpokladů a stránka meze uvádí, abyste je nemuseli odhadovat.

Oddělujte směr dokladů od čísel. Tam, kde model vychází z výzkumu, podporují citované studie směr účinku, například že klidnější činnosti snižují hněv více než prudké. Velikost účinku na obrazovce, jeho časový průběh a přesný tvar křivek jsou volby učiněné kvůli názornosti. Tvrzení této stránky jsou zapsána v [registru důkazů](@/evidence/index.cs.md) i se zdroji a mírou jejich síly.

## Pozadí: smyčka úlevy

[Negativní posílení](../slovnik/#negative-reinforcement) je proces, při němž se chování stává pravděpodobnějším, protože odstraňuje něco nepříjemného. Nevyžaduje, aby chování řešilo zdroj nepříjemného stavu; stačí, že po něm přijde úleva. Zážitkové vyhýbání, tedy snaha uniknout nechtěnému vnitřnímu prožitku, bylo navrženo jako proces společný mnoha psychickým obtížím (Hayes a kol., 1996).

Model zachycuje učení korekční aktualizací z Rescorlova–Wagnerova modelu (Rescorla a Wagner, 1972), v němž každá epizoda učení uzavře část rozdílu mezi tím, co je naučeno, a tím, co naučit lze. Zde se rozdíl v každé epizodě zmenší o 15 %, úměrně velikosti úlevy, takže silná úleva zpočátku buduje nutkání rychle a s blížící se hranicí pomaleji. Protože se tíseň před každou epizodou vrací na stejnou úroveň, může graf ukázat sílící návyk vedle nezměněné potíže. Právě tento průběh popisuje [Výzkumná poznámka 04](@/research/relief-is-not-resolution/index.cs.md) jako rozdíl mezi [úlevou a vyřešením](../slovnik/#relief-vs-resolution). Když se příčina změní, výchozí úroveň klesne a nutkání, které už není posilováno, slábne.

## Pozadí: ventilace a vzrušení v čase

[Hydraulická](../slovnik/#hydraulic-model) představa hněvu jako tlaku, který je třeba vypustit, předpovídá, že po bušení do něčeho bude člověk klidnější. Experimentální doklady ukazují opačným směrem. [Ventilace](../slovnik/#venting) spojená s ruminací o provokaci zvýšila hněv a agresi oproti nečinnosti (Bushman, 2002) a v metaanalýze činností pro zvládání hněvu snižovaly hněv a agresi ty, které tlumily [vzrušení](../slovnik/#arousal), kdežto ty, které vzrušení zvyšovaly, byly celkově neúčinné (Kjærvik a Bushman, 2024).

Model tato zjištění ukazuje jako tři průběhy během půl hodiny. Nejde o naměřený popis toho, jak hněv odeznívá, a časové konstanty jsou vymyšlené. Zachovává však pořadí: snížení vzrušení končí lépe než čekání a zvýšení vzrušení nekončí o nic lépe než čekání. Samostatná křivka vzrušení připomíná, že prudká činnost se může prožívat jako vybití, a přitom nechat tělo aktivované. Studie a jejich meze shrnuje [Výzkumná poznámka 02](@/research/venting-hypothesis/index.cs.md).

## Pozadí: vrchol a konec ve vzpomínce na nepohodlí

Zpětné hodnocení nesčítá zážitek okamžik po okamžiku. Účastníci, kteří hodnotili filmové ukázky, vynášeli celková hodnocení, která délka ukázek téměř neovlivnila (Fredrickson a Kahneman, 1993); tento jev se nazývá zanedbávání trvání. V experimentu se studenou vodou prodloužení nepříjemného pokusu o mírnější, stále nepříjemný závěr způsobilo, že právě tento pokus chtěla většina účastníků zopakovat (Kahneman a kol., 1993). [Pravidlo vrcholu a konce](../slovnik/#peak-end-rule) tento vzorec shrnuje: zapamatované nepohodlí sleduje nejhorší a závěrečný okamžik.

Model tuto aritmetiku zviditelňuje. Můžete sestavit epizodu, jejíž celkové nepohodlí roste, zatímco její zapamatovaná podoba se zlepšuje. Pro katarzi to má přímý význam: intenzivní noc, která skončí na vrcholu, si člověk může pamatovat jako obnovující víc, než by odpovídalo jejímu průběhu, a taková vzpomínka může ovlivnit rozhodnutí vyhledat ji znovu.

## Pozadí: synchronie spřažených oscilátorů

Synchronizace se objevuje v tak odlišných systémech, jako jsou blikající světlušky, buňky srdečního pacemakeru nebo oscilující chemické reakce. Kuramotův model zachycuje, co mají tyto systémy společné: mnoho rytmů s různými vlastními tempy, z nichž každý je ovlivňován ostatními. Strogatz (2000) shrnul čtvrt století práce na tomto modelu, který vykazuje přechod: pod kritickou silou vazby zůstává populace nekoherentní a nad ní se některé oscilátory spontánně synchronizují, zatímco jiné se dál rozcházejí.

Model je zařazen jako analogie [interpersonální synchronie](../slovnik/#interpersonal-synchrony), zkušenosti pohybovat se v rytmu s ostatními. Analogie je užitečná zejména v jednom bodě: synchronie je vlastností skupiny, která vzniká ze vzájemného působení, aniž by ji kdokoli dirigoval. Stejně důležité jsou její meze. Oscilátory nemají pocity ani vztahy. Zjištění o lidech, že ti, kdo jednali synchronně, poté více spolupracovali (Wiltermuth a Heath, 2009) a že synchronní tanec zvyšoval práh bolesti a sounáležitost se skupinou (Tarr a kol., 2015), pocházejí z experimentů s lidmi a na této matematice nezávisejí. Podrobněji je rozebírá [Výzkumná poznámka 03](@/research/collective-synchrony/index.cs.md).

## Pozadí: alostatická zátěž a zotavení

McEwen (1998) popsal mediátory stresu jako krátkodobě ochranné a škodlivé tehdy, když jsou aktivovány příliš často nebo se nevypínají účinně. [Alostatická zátěž](../slovnik/#allostatic-load) označuje tuto kumulativní cenu. Model myšlenku zjednodušuje na přírůstek a zotavení. Při častých stresorech a pomalém zotavení zátěž roste celé týdny; při stejných stresorech a rychlejším zotavení se ustálí na nižší úrovni. Poučení je kvalitativní: to, jak rychle se člověk zotavuje, může být stejně důležité jako to, jak často stres přichází, a jediná obnovující událost sníží zátěž jen nakrátko, pokud se tempo přicházejících stresorů nezmění. Výzkum stresu a sociální opory popisuje [Výzkumná poznámka 09](@/research/stress-and-social-buffering/index.cs.md).

## Co modely zachytit nedokážou

Každý model na této stránce vynechává to, na čem v životě záleží nejvíc.

Chybějí rozdíly mezi lidmi. Modely uplatňují na všechny stejná pravidla, kdežto lidé se liší temperamentem, historií, zdravím, citlivostí na stres i způsoby, jak se s obtížemi vyrovnávají. Zjištění na úrovni skupiny popisuje průměr napříč účastníky a neříká, jak zareaguje konkrétní člověk.

Chybí kontext. Úlevné chování na večírku, v krizi nebo po ztrátě je v modelu stejné číslo, v životě však jiná událost. Kdo je přítomen, co je v sázce a jaké možnosti člověk má, není proměnnou v žádné z těchto simulací.

Chybí význam. Modely počítají jednotky tísně, hněvu, nepohodlí, fáze a zátěže. Nedokážou zachytit, co zážitek znamená pro toho, kdo ho prožívá, jak lidé dávají smysl tomu, co se jim stalo, ani proč epizoda, která v grafu vypadá stejně, může být pro jednoho člověka zlomem a pro jiného opakováním.

Chybí změna jednáním. Ve smyčce úlevy se příčina mění náhodným losem. V životě se příčiny mění, protože lidé mluví, rozhodují se, žádají o pomoc, odcházejí, napravují nebo je podpoří druzí. Nic z toho modelováno není a právě tuto část za nikoho žádná simulace neudělá.

Z těchto důvodů modely nejsou nástrojem k posuzování sebe ani kohokoli jiného. Je-li tíseň, hněv nebo stres dlouhodobý či silný, rozhovor s někým, komu důvěřujete, a v případě potřeby s kvalifikovaným odborníkem řekne víc než jakákoli křivka.

## Kde číst dál

[Stránka o metodách](@/methods/index.cs.md) vysvětluje, proč signály a modely podporují inference se stanovenou mírou nejistoty, a nikoli závěry o konkrétním člověku, a [přehled dokladů](@/evidence/index.cs.md) ukazuje, jak je každé tvrzení této stránky hodnoceno a revidováno.

Výzkumné poznámky nabízejí empirické pozadí jednotlivých modelů: [úleva není řešení](@/research/relief-is-not-resolution/index.cs.md), [hypotéza ventilace](@/research/venting-hypothesis/index.cs.md), [kolektivní synchronie](@/research/collective-synchrony/index.cs.md) a [stres a sociální opora](@/research/stress-and-social-buffering/index.cs.md).

Teoretické stránky rozvádějí myšlenky, z nichž modely vycházejí: [učení, vyhýbání a úleva](@/theory/learning-avoidance-and-relief/index.cs.md), [alostáza a stres](@/theory/allostasis-and-stress/index.cs.md) a [kolektivní emoce a rituál](@/theory/collective-emotion-and-ritual/index.cs.md).
