+++
title = "Catharsis as a Service™"
description = "Umělecké dílo a knihovna důkazů o kolektivní katarzi: co je katarze, proč úleva není řešení, co ukazuje psychologický výzkum a praktické rady seřazené podle síly důkazů."
template = "index.html"

[extra]
featured = "artifacts/catharsis-as-a-service/index.md"

[extra.purpose]
body = [
  "Ukázka je jen tak dobrá jako záznamy, které za ní stojí, a proto tato stránka o důvěru nežádá. Historie sestavení, zdroje každého tvrzení i pravidla, podle nichž práce probíhala, jsou veřejné a každá položka níže odkazuje na záznam, který popisuje.",
  "Téma je zpracované jako odborná práce, ne jako marketing. Knihovna shrnuje klasické prameny a recenzovaný výzkum na úrovni skupin, hodnotí sílu důkazů a uvádí jejich limity. Jde o vzdělávací publikaci, ne o zdravotnický zdroj, a nikoho neposuzuje ani mu individuálně neradí.",
]
label = "Proč web vznikl"
heading = "Případová studie dozorovaného a ověřitelného vývoje."
lead = "Catharsis as a Service™ vznikl především jako technická ukázka a případová studie: pro Majordomus (majordomus.dev), dozorovou vrstvu pro vývoj s pomocí AI, a pro Prismatic jako příklad vývoje, v němž má každé veřejné tvrzení zdroj, hodnocení a dá se ověřit. Umělecké dílo a výzkumná knihovna jsou materiálem, na kterém se obojí předvádí."
verify_label = "Ověřte si to sami"
verify = [
  { title = "Zdrojový kód", text = "Repozitář s úplnou historií commitů, validátory, testy a definicemi workflow.", url = "https://github.com/korczis/catharsis-as-a-service" },
  { title = "Běhy pipeline", text = "Validace, nasazení a ověření proti živé URL pro každý push do main.", url = "https://github.com/korczis/catharsis-as-a-service/actions" },
  { title = "Vydání", text = "Vydání se publikuje až poté, co živý web projde ověřením.", url = "https://github.com/korczis/catharsis-as-a-service/releases" },
  { title = "Stav sestavení", text = "Revize a verze obsahu tohoto sestavení a aktuální statistiky registru důkazů.", path = "status/index.md" },
  { title = "Registr důkazů", text = "Každé tvrzení s typem, úrovní důkazů, jistotou, zdroji a datem revize.", path = "evidence/index.md" },
  { title = "API", text = "Verzovaný export stránek, registru důkazů a slovníku pojmů ve formátu JSON.", file = "api/v1/index.json" },
]

[[extra.purpose.cases]]
label = "Případ 01 · Majordomus"
title = "Vývoj s pomocí AI pod dozorem"
text = "Web napsal AI agent pro programování řízený jedním člověkem. Majordomus každé úloze vymezil deklarované cesty, zaznamenával její průběh a za dokončenou ji přijal, až když prošel její ověřovací příkaz."
points = [
  "Dvě chyby rozsahu úlohy a jedno selhání inicializace byly nahlášeny lokálně ještě před prvním pushem; zaznamenanou časovou osu uvádí poznámka o metodě.",
  "Pravidla, workflow a kontext pro jakéhokoli AI pracovníka jsou uložené v adresáři .ai/, který nezávisí na poskytovateli a verzuje se spolu s kódem.",
  "Nasazení se považuje za dokončené až poté, co workflow Pages ověří živou URL, a vydání vzniká až po této kontrole.",
]
links = [
  { label = "Poznámka o metodě", path = "research/method-majordomus/index.md" },
  { label = "Technické články", path = "engineering/_index.md" },
  { label = "majordomus.dev", url = "https://majordomus.dev" },
]

[[extra.purpose.cases]]
label = "Případ 02 · Prismatic"
title = "Vývoj, který lze ověřit"
text = "Pro obsah platí stejný standard jako pro kód. Tvrzení lze zveřejnit, jen když ho registr důkazů zaznamenává s posouzenými zdroji, s úrovní důkazů nejvýše rovnou jeho nejsilnějšímu zdroji a s datem revize, které ještě neuplynulo; jinak sestavení selže."
points = [
  "Články z odborných časopisů musí mít v bibliografii DOI a odkazy se kontrolují proti Crossrefu.",
  "Přehnaná tvrzení uvedená ve standardech obsahu, chybějící klinická upozornění a rozdíly mezi anglickou a českou verzí neprojdou validací nebo end-to-end testy.",
  "Každý příkaz zmíněný v dokumentaci je registrovaný spolu s testem, který ho spouští.",
]
links = [
  { label = "Registr důkazů", path = "evidence/index.md" },
  { label = "Metody", path = "methods/index.md" },
  { label = "Registr příkazů", path = "commands/index.md" },
]

[extra.intent]
body = [
  "Dílo vychází z běžné zkušenosti. Po koncertu, dlouhém běhu, hádce, která skončí křikem, nebo po noci protančené s ostatními se mnoho lidí cítí lehčeji a ten pocit je skutečný, i když je tělo stále aktivované. Web zpochybňuje až úsudek, který často následuje: že lehkost znamená, že to, co člověka tížilo, je vyřešené.",
  "Na tom úsudku záleží, protože ovlivňuje chování. Když se úleva čte jako vyřešení, činnost, která ulevuje, se opakuje pokaždé, když se tlak vrátí, a tlak se vrací, protože se na jeho zdroji nic nezměnilo. Teorie učení tomu říká negativní posílení; běžná řeč mluví o zvládání, které potichu přestalo fungovat.",
  "Knihovna nevystupuje proti úlevě. Odděluje tři otázky, které obvykle splývají v jednu: co se změnilo v těle, co se změnilo v porozumění a co se změnilo v situaci. Každá výzkumná poznámka, teoretický text i rada jsou napsané tak, aby tyto otázky držely od sebe.",
]
label = "Záměr"
heading = "Úleva není řešení."
lead = "Catharsis as a Service™ je umělecké dílo a knihovna důkazů o jedné rozšířené záměně: o přesvědčení, že pocit uvolnění znamená, že se něco vyřešilo."
problem_label = "Problém, kterým se zabývá"
problem = "Současná kultura prodává emoční uvolnění jako řešení: noc venku, playlist, výkřik, nákup. Pocit úlevy je skutečný a často cenný. Potíž je v tom, za co je považován. Když se úleva bere jako řešení, lidé opakují to, co pomáhá v danou chvíli, a diví se, když se původní potíž vrátí. Psychologický výzkum tuto mezeru zkoumá desítky let, jeho zjištění se však jen zřídka dostanou tam, kde se uvolnění prodává."
cta_research = "Číst výzkum"
cta_advice = "Otevřít knihovnu rad"
audience_label = "Pro koho je"
audience = [
  "Pro lidi, kteří se spoléhají na intenzivní zážitky, aby něco zvládli, a chtějí rozumět tomu, co tyto zážitky dělají a co ne.",
  "Pro čtenáře, které zajímá psychologie emocí, regulace emocí a kolektivní chování.",
  "Pro umělce, designéry a technology, kteří pracují s jazykem dat, duševní pohody a sebeoptimalizace.",
]
approach_label = "Přístup"
approach = [
  { title = "Dílo", text = "Plakát a interaktivní stránka, které představí kolektivní euforii a poté ji popíší jako transakci služby." },
  { title = "Důkazy", text = "Výzkumné poznámky, které shrnují klasické prameny a recenzované studie, každá se svou literaturou." },
  { title = "Praxe", text = "Rady seřazené podle síly důkazů, s konkrétními kroky a výslovně uvedenými limity." },
]

[extra.concept]
body = [
  "Slovo urazilo od svého původu dlouhou cestu. U Aristotela popisovalo, co tragédie dělá s publikem, a badatelé se dodnes neshodnou, zda měl na mysli očištění, pročištění, nebo vyjasnění emocí. Breuer a Freud si ho vypůjčili pro klinickou metodu, v níž vybavení bolestné vzpomínky se silnou emocí zmírnilo příznaky, alespoň na čas.",
  "Populární kultura dvacátého století z té myšlenky udělala hydraulický obraz: emoce se hromadí jako tlak a musí ven, jinak vybuchne jinde. Obraz je intuitivní a v radách o hněvu, zármutku a stresu dodnes běžný. Experimentální psychologie ho mnohokrát testovala a v prosté podobě neobstál.",
  "Zůstává užší a užitečnější myšlenka. Vyjádření emoce spíše pomáhá, když něco přidá: podporu druhých, nové porozumění, jiné zhodnocení situace nebo rozhodnutí jednat. Vyjádření, které emoci jen znovu přehrává, ji spíše udržuje.",
]
label = "Co je katarze"
heading = "Prožívané uvolnění a otevřená empirická otázka."
definition = "V tomto projektu je katarze subjektivně prožívané uvolnění emočního napětí, které následuje po vyjádření, fyzické námaze nebo ponoření do zážitku. Zda se změní příčina tohoto napětí, je samostatná otázka a odpověď závisí na emoci, metodě i kontextu."
lenses = [
  { years = "asi 335 př. n. l.", title = "Klasický", text = "Aristotelés popisuje tragédii jako umění, které skrze soucit a strach dosahuje katarze takových emocí. Odborníci se dodnes přou, zda měl na mysli očistu, zušlechtění nebo objasnění." },
  { years = "1895", title = "Klinický", text = "Katarzní metoda Breuera a Freuda ulevovala od příznaků výbojem emocí, tzv. abreakcí. Freud od ní později upustil, mimo jiné proto, že úleva byla často jen dočasná." },
  { years = "1986 do dneška", title = "Empirický", text = "Kontrolované studie ukazují, že ventilace hněvu zvyšuje agresi, zatímco vyjádření emocí pomáhá, když přináší sociální oporu, porozumění nebo regulaci." },
]
timeline_title = "Časová osa pojmu katarze"
timeline_description = "Šest milníků od Aristotelovy Poetiky po výzkum synchronie a sociálních vazeb."
timeline_caption = "Jak se katarze přesunula z estetiky ke klinické metodě a k empirické výzkumné otázce."
timeline = [
  { year = "asi 335 př. n. l.", label = "Aristotelés, Poetika: katarze skrze soucit a strach" },
  { year = "1895", label = "Breuer a Freud: katarzní metoda a abreakce" },
  { year = "1986", label = "Pennebaker a Beall: psaní o traumatu a zdraví" },
  { year = "1998", label = "Gross: rámec regulace emocí" },
  { year = "1999–2002", label = "Bushman a kolegové: ventilace hněvu nesnižuje agresi" },
  { year = "2009–2015", label = "Výzkum synchronie: sdílený rytmus a sociální vazby" },
]
link = "research/what-is-catharsis/index.md"
cta = "Historie a definice"

[extra.mechanism]
body = [
  "Model je záměrně jednoduchý, aby šlo každý krok porovnat s výzkumem. Opakování a rytmus zužují pozornost; pohyb v souladu s ostatními souvisí s pocitem blízkosti a vyšším prahem bolesti; po fyzických a hudebních vrcholech přichází silný pocit uvolnění. Žádný z těchto kroků nevyžaduje, aby se původní potíž změnila.",
  "Smyčka se uzavírá, protože úleva je odměnou. Cokoli úlevě spolehlivě předchází, se příště stane pravděpodobnějším, a proto lze tentýž rituál vyhledávat znovu a znovu. Na stránce interaktivních modelů můžete měnit velikost úlevy i šanci, že se příčina změní, a sledovat, jak nutkání opakovat roste, nebo slábne.",
]
label = "Jak to funguje"
heading = "Smyčka úlevy."
intro = "Artefakt modeluje kolektivní katarzi jako čtyřfázový proces. Každá fáze má doložený psychologický nebo fyziologický základ a žádná z nich nevyžaduje, aby se změnil původní problém."
steps = [
  { name = "Nevyřešený stav", text = "Stres, zármutek, hněv nebo úzkost s příčinou, která leží mimo daný okamžik." },
  { name = "Opakování", text = "Rytmus a opakovaný pohyb zužují pozornost a na čas přerušují ruminaci." },
  { name = "Synchronizace", text = "Pohyb v souladu s druhými zvyšuje blízkost a spolupráci a zvyšuje práh bolesti." },
  { name = "Výboj", text = "Námaha a hudební vrcholy přinášejí akutní zlepšení nálady a silný pocit uvolnění." },
]

[extra.mechanism.loop]
title = "Smyčka úlevy"
description = "Nevyřešený stav vede k opakování, synchronizaci a výboji. Výboj přináší dočasnou úlevu a nezměněný stav vede zpět na začátek."
caption = "Smyčka vyplývající z negativního posilování: úleva zvyšuje pravděpodobnost, že se posloupnost zopakuje, zatímco nevyřešený stav se vrací."
input = "Nevyřešený stav"
repetition = "Opakování"
synchronization = "Synchronizace"
discharge = "Výboj"
relief = "Dočasná úleva"
loop = "příčina beze změny"

[extra.mechanism.curve]
title = "Dva průběhy tísně v čase"
description = "Spojnicový graf s časem na vodorovné ose a tísní na svislé ose. Jedna křivka vrcholí, během výboje klesá a vrací se na výchozí úroveň; druhá postupně klesá na nižší úroveň."
caption = "Výboj versus zpracování. Koncepční ilustrace argumentu, nikoli naměřená data."
axis_time = "čas"
axis_arousal = "tíseň"
baseline = "výchozí úroveň"
discharge = "výboj, pak návrat"
processing = "zpracování"

[extra.evidence]
body = [
  "Každé tvrzení webu je zapsané v registru důkazů s typem, úrovní důkazů od A do E, hodnocením jistoty a datem, do kdy se musí znovu ověřit. Tvrzení nikdy nemá vyšší úroveň než jeho nejsilnější zdroj a sestavení selže, jakmile datum revize uplyne.",
  "Úrovně popisují sílu použitých výzkumných designů, ne důležitost tématu. Mnoho z toho, na čem u katarze, zármutku a kolektivních zážitků záleží, bylo zkoumáno převážně korelačními nebo kvalitativními metodami, a registr to říká otevřeně, místo aby taková zjištění vydával za experimenty.",
]
label = "Důkazy"
heading = "Co ukazuje výzkum."
intro = "Výzkumné poznámky oddělují, co studie zjistily, od toho, co zůstává nejisté. Celý projekt rámují čtyři zjištění."
read = "Číst poznámku"
notes_label = "Výzkumné poznámky"
cta = "Všechny výzkumné poznámky"
cta_ledger = "Registr důkazů"
cta_methods = "Metody"
cta_glossary = "Slovník pojmů"
findings = [
  { title = "Ventilace zvyšuje agresi", text = "Bušení do boxovacího pytle při myšlenkách na provokaci vedlo k většímu hněvu a agresi než tiché sezení.", source = "Bushman, 2002", path = "research/venting-hypothesis/index.md" },
  { title = "Synchronie buduje vazby", text = "Synchronizovaný skupinový tanec zvýšil práh bolesti a uváděnou blízkost ke skupině.", source = "Tarr a kol., 2015", path = "research/collective-synchrony/index.md" },
  { title = "Samotné mluvení nestačí", text = "Mluvení o emočním zážitku působilo užitečně, ale bez kognitivní práce nesnížilo jeho emoční dopad.", source = "Zech a Rimé, 2005", path = "research/crying-and-sharing/index.md" },
  { title = "Debriefing nepředešel PTSP", text = "Přehled Cochrane nenašel preventivní účinek jednorázového debriefingu a našel určité známky škody.", source = "Rose a kol., 2002", path = "research/clinical-perspectives/index.md" },
]

[extra.library]
body = [
  "Rady jsou psané pro dospělé, kteří přemýšlejí o svých vlastních zvycích. Každá uvádí, jak silné důkazy za ní stojí, co dělat v konkrétních krocích a kde doporučení přestává platit. Žádná nenahrazuje individuální pomoc a několik z nich výslovně jmenuje situace, v nichž je správným dalším krokem odborník.",
]
label = "Rady"
heading = "Od důkazů k praxi."
intro = "Doporučení, každé seřazené podle síly důkazů a doplněné konkrétními kroky a výslovnými limity. Jde o obecné vzdělávání, ne o léčebný plán."
cta = "Otevřít knihovnu rad"

[extra.making]
body = [
  "Dozorová vrstva práci v malém zpomalila a ve velkém zrychlila. Každý úkol měl deklarovaný rozsah, každé tvrzení o dokončení mělo ověřovací příkaz a každé nasazení bylo před vydáním zkontrolováno proti živému webu. Chyby se objevily jako lokální nálezy, ne jako rozbité stránky.",
  "Koncepční obrazovky ukazují, kam nástroje směřují: cockpit nad sezeními, pravidly, testy a milníky. Jejich data jsou ilustrativní. Skutečnými záznamy tohoto projektu jsou commity, běhy pipeline a poznámka o metodě.",
]
label = "Jak to vzniklo"
heading = "První vydání za jedno sezení. Ověřeno před každým tvrzením."
intro = "Web napsal AI agent pro programování řízený jedním člověkem a dozorovaný Majordomem, kontrolní vrstvou, která vymezuje rozsah každé úlohy, zaznamenává průběh a odmítne uzavřít práci, která nebyla ověřena na živém webu."
cta = "Číst poznámku o metodě"
cta_case = "Případová studie Majordomu"
cta_engineering = "Technické články"
stats = [
  { value = "51 min 36 s", label = "od prázdného repozitáře k prvnímu ověřenému vydání" },
  { value = "19 min 19 s", label = "od inicializace Majordomu k tomuto vydání" },
  { value = "2 min 57 s", label = "od pushe k ověřenému a publikovanému vydání" },
  { value = "7 / 7", label = "jobů pipeline prošlo při prvním nasazení" },
]
points = [
  "Dvě chyby rozsahu úlohy a jedno selhání inicializace byly zachyceny lokálně ještě před prvním pushem.",
  "Každý push do main se validuje, nasadí, ověří ve skutečném prohlížeči proti živé URL a automaticky vydá.",
  "Neuvádí se žádný násobek zrychlení: chyběla kontrolní podmínka a poznámka o metodě vysvětluje, co záznamy ukázat mohou a co ne.",
]

[extra.faq]
label = "Otázky"
heading = "Časté otázky."
items = [
  { question = "Co je katarze?", answer = "Katarze je představa, že vyjádření emoce snižuje její intenzitu. Pojem pochází z Aristotelovy Poetiky a Breuer s Freudem ho později použili pro klinickou metodu emočního výboje. Výzkum ukazuje, že pocit uvolnění je skutečný, zatímco jeho vliv na samotnou emoci závisí na emoci a na tom, zda vyjádření zahrnuje oporu, porozumění nebo regulaci." },
  { question = "Je ventilace hněvu zdravá?", answer = "Kontrolované experimenty zjistily, že ventilace hněvu při soustředění na provokaci zvýšila hněv a agresi ve srovnání s nicneděláním. Spolehlivěji hněv snižuje nejprve snížit vzrušení a pak situaci přehodnotit nebo o ní uvažovat s odstupem." },
  { question = "Proč je tanec s dalšími lidmi tak příjemný?", answer = "Synchronní pohyb zvyšuje sympatie, blízkost a spolupráci. Ve studii skupinového tance zvýšily synchronie i fyzická námaha práh bolesti, který se používá jako nepřímý ukazatel aktivity endorfinů, a v zobrazovací studii souvisely vrcholné okamžiky hudebního prožitku s uvolněním dopaminu v oblastech spojených s odměnou (Salimpoor a kol., 2011)." },
  { question = "Když je úleva dočasná, je bezcenná?", answer = "Ne. Úleva podporuje zotavení, energii i propojení s druhými a má hodnotu sama o sobě. Rozlišení je důležité proto, že se od úlevy často očekává něco, co udělat nemůže: změnit podmínky, které tíseň vyvolaly." },
  { question = "Měří tento web moje emoce?", answer = "Ne. Každá zobrazená metrika je umělecká hodnota, nikoli měření. Web neobsahuje žádnou analytiku, trackery ani cookies a jeho zdrojový kód je veřejný." },
  { question = "Jde o lékařskou radu?", answer = "Ne. Obsah je vzdělávací a vychází z publikovaného výzkumu. Pokud potíže přetrvávají, narušují každodenní život nebo zahrnují myšlenky na sebepoškození, obraťte se na kvalifikovaného odborníka nebo místní tísňovou linku." },
  { question = "Jak web vznikl a jak dlouho to trvalo?", answer = "První vydání vzniklo během jednoho pracovního sezení; napsal ho AI agent pro programování pod dozorem Majordomu (majordomus.dev), 51 minut a 36 sekund po založení repozitáře. Další fáze prošly stejnou dozorovanou smyčkou a jsou uvedeny v historii vydání. Poznámka o metodě dokumentuje časovou osu, druhy zadání i to, co z toho vyvodit nelze." },
  { question = "Proč tento web existuje?", answer = "Především jako technická ukázka a případová studie: Majordomu, dozorové vrstvy pro vývoj s pomocí AI, a standardu ověřitelné práce Prismatic, v němž má každé veřejné tvrzení zdroj, hodnocení síly důkazů a datum revize. Umělecké dílo i výzkumná knihovna jsou materiálem, na kterém ukázka stojí, a oba tomuto standardu podléhají." },
]

[extra.making.screens]
id = "making-cockpit"
caption = "Koncepční obrazovky cockpitu Majordomu pro sezení, testy a milníky. Data v nich jsou ilustrativní a nepopisují tento projekt; naměřenou časovou osu uvádí poznámka o metodě."
items = [
  { src = "assets/majordomus/cockpit-sessions.png", title = "Sezení", alt = "Koncepční obrazovka pohledu Sezení v cockpitu Majordomu: seznam pracovních sezení a časová osa jednoho sezení od začátku po aktualizaci dokumentace, se zdroji kontextu, které načetlo.", caption = "Každé sezení uchovává časovou osu, zdroje kontextu, rozhodnutí a předávku." },
  { src = "assets/majordomus/cockpit-tests.png", title = "Testy", alt = "Koncepční obrazovka pohledu Testy v cockpitu Majordomu: počty úspěšných a neúspěšných testů, vývoj výsledků, pokrytí, kvalitativní brány a živý výstup testů.", caption = "Běhy testů, selhání a kvalitativní brány na jednom místě, propojené s issues a commity." },
  { src = "assets/majordomus/cockpit-milestones.png", title = "Milníky", alt = "Koncepční obrazovka pohledu Milníky v cockpitu Majordomu: tři milníky s ukazateli postupu, graf kumulativního postupu, časová osa a závislosti.", caption = "Milníky s postupem, harmonogramem a závislostmi odvozenými z plánu issues." },
]

[extra.statement]
body = [
  "Fyziologické zotavení je normální a cenný proces. Po stresové reakci se srdeční frekvence, krevní tlak i stresové hormony vracejí k výchozí úrovni a dlouhodobé selhání tohoto návratu je spojováno s kumulativním opotřebením organismu. Zotavení stojí za to chránit.",
  "Zotavení ale popisuje organismus, ne okolnosti. Člověk se může vyspat, vyběhat, vyplakat, vyzpívat nebo vytančit zpět do klidu, zatímco nájem je pořád nezaplacený, vztah pořád nenapravený a ztráta pořád ztrátou. Řádek úleva zaznamenána ≠ příčina vyřešena připomíná, že je potřeba ptát se na obojí.",
]
label = "Teze"
lines = ["Tělo může změnit stav,", "aniž se změní", "svět kolem něj."]
text = "Srdeční frekvence se zklidní, svaly povolí, dav se rozejde a člověk popisuje úlevu. To všechno může být skutečné a velkou část lze zaznamenat. Nic z toho ale neukazuje, že se změnil dluh, konflikt, ztráta nebo pracovní podmínky, které za potížemi stojí. V téhle mezeře je celý argument díla, vyslovený co nejprostěji."
formula = "úleva zaznamenána ≠ příčina vyřešena"
cta_methods = "Časový model"
cta_note = "Úleva není vyřešení"

[extra.venting]
body = [
  "To rozlišení má praktické důsledky. Rady typu mlátit do polštářů, křičet do deky nebo vybít vztek vyčerpávající námahou stojí na hydraulickém obrazu. Kontrolované studie naznačují, že spolehlivější cestou ke klidnějším pocitům a menší agresi je nejprve vzrušení snížit a teprve potom o situaci přemýšlet s určitým odstupem.",
  "Nic z toho nedělá pohyb ani silné emoce podezřelými. Cvičení má pro náladu vlastní přínosy a křik na koncertě není klinický problém. Pointa je užší: když je cílem hněv zmírnit, metoda, která nejvíc připomíná uvolnění, není ta, která funguje nejlépe.",
]
label = "Katarze není ventilace"
heading = "Uvolnění není totéž co vybít si vztek."
lead = "Katarze označuje prožívané uvolnění. Ventilace označuje strategii: vyjádřit hněv aktivitou s vysokým vzrušením v očekávání, že tím odezní. Obojí se často zaměňuje a výzkum je od sebe odlišuje."
contrast = [
  { label = "Zvyšování vzrušení", title = "Aktivity, které vzrušení zvyšují", value = "g = −0,02", text = "Napříč studiemi aktivity, které zvyšovaly fyziologické vzrušení, spolehlivě nesnižovaly hněv ani agresi; interval spolehlivosti zahrnuje nulu." },
  { label = "Snižování vzrušení", title = "Aktivity, které vzrušení snižují", value = "g = −0,63", text = "Aktivity, které vzrušení snižovaly, byly napříč studiemi a vzorky spojeny se středně velkým poklesem hněvu a agrese." },
]
stats = [
  { value = "154", label = "studií" },
  { value = "184", label = "vzorků" },
  { value = "10 189", label = "účastníků" },
]
source = "Kjærvik, S. L., & Bushman, B. J. (2024). Metaanalýza v časopise Clinical Psychology Review, 109, 102414."
meaning = "Pocit uvolnění po křiku nebo bušení do něčeho je skutečný. Důkazy ale nepodporují očekávání, že vybití vzrušení zmenší hněv, který přijde potom. Lépe funguje nejprve vzrušení snížit a teprve pak pracovat se situací."
cta_note = "Hypotéza ventilace"
cta_advice = "Nechte hněv vychladnout"

[extra.questions]
body = [
  "Dobré otázky drží úlevu a vyřešení od sebe, aniž by jedno či druhé zlehčovaly. Nejsou to testy, které je třeba splnit. Jsou to způsoby, jak si všimnout, zda zvyk ještě dělá to, k čemu ho používáme.",
]
label = "Lepší otázky"
heading = "Lepší otázky než: pomohlo to?"
intro = "Zda byl zážitek příjemný, je nejsnazší a zároveň nejméně informativní otázka. Tyto otázky vycházejí z výzkumu regulace emocí a z toho, co se děje po úlevě."
items = [
  { instead = "Je mi líp?", better = "Co přesně se změnilo: tělo, nálada, porozumění, nebo situace?" },
  { instead = "Mám to všechno pustit ven?", better = "Snižuje vyjádření mé vzrušení a někam vede, nebo mě nutí provokaci znovu přehrávat?" },
  { instead = "Proč se to pořád vrací?", better = "Čemu se mi díky úlevě snáz vyhýbalo?" },
  { instead = "Je to normální?", better = "Trvá to déle, sílí to, nebo to narušuje spánek, práci či vztahy?" },
  { instead = "Jak ten stav zažít znovu?", better = "Které části toho zážitku, třeba pohyb, hudbu nebo lidi, můžu přenést do běžného týdne?" },
  { instead = "Spravil to ten večer venku?", better = "Jaký je jeden konkrétní krok k příčině a kdo by ho mohl udělat se mnou?" },
]

[extra.boundary]
body = [
  "Popisy výzkumu se tu týkají skupin lidí zkoumaných za určitých podmínek. Nemohou říct, čím prochází konkrétní čtenář, ani co mu pomůže. Pokud je to, co prožíváte, vážné, dlouhotrvající nebo děsivé, nejužitečnějším krokem je mluvit s kvalifikovaným člověkem, který vaši situaci vyslechne.",
]
label = "Klinická hranice"
heading = "Kde tento web končí."
text = "Jde o vzdělávací publikaci. Shrnuje výzkum na úrovni skupin, nemůže posoudit jednotlivce a nic na něm vás neměří. Některé zkušenosti potřebují kvalifikovaného odborníka, ne článek."
signs_label = "Obraťte se na kvalifikovaného odborníka, pokud"
signs = [
  "potíže trvají týdny nebo stále sílí",
  "je narušený spánek, práce, studium nebo vztahy",
  "úleva závisí na alkoholu, drogách nebo riskantním chování",
  "traumatická událost se stále vrací v podobě dotěrných vzpomínek, nočních můr nebo vyhýbání",
]
urgent = "Pokud máte myšlenky na ublížení sobě nebo někomu jinému, kontaktujte hned místní tísňovou linku nebo krizovou linku."
cta_advice = "Po traumatické události"
cta_evidence = "Jak se tvrzení hodnotí"

[extra.explore]
label = "Prozkoumejte"
heading = "Devět cest do knihovny."
intro = "Dílo klade otázku; knihovna na ni odpovídá do různé hloubky. Začněte tam, kde je vaše otázka: u zjištění, teorie, modelu, se kterým můžete hýbat, praktického kroku, hodnocení tvrzení, pojmu, nebo hledání napříč vším."
items = [
  { title = "Výzkumné poznámky", text = "Co studie zjistily o ventilaci, synchronii, pláči, zármutku, spánku, pohybu a měření, s limity uvedenými hned vedle zjištění.", path = "research/_index.md" },
  { title = "Teorie", text = "Rámce za zjištěními: teorie katarze, procesní model regulace emocí, teorie hodnocení, konstruované emoce, učení vyhýbání, alostáza a rituál.", path = "theory/_index.md" },
  { title = "Interaktivní modely", text = "Pět malých simulací úlevy, vzrušení, vzpomínky na nepohodlí, synchronie a stresové zátěže, označených jako ilustrace, ne předpovědi.", path = "models/index.md" },
  { title = "Rady", text = "Doporučení s hodnocením důkazů, konkrétními kroky a výslovnými limity, psaná pro dospělé, kteří přemýšlejí o svých zvycích.", path = "advice/_index.md" },
  { title = "Registr důkazů", text = "Každé tvrzení s typem, úrovní, jistotou, zdroji a datem revize a přehled toho, co se změnilo.", path = "evidence/index.md" },
  { title = "Slovník pojmů", text = "Psychologické, fyziologické a metodologické pojmy vysvětlené srozumitelně, s odkazy na poznámky a zdroje.", path = "glossary/index.md" },
  { title = "Hledat", text = "Najděte poznámky, texty, rady a pojmy v obou jazycích; vyhledávání ignoruje diakritiku a běží ve vašem prohlížeči.", path = "search/index.md" },
  { title = "Případová studie", text = "Jak web vznikl s AI agentem pod dozorem Majordomu, s interaktivní časovou osou skutečných záznamů úkolů, commitů, pipeline a vydání.", path = "case-study/index.md" },
  { title = "Technika", text = "Technické články o architektuře, registru důkazů jako kódu, testování, paralelních agentech, interaktivních modelech a poctivé bilanci času stráveného i ušetřeného.", path = "engineering/_index.md" },
]

[extra.statement.poster]
id = "poster-thesis"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/zvedavost-meni-realitu.png", title = "Zvědavost mění realitu", alt = "Plakát v černé a červené: titulek ZVĚDAVOST MĚNÍ REALITU nad postavou, která kráčí k rudě zářícím dveřím mezi stěnami obrazovek; boční panely uvádějí vstup, proces a výstup a umělecký panel telemetrie končí řádkem root cause: unchanged.", caption = "Ne utéct před životem, ale vidět ho jasněji." },
]

[extra.venting.poster]
id = "poster-venting"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/vice-dat-mene-iluzi.png", title = "Více dat. Méně iluzí.", alt = "Plakát: VÍCE DAT. MÉNĚ ILUZÍ. nad davem se zdviženýma rukama před pódiem s rudě zářící branou; dole požadavek POST /v1/catharsis → 200 OK s problem_solved: false a umělecký panel telemetrie.", caption = "Endpoint odpoví, dav tančí, příčina zůstává nezměněná." },
]

[extra.questions.poster]
id = "poster-questions"
caption = "Ze série plakátů Catharsis as a Service. Slogany a čísla na plakátech patří k dílu; nejsou to výzkumná zjištění."
items = [
  { src = "assets/posters/tezsi-otazky.png", title = "Těžší otázky. Lepší svět.", alt = "Plakát: TĚŽŠÍ OTÁZKY. LEPŠÍ SVĚT. Poutník stoupá po rudě žhnoucí stezce k dveřím na hoře; ukazatele vlevo hlásají comfort, distraction, noise, same patterns a illusions, vpravo curiosity, evidence, context, perspective a better decisions.", caption = "Ne hledat pohodlné odpovědi, ale lepší otázky." },
]

+++
