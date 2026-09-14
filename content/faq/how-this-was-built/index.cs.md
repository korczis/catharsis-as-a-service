+++
title = "Jak web vznikl a jak dlouho to trvalo?"
description = "Od prázdného repozitáře na GitHubu k ověřenému vydání to trvalo 51 minut a 36 sekund; web postavil AI agent pod dohledem. Časová osa pochází ze záznamů a žádný násobek zrychlení se neuvádí."
date = 2026-09-14
weight = 17

[taxonomies]
tags = ["metody", "majordomus", "dodávka softwaru"]

[extra]
kicker = "Otázka 17"
short_answer = "Web vznikl v jednom pracovním sezení: postavil ho AI agent řízený jedním člověkem, s Majordomem jako vrstvou dohledu. Od založení repozitáře po první ověřené vydání uplynulo 51 minut a 36 sekund, od inicializace Majordoma po totéž vydání 19 minut a 19 sekund. Tyto délky pocházejí ze záznamů Gitu, GitHubu, pipeline a Majordoma. Žádný násobek zrychlení se neuvádí, protože chyběla kontrolní podmínka."
related_questions = ["faq/how-evidence-is-graded/index.md", "faq/why-an-artwork/index.md", "faq/does-this-site-measure-me/index.md"]
read_next = ["research/method-majordomus/index.md", "evidence/index.md"]
references = ["repository-2026", "majordomus-2026"]
+++

## Co říkají záznamy

Web je dvojjazyčná statická publikace generovaná nástrojem Zola, nasazovaná na GitHub Pages a při každé změně ověřovaná proti živé adrese. Vznikl v jednom pracovním sezení: vytvořil ho AI agent (Claude Code) řízený jedním člověkem, s Majordomem jako vrstvou dohledu mezi agentem a repozitářem.

Všechny níže uvedené časy jsou v UTC dne 14. září 2026 a pocházejí z historie Gitu, z GitHub API, z ledgeru Majordoma a ze záznamů pipeline. Pracovní sezení začalo v 9:45 přestavbou plakátu. Repozitář na GitHubu byl založen v 9:54:06. Vrstva Majordoma byla inicializována a první dohlížená úloha zahájena v 10:26:23. Web byl commitnut v 10:42:45. Pipeline Pages proběhla se 7 úlohami za 2 minuty 43 sekund, všechny prošly, a vydání v0.1.0 bylo po živém ověření publikováno v 10:45:42.

Odvozené délky jsou: od založení repozitáře po první ověřené vydání **51 min 36 s**; od inicializace Majordoma po první ověřené vydání **19 min 19 s**; od pushe po ověřené vydání **2 min 57 s**. Při tomto vydání web procházel 7 validačními fázemi a 30 prohlížečovými testy.

## Co dodal člověk

Práci řídilo asi patnáct zpráv od jednoho člověka pěti druhů: jednořádková žádost o založení projektu na GitHubu; umělecké zadání plakátu a následná volba ze tří nabídnutých přístupů; tři strukturovaná zadání se stoupajícím rozsahem; krátké pokyny během práce, například nasadit, ověřit v prohlížeči a vydávat automaticky; a redakční směřování včetně nahrazení propagačních textů seriózní ozdrojovanou psychologií.

Žádná z těchto zpráv neurčovala implementační detaily, jako je syntaxe šablon nebo testovací případy. To byla rozhodnutí agenta a úkolem vrstvy dohledu bylo udržet je ověřitelná.

## Co dohled zachytil

Majordomus nepsal kód. Vymezoval a zaznamenával práci a tři vady se staly lokálními nálezy místo neúspěšných běhů pipeline. V 10:29:16 byl po přesunu souborů ohlášen únik ze scope a úloha byla restartována. V 10:39:39 ohlásila kontrola před pushem vadně zapsaný scope a úloha byla restartována dřív, než k jakémukoli pushi došlo. Před prvním commitem ohlásila zdravotní kontrola běžící v pre-commit hooku, že README neodkazuje na bootstrapovací soubor pro agenty; vada byla opravena dřív, než se dostala do repozitáře.

Jeden mechanismus váží víc než ostatní: úlohu nelze uzavřít jako dokončenou, dokud neprojde její ověřovací příkaz. Tady jím byl živý smoke test, takže „dokončeno" znamenalo „nasazeno a ověřeno", ne „napsáno". Úloha byla uzavřena v 10:47:25 s tímto testem, který prošel za 7 sekund.

## Proč se neuvádí žádný násobek zrychlení

Proběhlo jedno sezení a žádné srovnatelné sezení bez dohledu, takže chybí kontrolní podmínka a žádný faktor zrychlení uvést nelze. To je poctivý limit a je zapsán v rejstříku dokladů vedle samotné časové osy.

Co záznamy ukazují, je místo, kde se čas neztratil. Žádný push CI neodmítla, žádné nasazení se nemuselo vracet zpět a první běh pipeline prošel ve všech sedmi úlohách. Platí tři další omezení: časová osa začíná u prvního zaznamenaného souboru, takže plánování před ním není zahrnuto; délky závisejí na nástrojích, hardwaru a latenci sítě tohoto sezení; a sezení se opíralo i o běžné pojistky nesouvisející s Majordomem, jejichž účinek zde není oddělen.
