from onyx.agents.agent_search.dr.constants import MAX_DR_PARALLEL_SEARCH
from onyx.agents.agent_search.dr.enums import DRPath, ResearchType
from onyx.prompts.prompt_template import PromptTemplate

# Standartai
SEPARATOR_LINE = "-------"
SEPARATOR_LINE_LONG = "---------------"
SUFFICIENT_INFORMATION_STRING = "Turiu pakankamai informacijos"
INSUFFICIENT_INFORMATION_STRING = "Neturiu pakankamai informacijos"


KNOWLEDGE_GRAPH = DRPath.KNOWLEDGE_GRAPH.value
INTERNAL_SEARCH = DRPath.INTERNAL_SEARCH.value
CLOSER = DRPath.CLOSER.value
WEB_SEARCH = DRPath.WEB_SEARCH.value


DONE_STANDARD: dict[str, str] = {}
DONE_STANDARD[ResearchType.THOUGHTFUL] = (
    "Stenkis įsitikinti, kad, tavo manymu, turi pakankamai informacijos, kad \
atsakytum į klausimą taip, kaip jis suformuluotas, ir tokiu detalumo lygiu, kuris aiškiai nurodytas klausime. \
Tačiau atsakymas turėtų būti pilnas. Jei trūksta informacijos, tu turėtum papildomai klausti follow-up klausimų, jei reikia."
)

DONE_STANDARD[ResearchType.DEEP] = (
    "Stenkis įsitikinti, kad, tavo manymu, turi pakankamai informacijos, kad \
atsakytum į klausimą taip, kaip jis suformuluotas, ir tokiu detalumo lygiu, kuris aiškiai nurodytas klausime. \
Būk ypač dėmesingas detalėms, kurios, tavo nuomone, būtų įdomios naudotojui. Apsvarstyk \
užduoti papildomus klausimus, jei reikia."
)


# TODO: žr. TODO OrchestratorTool, perkelti įrankio aprašą į įrankio implementacijos klasę v2 versijai
TOOL_DESCRIPTION: dict[DRPath, str] = {}
TOOL_DESCRIPTION[DRPath.INTERNAL_SEARCH] = f"""\
Šis įrankis naudojamas klausimams, į kuriuos galima atsakyti naudojant informaciją, \
esančią prijungtuose dokumentuose, kurie daugiausia bus privatūs organizacijai/naudotojui.
Atkreipkite dėmesį, kad paieškos įrankis nėra tinkamas laiko tvarka suformuluotiems klausimams \
(pvz., '...naujausias el. laiškas...', '...paskutinės 2 išspręstos Jira užduotys...') ir \
agregavimo tipo klausimams (pvz., 'kiek...') \
(nebent tokia informacija yra prijungtuose dokumentuose). Jei yra tokiems klausimams labiau \
tinkamų įrankių, naudokite juos.
Paprastai nereikėtų klausti patikslinimų apie temas, kurių ieško {INTERNAL_SEARCH} įrankis, \
nes gauti dokumentai tikėtina suteiks daugiau konteksto.
Kiekviena užklausa {INTERNAL_SEARCH} įrankiui turėtų būti parašyta kaip PAIEŠKOS UŽKLAUSA, o NE kaip klausimas \
ar instrukcija! Taip pat, \
{INTERNAL_SEARCH} įrankis PALAIKO lygiagrečius iškvietimus iki {MAX_DR_PARALLEL_SEARCH} užklausų.
"""

TOOL_DESCRIPTION[DRPath.WEB_SEARCH] = f"""\
Šis įrankis naudojamas klausimams, į kuriuos galima atsakyti naudojant \
viešai internete prieinamą informaciją. {WEB_SEARCH} įrankis PALAIKO lygiagrečius iškvietimus \
iki {MAX_DR_PARALLEL_SEARCH} užklausų.
NAUDOJIMO PASTABOS:
  - Kadangi {WEB_SEARCH} įrankis nėra tinkamas laiko tvarka suformuluotiems klausimams \
(pvz., '...naujausias publikavimas...'), jei tikslas iš tiesų yra tokio tipo klausimai, \
turėtum siųsti užklausas \
{WEB_SEARCH} įrankiui, pavyzdžiui, '... NAUJIAUSIOS publikacijos...', ir tikėtis, kad vėlesni \
kalbos modelio iškvietimai sugebės iš rezultatų rasti 'naujausią publikaciją'.
"""

TOOL_DESCRIPTION[DRPath.KNOWLEDGE_GRAPH] = f"""\
Šis įrankis panašus į paieškos įrankį, tačiau atsako į klausimus remdamasis \
iš pirminių dokumentų išgautomis esybėmis ir ryšiais. \
Jis tinka atsakyti į sudėtingus klausimus apie konkrečias esybes ir jų ryšius, pavyzdžiui, \
"apibendrink atvirus bilietus, priskirtus Jonui per pastarąjį mėnesį". \
Jis taip pat gali užklausti reliacinę duomenų bazę, kurioje yra esybės ir ryšiai, todėl gali \
atsakyti į agregavimo tipo klausimus, pvz., 'kiek Jira užduočių kiekvienas darbuotojas uždarė praėjusį mėnesį?'. \
Tačiau {KNOWLEDGE_GRAPH} įrankis TURI BŪTI NAUDOJAMAS tik tada, jei į klausimą galima atsakyti naudojant \
žinių grafike prieinamas esybių/ryšių tipus. (Taigi net jei naudotojas \
paprašo naudoti Žinių Grafiką, bet klausimas/prašymas tiesiogiai nesusijęs \
su žinių grafiko esybėmis/ryšiais, nenaudok {KNOWLEDGE_GRAPH} įrankio.).
Atkreipk dėmesį, kad {KNOWLEDGE_GRAPH} įrankis gali ir RASTI, ir ANALIZUOTI/AGREGUOTI/UŽKLAUSTI \
atitinkamus dokumentus/esybes. \
Pvz., jei klausimas yra "kiek yra atvirų Jira užduočių", turėtum tai pateikti kaip vieną užklausą \
{KNOWLEDGE_GRAPH} įrankiui, o ne skaidyti į radimą ir skaičiavimą.
Taip pat {KNOWLEDGE_GRAPH} įrankis veikia lėčiau nei standartiniai paieškos įrankiai.
Svarbu: {KNOWLEDGE_GRAPH} įrankis taip pat gali analizuoti atitinkamus dokumentus/esybes, todėl NENAUDOK \
strategijos „pirmiausia rasti dokumentus, o tada analizuoti vėliau“. Užklausk {KNOWLEDGE_GRAPH} \
įrankį tiesiogiai, pvz., 'apibendrink naujausią Jono sukurtą Jira užduotį'.
Galiausiai, norint naudoti {KNOWLEDGE_GRAPH} įrankį, svarbu žinoti konkretų esybės/ryšio tipą, \
į kurį referuoja klausimas. Jei to pagrįstai negalima nustatyti, pagalvok apie patikslinimo klausimą.
Kita vertus, {KNOWLEDGE_GRAPH} įrankiui NEREIKIA nurodyti atributų. T. y., galima \
ieškoti esybių nenustatant konkrečių atributų. Todėl, jei klausime prašoma esybės ar \
esybės tipo apskritai, neturėtum klausti patikslinimų dėl atributų specifikavimo. \

CRITICAL NOTE: questions to the {KNOWLEDGE_GRAPH} tool MUST only relate to entities and relationships in the knowledge graph, \
as specified for the knowledge graph! The questions are certainly derived from the user query to generate \
some sub-answers, but the question sent to the graph must be a question that can be answered using the \
entity and relationship types and their attributes that will be communicated to you.
"""

TOOL_DESCRIPTION[DRPath.CLOSER] = f"""\
Šis įrankis neturi tiesioginės prieigos prie dokumentų, tačiau naudoja
ankstesnių įrankių iškvietimų rezultatus tam, kad sugeneruotų išsamų galutinį atsakymą. Jis turėtų būti kviečiamas tiksliai vieną kartą
pačioje pabaigoje, kad būtų sujungta surinkta informacija, prireikus atlikti palyginimus ir atrinkti
aktualiausią informaciją klausimui atsakyti. Taip pat gali iškart pereiti prie {CLOSER}, jei
pateiktoje istorijoje yra pakankamai informacijos atsakymui.
"""


TOOL_DIFFERENTIATION_HINTS: dict[tuple[str, str], str] = {}
TOOL_DIFFERENTIATION_HINTS[
    (
        DRPath.INTERNAL_SEARCH.value,
        DRPath.WEB_SEARCH.value,
    )
] = f"""\
- apskritai, pirmiausia turėtum naudoti {INTERNAL_SEARCH} įrankį, o {WEB_SEARCH} naudoti tik tuo atveju, jei \
{INTERNAL_SEARCH} įrankio rezultatuose neradai reikiamos informacijos arba naudotojas aiškiai prašo ar \
numano {WEB_SEARCH} įrankio naudojimą. Be to, jei {WEB_SEARCH} įrankis nesuteikė \
reikalingos informacijos, gali kitame žingsnyje pereiti prie {INTERNAL_SEARCH}.
"""

TOOL_DIFFERENTIATION_HINTS[
    (
        DRPath.KNOWLEDGE_GRAPH.value,
        DRPath.INTERNAL_SEARCH.value,
    )
] = f"""\
- peržiūrėk naudotojo užklausą ir žinių grafiko esybių bei ryšių tipus, \
ar klausimas apskritai gali būti atsakytas naudojant {KNOWLEDGE_GRAPH} įrankį. Jei ne, '{INTERNAL_SEARCH}' \
gali būti geriausia alternatyva.
- jei į klausimą galima atsakyti naudojant {KNOWLEDGE_GRAPH}, bet klausimas panašus į standartinę \
'ieškok to' tipo užklausą, tuomet naudok '{INTERNAL_SEARCH}'.
- taip pat apsvarstyk, ar naudotojo užklausa implikuoja standartinę {INTERNAL_SEARCH} užklausą ar \
{KNOWLEDGE_GRAPH} užklausą. Pavyzdžiui, 'naudok paprastą paiešką, kad rastum <xyz>' reiškia standartinę {INTERNAL_SEARCH} užklausą, \
o 'naudok žinių grafiką (arba KG), kad apibendrintum...' turėtų reikšti {KNOWLEDGE_GRAPH} užklausą.
"""

TOOL_DIFFERENTIATION_HINTS[
    (
        DRPath.KNOWLEDGE_GRAPH.value,
        DRPath.WEB_SEARCH.value,
    )
] = f"""\
- peržiūrėk naudotojo užklausą ir žinių grafiko esybių bei ryšių tipus, \
ar klausimas apskritai gali būti atsakytas naudojant {KNOWLEDGE_GRAPH} įrankį. Jei ne, '{WEB_SEARCH}' \
GALI būti alternatyva, bet tik jei klausimas susijęs su viešais duomenimis. Pirmiausia gali \
apsvarstyti ir kitus įrankius, galinčius užklausti interneto duomenis, jei tokių yra.
- jei į klausimą galima atsakyti naudojant {KNOWLEDGE_GRAPH}, bet klausimas panašus į standartinę \
- taip pat apsvarstyk, ar naudotojo užklausa implikuoja standartinę {WEB_SEARCH} užklausą ar \
{KNOWLEDGE_GRAPH} užklausą (darome prielaidą, kad duomenys gali būti tiek vieši, tiek vidiniai). \
Pavyzdžiui, 'naudok paprastą interneto paiešką, kad rastum <xyz>' reiškia standartinę {WEB_SEARCH} užklausą, \
o 'naudok žinių grafiką (arba KG), kad apibendrintum...' turėtų reikšti {KNOWLEDGE_GRAPH} užklausą.
"""


TOOL_QUESTION_HINTS: dict[str, str] = {
    DRPath.INTERNAL_SEARCH.value: f"""jei įrankis yra {INTERNAL_SEARCH}, klausimas turi būti \
parašytas kaip iki {MAX_DR_PARALLEL_SEARCH} užklausų sąrašas, tinkamas paieškai. \
Jei reikia ieškoti kelių aspektų, klausimą reikėtų suskaidyti į kelias dalines užduotis.
""",
    DRPath.WEB_SEARCH.value: f"""jei įrankis yra {WEB_SEARCH}, klausimas turi būti \
parašytas kaip iki {MAX_DR_PARALLEL_SEARCH} užklausų sąrašas, tinkamas paieškai. Užklausos turėtų būti trumpos \
ir fokusuotos į vieną konkretų aspektą. Jei reikia ieškoti kelių aspektų, klausimą reikėtų suskaidyti \
į kelias dalines užduotis.
""",
    DRPath.KNOWLEDGE_GRAPH.value: f"""jei įrankis yra {KNOWLEDGE_GRAPH}, klausimą reikia \
parašyti kaip vieno klausimo sąrašą.
""",
    DRPath.CLOSER.value: f"""jei įrankis yra {CLOSER}, klausimų sąrašas turėtų būti tiesiog \
['Atsakyk į pirminį klausimą naudodamas turimą informaciją.'].
""",
}


KG_TYPES_DESCRIPTIONS = PromptTemplate(
    f"""\
Čia pateikiami žinių grafike galimi esybių tipai:
{SEPARATOR_LINE}
---possible_entities---
{SEPARATOR_LINE}

Čia pateikiami žinių grafike galimi ryšių tipai:
{SEPARATOR_LINE}
---possible_relationships---
{SEPARATOR_LINE}
"""
)


ORCHESTRATOR_DEEP_INITIAL_PLAN_PROMPT_STREAM = PromptTemplate(
    f"""
Tu puikiai gebi analizuoti klausimą ir išskaidyti jį į \
aukšto lygio, atsakomus sub-klausimus.

Atsižvelgdamas į naudotojo užklausą ir turimų įrankių sąrašą, tavo užduotis – parengti aukšto lygio planą, \
susidedantį iš iteracijų sąrašo, kur kiekviena iteracija apibrėžia \
ištirtinus aspektus, kad proceso pabaigoje turėtum pakankamai \
informacijos sukurti gerai ištirtą ir ypač aktualų atsakymą į naudotojo užklausą.

Atkreipk dėmesį, kad planas bus naudojamas tik kaip gairės, o atskiras agentas naudos tavo planą kartu \
su ankstesnių iteracijų rezultatais, kad kiekvienai iteracijai sugeneruotų konkrečius klausimus pasirinktoms \
priemonėms. Todėl plane nereikėtų būti per daug konkrečiam, nes kai kurie žingsniai gali priklausyti nuo \
ankstesnių žingsnių.

Daryk prielaidą, kad visi žingsniai bus vykdomi nuosekliai, todėl ankstesnių žingsnių atsakymai bus žinomi \
vėlesniuose žingsniuose. Tam užfiksuoti, vėlesniuose žingsniuose gali remtis ankstesniais rezultatais. (Pavyzdys \
'vėlesnio' klausimo: 'rask informaciją kiekvienam 3 žingsnio rezultatui'.)

Tavo dispozicijoje yra ---num_available_tools--- įrankių, \
---available_tools---.

---tool_descriptions---

---kg_types_descriptions---

Čia pateikiamas įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Svarbiausia, čia yra klausimas, kuriam turi parengti planą:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Galiausiai, pateikiamos kelios paskutinės pokalbio žinutės nuorodai (jei yra).
Atkreipk dėmesį, kad pokalbio istorijoje gali jau būti atsakymas į naudotojo klausimą, tokiu atveju gali
iškart pereiti prie {CLOSER}, arba naudotojo klausimas gali būti ankstesnio klausimo tąsa.
Bet kuriuo atveju, nesupainiok toliau pateiktos informacijos su naudotojo užklausa. Ji skirta tik kontekstui.
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Taip pat dabartinis laikas yra ---current_time---. Apsvarstyk tai, jei klausimas susijęs su datomis ar
laikotarpiais.

GAIRĖS:
   - planas turi užtikrinti, kad a) problema būtų pilnai suprasta, b) būtų užduoti tinkami klausimai,
     c) būtų surinkta tinkama informacija, kad galutinis atsakymas būtų gerai ištirtas ir itin aktualus,
     rodantis gilų problemos supratimą. Pavyzdžiui, jei klausimas
susijęs su sprendimo pozicionavimu rinkoje, plane turėtų būti numatyta pilnai suprasti rinką, \
įskaitant klientų tipus ir naudotojų personas, konkurentus ir jų pozicionavimą ir pan.
   - dar kartą: kadangi vėlesni žingsniai gali priklausyti nuo ankstesnių, žingsniai turėtų būti gana aukšto lygio.
     Pavyzdžiui, jei klausimas: 'kurios Jira užduotys sprendžia pagrindines Nike problemas?', geras planas galėtų būti:
   --
   1) identifikuoti pagrindinę Nike problemą
   2) rasti Jira užduotis, kurios sprendžia 1 žingsnyje identifikuotą problemą
   3) sugeneruoti galutinį atsakymą
   --
   - paskutinis žingsnis turėtų būti 'sugeneruoti galutinį atsakymą' arba kažkas panašaus.

Prašome pirmiausia trumpai pamąstyti (1–2 sakiniai) ir tuomet pateikti planą. Įvyniojęs savo samprotavimą į \
<reasoning> ir </reasoning> žymes, o planą pateikdamas tarp <plan> ir </plan> žymių, pvz.:
<reasoning> [tavo samprotavimas 1–2 sakiniais] </reasoning>
<plan>
1. [1 žingsnis]
2. [2 žingsnis]
...
n. [n-tasis žingsnis]
</plan>

ATSAKYMAS:
"""
)


ORCHESTRATOR_DEEP_INITIAL_PLAN_PROMPT = PromptTemplate(
    f"""
Tu puikiai gebi analizuoti klausimą ir išskaidyti jį į \
aukšto lygio, atsakomus sub-klausimus.

Atsižvelgdamas į naudotojo užklausą ir turimų įrankių sąrašą, tavo užduotis – parengti aukšto lygio planą, \
susidedantį iš iteracijų sąrašo, kur kiekviena iteracija apibrėžia \
ištirtinus aspektus, kad proceso pabaigoje turėtum pakankamai \
informacijos sukurti gerai ištirtą ir ypač aktualų atsakymą į naudotojo užklausą.

Atkreipk dėmesį, kad planas bus naudojamas tik kaip gairės, o atskiras agentas naudos tavo planą kartu \
su ankstesnių iteracijų rezultatais, kad kiekvienai iteracijai sugeneruotų konkrečius klausimus pasirinktoms \
priemonėms. Todėl plane nereikėtų būti per daug konkrečiam, nes kai kurie žingsniai gali priklausyti nuo \
ankstesnių žingsnių.

Daryk prielaidą, kad visi žingsniai bus vykdomi nuosekliai, todėl ankstesnių žingsnių atsakymai bus žinomi \
vėlesniuose žingsniuose. Tam užfiksuoti, vėlesniuose žingsniuose gali remtis ankstesniais rezultatais. (Pavyzdys \
'vėlesnio' klausimo: 'rask informaciją kiekvienam 3 žingsnio rezultatui'.)

Tavo dispozicijoje yra ---num_available_tools--- įrankių, \
---available_tools---.

---tool_descriptions---

---kg_types_descriptions---

Čia pateikiamas įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Svarbiausia, čia yra klausimas, kuriam turi parengti planą:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Galiausiai, pateikiamos kelios paskutinės pokalbio žinutės nuorodai (jei yra). \
Atkreipk dėmesį, kad pokalbio istorijoje gali jau būti atsakymas į naudotojo klausimą, tokiu atveju gali \
iškart pereiti prie {CLOSER}, arba naudotojo klausimas gali būti ankstesnio klausimo tąsa. \
Bet kuriuo atveju, nesupainiok toliau pateiktos informacijos su naudotojo užklausa. Ji skirta tik kontekstui.
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Taip pat dabartinis laikas yra ---current_time---. Apsvarstyk tai, jei klausimas susijęs su datomis ar \
laikotarpiais.

GAIRĖS:
   - planas turi užtikrinti, kad a) problema būtų pilnai suprasta,  b) būtų užduoti tinkami klausimai, c) būtų surinkta tinkama informacija, kad \
galutinis atsakymas būtų gerai ištirtas ir itin aktualus, \
ir rodytų gilų problemos supratimą. Pavyzdžiui, jei klausimas susijęs su \
sprendimo pozicionavimu rinkoje, plane turėtų būti numatyta pilnai suprasti rinką, \
įskaitant klientų tipus ir naudotojų personas, konkurentus ir jų pozicionavimą ir pan.
   - dar kartą: kadangi vėlesni žingsniai gali priklausyti nuo ankstesnių, žingsniai turėtų būti gana aukšto lygio. \
Pavyzdžiui, jei klausimas: 'kurios Jira užduotys sprendžia pagrindines Nike problemas?', geras planas galėtų būti:
   --
   1) identifikuoti pagrindinę Nike problemą
   2) rasti Jira užduotis, kurios sprendžia 1 žingsnyje identifikuotą problemą
   3) sugeneruoti galutinį atsakymą
   --
   - paskutinis žingsnis turėtų būti 'sugeneruoti galutinį atsakymą' arba kažkas panašaus.

Prašome suformatuoti atsakymą kaip JSON žodyną pagal šį šabloną:
{{
        "reasoning": "<tavo samprotavimas 2–4 sakiniais. Pagalvok kaip žmogus. \
Taip pat apsvarstyk dabartinį laiką, jei tai naudinga problemai.>",
   "plan": "<pilnas planas, GRAŽIAI suformatuotas kaip eilutė. Žr. pavyzdžius aukščiau, tačiau \
įsitikink, kad naudojamas markdown formatavimas sąrašams ir kitam formatavimui. \
(Atkreipk dėmesį, kad planas turi būti eilutė, o ne eilučių sąrašas! Jei klausimas \
susijęs su datomis ir pan., taip pat apsvarstyk dabartinį laiką. Taip pat, dar kartą, žingsniuose \
NETURI būti konkretaus įrankio pavadinimų, net jei jis buvo naudotas formuojant \
klausimą. Tiesiog pateik žingsnius.)>"
}}
"""
)


ORCHESTRATOR_FAST_ITERATIVE_REASONING_PROMPT = PromptTemplate(
    f"""
Iš esmės, turi atsakyti į naudotojo klausimą/užklausą. Tam gali reikėti atlikti įvairias paieškas ar \
iškviesti kitus įrankius/pagalbinius agentus.

Jau turi keletą dokumentų ir informacijos iš ankstesnių paieškų/įrankių iškvietimų, kuriuos \
generavai ankstesnėse iteracijose.

TAVO UŽDUOTIS – nuspręsti, ar anksčiau gautų dokumentų ir informacijos \
pakanka, kad PILNAI atsakytum į naudotojo klausimą.

Pastaba: dabartinis laikas yra ---current_time---.

Čia yra įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Svarbiausia, čia yra klausimas, kuriam turi parengti atsakymą:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Čia yra kelios paskutinės pokalbio žinutės nuorodai (jei yra).
Atkreipk dėmesį, kad pokalbio istorijoje jau gali būti atsakymas į naudotojo klausimą, tokiu atveju gali \
iškart pereiti prie {CLOSER}, arba naudotojo klausimas gali būti ankstesnio klausimo tąsa. \
Bet kuriuo atveju, nesupainiok toliau pateiktos informacijos su naudotojo užklausa. Ji skirta tik kontekstui.
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Čia pateikiami ankstesni sub-klausimai/sub-užduotys ir atitinkamai gauti dokumentai/informacija (jei yra). \
{SEPARATOR_LINE}
---answer_history_string---
{SEPARATOR_LINE}

GAIRĖS:
   - peržiūrėk pirminį klausimą ir ankstesnius sub-klausimus/sub-užduotis su \
gautais dokumentais/informacija, kad nustatytum, ar informacijos pakanka \
pilnai atsakyti į pirminį klausimą.
   - maždaug taip turėtum apsispręsti, ar darbas baigtas, ar reikia daugiau tyrimo:
{DONE_STANDARD[ResearchType.THOUGHTFUL]}

Prašome trumpai (1–2 sakiniais) pagrįsti, ar pakanka informacijos atsakyti į pirminį klausimą, \
tuomet užbaik tiesiogine fraze „Todėl, {SUFFICIENT_INFORMATION_STRING} atsakyti į pirminį klausimą.“ arba \
„Todėl, {INSUFFICIENT_INFORMATION_STRING} atsakyti į pirminį klausimą.“ \
PRIVALAI baigti viena iš šių dviejų frazių PAŽODIŠKAI.

ATSAKYMAS:
"""
)


ORCHESTRATOR_FAST_ITERATIVE_DECISION_PROMPT = PromptTemplate(
    f"""
Iš esmės, turi atsakyti į naudotojo užklausą. Tam gali tekti atlikti įvairias paieškas.

Jau gali turėti atsakymų į ankstesnes paieškas, kurias generavai ankstesnėse iteracijose.

Nuspręsta, kad norint atsakyti į pirminį klausimą, reikia papildomos informacijos.

TAVO UŽDUOTIS – nuspręsti, kurį įrankį kviesti toliau, ir kokį konkretų klausimą/užduotį jam pateikti, \
atsižvelgiant į jau gautus atsakymus ir vadovaujantis pradiniu planu.

Pastabos:
 - dabar planuoji ---iteration_nr--- iteraciją.
 - dabartinis laikas yra ---current_time---.

Tavo dispozicijoje yra ---num_available_tools--- įrankių, \
---available_tools---.

---tool_descriptions---

Dabar įrankiai gali skambėti panašiai. Čia yra įrankių atskyrimo gairės:

---tool_differentiation_hints---

Jei prieinamas Žinių Grafikas, čia yra žinių grafike prieinami esybių ir ryšių tipai \
užklausoms:

---kg_types_descriptions---

Štai pirminis klausimas, į kurį turi atsakyti:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Čia yra kelios paskutinės pokalbio žinutės nuorodai (jei yra), kurios gali būti svarbios \
kontekstui.
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Čia yra ankstesni sub-klausimai/sub-užduotys ir atitinkamai gauti dokumentai/informacija (jei yra). \
{SEPARATOR_LINE}
---answer_history_string---
{SEPARATOR_LINE}

Čia yra įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Ir galiausiai, čia pateikiamas ankstesnės iteracijos samprotavimas, kodėl reikia \
papildomų tyrimų (t. y., įrankių iškvietimų):
{SEPARATOR_LINE}
---reasoning_result---
{SEPARATOR_LINE}

GAIRĖS:
   - atsižvelk į priežastis, kodėl reikia daugiau tyrimų, pirminį klausimą, turimus įrankius \
(ir jų atskyrimą), ankstesnius sub-klausimus/sub-užduotis ir gautą informaciją \
bei paskutines pokalbio žinutes (jei aktualu), kad nuspręstum, kurį įrankį kviesti toliau \
ir kokius klausimus/užduotis jam pateikti.
   - gali svarstyti tik tokį įrankį, kurio kaina telpa į likusį laiko biudžetą! Įrankio kaina turi būti mažesnė už \
likusį biudžetą.
   - būk atsargus ir NEKARTOK beveik to paties SUB-KLAUSIMO tam pačiam įrankiui! \
Jei iš vieno įrankio negavai gero atsakymo, gali užduoti tą patį tikslą kitam įrankiui,
tik jei jis taip pat tinkamas.
   - Vėlgi, dėmesys – NAUJOS INFORMACIJOS gavimui! Stenkis formuoti klausimus, kurie
         - užpildo informacijos spragas pirminio klausimo atžvilgiu
         - arba yra įdomios ankstesnių atsakymų tęsiniai, jei, tavo manymu, \
naudotojui tai būtų įdomu.

TAVO UŽDUOTIS: turi sukonstruoti kitą klausimą ir pasirinkti įrankį, kuriam jį siųsti. Tam apsvarstyk \
pirminį klausimą, tavo turimus įrankius, iki šiol gautus atsakymus \
(iš ankstesnių iteracijų arba iš pokalbio istorijos) ir pateiktą priežastį, kodėl reikia daugiau \
tyrimų. Įsitikink, kad klausimas yra konkretus ir – jei taikoma – \
REMiasi iki šiol gautomis įžvalgomis, kad gautum naują, tikslingą informaciją, reikalingą \
atsakyti į pirminį klausimą.

Prašome suformatuoti atsakymą kaip JSON žodyną pagal šį šabloną:
{{
        "reasoning": "<palik tuščią, nes tai jau pateikta>",
   "next_step": {{
        "tool": "<---tool_choice_options--->",
                  "questions": "<klausimas, kurį nori pateikti įrankiui. Atkreipk dėmesį, kad \
klausimas turi tikti įrankiui. Pavyzdžiui:
---tool_question_hints---]>
Taip pat, jei galutinis klausimas prašo palyginti kelias galimybes ar esybes, PRIVALAI \
KLAUSTI apie KIEKVIENĄ galimybę ar esybę ATSKIRAI, nes vėlesniuose žingsniuose galėsi tiek \
užduoti daugiau klausimų, tiek palyginti ir įvertinti surinktą informaciją! \
(Pavyzdžiui, „kodėl Puma padarė X kitaip nei Adidas...“ turėtų virsti klausimais \
„kaip Puma padarė X..“ ir „kaip Adidas padarė X..“, o ne „kaip Puma ir Adidas padarė X..“)"}}
}}
"""
)


ORCHESTRATOR_NEXT_STEP_PURPOSE_PROMPT = PromptTemplate(
    f"""
Iš esmės, turi atsakyti į naudotojo užklausą. Tam gali tekti atlikti įvairias paieškas.

Gali jau turėti atsakymų į ankstesnes paieškas, kurias generavai ankstesnėse iteracijose.

Nuspręsta, kad norint atsakyti į pirminį klausimą, reikia daugiau tyrimo, ir \
atitinkami įrankiai bei jų iškvietimai buvo parinkti.

TAVO UŽDUOTIS – per 2–3 sakinius aiškiai išdėstyti šių įrankių iškvietimų tikslą.

Štai pirminis klausimas, į kurį turi atsakyti:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Čia yra samprotavimas, kodėl prireikė daugiau tyrimo (t. y., įrankių iškvietimų):
{SEPARATOR_LINE}
---reasoning_result---
{SEPARATOR_LINE}

Ir čia yra parinkti įrankiai bei jų iškvietimai:
{SEPARATOR_LINE}
---tool_calls---
{SEPARATOR_LINE}

Prašome glaustai (1–2 sakiniais) įvardinti šių įrankių iškvietimų tikslą. \
Pavyzdžiui, „Dabar bandau rasti daugiau informacijos apie Nike ir Puma naudodamas \
Interneto Paiešką“ (darome prielaidą, kad parinktas įrankis yra Interneto Paieška; čia būtina \
įvardyti konkretų įrankį.)

Atkreipk dėmesį į VIENĄ IŠIMTĮ: jei kviečiamas {CLOSER} įrankis (ar įrankiai), tuomet reikėtų \
pasakyti kažką panašaus į „Dabar bandau sugeneruoti galutinį atsakymą, nes turiu pakankamai informacijos“, \
bet neminėk {CLOSER} įrankio tiesiogiai.

ATSAKYMAS:
"""
)


TOOL_OUTPUT_FORMAT = """\
Prašome suformatuoti atsakymą kaip JSON žodyną pagal šį šabloną:
{
   "reasoning": "<tavo samprotavimas 5–8 sakiniais, kas nulėmė tavo išvadas dėl \
konkretaus paieškos klausimo, remiantis dokumentais. Pradėk trumpu teiginiu, ar \
SPECIFINIS KONTEKSTAS paminėtas dokumentuose. (Pavyzdys: 'Nepavyko rasti informacijos \
apie geltoną karį konkrečiai, bet radau informaciją apie karį...'). Čia sugeneruok \
informaciją, kuri bus reikalinga glaustam atsakymui į konkretų paieškos klausimą.>",
   "answer": "<konkretus atsakymas į konkretų paieškos klausimą. Gali reikėti pagrįsti \
remiantis dokumentais. Vėlgi, pradėk trumpu teiginiu, ar SPECIFINIS KONTEKSTAS \
paminėtas dokumentuose. (Pavyzdys: 'Nepavyko rasti informacijos apie geltoną karį konkrečiai, \
bet radau informaciją apie karį...'). Atsakymas turi būti tikslus ir glaustas, \
ir konkrečiai atsakyti į klausimą. Cituok dokumentų šaltinius inline formatu [[1]][[7]] ir pan. kur yra \
   būtina nurodyti dokumentų numerius skliaustuose, o ne pavadinimus.>",
   "claims": "<trumpų teiginių sąrašas, aptartų dokumentuose ir susijusių su užklausa ir/arba \
pirminiu klausimu. Jie vėliau bus naudojami papildomiems klausimams ir verifikacijoms. Atmink, kad \
jų gali nebūti glaustame atsakyme aukščiau. Taip pat kiekvienas teiginys \
turi turėti VIENĄ faktą su pakankamu kontekstu, kad kita sistema galėtų jį patikrinti \
be papildomo grįžimo prie šių dokumentų. Taip pat čia cituok šaltinius inline formatu [[1]][[7]] ir pan. \
Formatas: [<teiginys 1>, <teiginys 2>, <teiginys 3>, ...], kiekvienas su citatomis.>"
}
"""

INTERNAL_SEARCH_PROMPTS: dict[ResearchType, PromptTemplate] = {}
INTERNAL_SEARCH_PROMPTS[ResearchType.THOUGHTFUL] = PromptTemplate(
    f"""
Tu puikiai moki naudoti pateiktus dokumentus, konkretų paieškos klausimą ir \
pirminį naudotojo klausimą, kad pateiktum glaustą, aktualų ir pagrįstą \
atsakymą į konkretų paieškos klausimą. Nors tavo atsakymas turėtų daugiausia sietis su konkrečiu \
paieškos klausimu, nepamiršk ir pirminio klausimo, kad suteiktum vertingų įžvalgų jam atsakyti.

Štai konkretus paieškos klausimas:
{SEPARATOR_LINE}
---search_query---
{SEPARATOR_LINE}

Štai pirminis klausimas, į kurį galiausiai reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

O čia yra dokumentų sąrašas, kuriuos PRIVALAI naudoti atsakydamas į konkretų paieškos klausimą:
{SEPARATOR_LINE}
---document_text---
{SEPARATOR_LINE}

Pastabos:
   - naudok tik tuos dokumentus, kurie yra aktualūs konkrečiam paieškos klausimui IR apie kuriuos ŽINAI, kad jie \
taikomi klausimo kontekstui! Pavyzdys: kontekstas apie tai, ką Nike darė, kad skatintų pardavimus, \
o klausimas apie tai, ką Puma daro pardavimams skatinti – NENAUDOK JOKIOS \
informacijos apie Nike! Net jei kontekstas nekalba apie Nike pardavimus, o tik apie \
„pardavimų skatinimą“ apskritai (be įmonių), vis tiek negalima naudoti tokios informacijos! \
Privalai būti tikras dėl konteksto teisingumo. Jei abejoji – nenaudok to dokumento!
   - itin svarbu vengti fantazavimo ir informacijos ištraukimo iš konteksto.
   - aiškiai nurodyk bet kokias prielaidas, kurias darai savo atsakyme.
   - nors pirminis klausimas svarbus, daugiausia dėmesio skirk konkrečiam paieškos klausimui. \
Tai yra tavo užduotis.
   - dar kartą – nenaudok/cituok jokių dokumentų, dėl kurių nesate 100% tikras, kad jie aktualūs \
KONKREČIAM klausimo kontekstui! IR NESPĖLIIOK, sakydamas „panašu, kad šis kontekstas tinka“. \
TAIP DARYTI NEGALIMA. Jei klausimas apie „geltoną karį“, o dokumentuose yra tik „kario“ paminėjimas, \
aiškiai pasakyk „nėra paminėta geltonas karis konkrečiai“ ir IGNORUOK tą dokumentą. Jei \
vis dėlto stipriai įtari, kad dokumentas aktualus, gali jį panaudoti, bet PRIVALAI aiškiai \
nurodyti, kad nesi 100% tikras ir kad dokumente neminimas „geltonas karis“ (kaip pavyzdys).
Jei konkreti sąvoka ar terminas nėra pateiktas, atsakymas turi tai aiškiai įvardyti prieš \
teikiant bet kokią susijusią informaciją.
   - Visada pradėk atsakymą tiesiogine fraze apie tai, ar dokumentuose buvo rasta \
tiksli frazė ar reikšmė.
   - pateik tik TRUMPĄ atsakymą, kuris i) pateikia prašytą informaciją, jei klausimas yra \
labai konkretus, ii) cituoja atitinkamus dokumentus atsakymo pabaigoje, iii) pateikia TRUMPĄ \
aukšto lygio santrauką iš cituotų dokumentų, nurodydamas dokumentus, kurie yra labiausiai \
aktualūs konkrečiam klausimui.

{TOOL_OUTPUT_FORMAT}
"""
)

INTERNAL_SEARCH_PROMPTS[ResearchType.DEEP] = PromptTemplate(
    f"""
Tu puikiai moki naudoti pateiktus dokumentus, konkretų paieškos klausimą ir \
pirminį naudotojo klausimą, kad pateiktum glaustą, aktualią ir pagrįstą \
analizę į konkretų paieškos klausimą. Nors tavo atsakymas turėtų daugiausia sietis su konkrečiu \
paieškos klausimu, nepamiršk ir pirminio klausimo, kad suteiktum vertingų įžvalgų jam atsakyti.

Štai konkretus paieškos klausimas:
{SEPARATOR_LINE}
---search_query---
{SEPARATOR_LINE}

Štai pirminis klausimas, į kurį galiausiai reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

O čia yra dokumentų sąrašas, kuriuos PRIVALAI naudoti atsakydamas į konkretų paieškos klausimą:
{SEPARATOR_LINE}
---document_text---
{SEPARATOR_LINE}

Pastabos:
   - naudok tik tuos dokumentus, kurie yra aktualūs konkrečiam paieškos klausimui IR apie kuriuos ŽINAI, kad jie \
taikomi klausimo kontekstui! Pavyzdys: kontekstas apie tai, ką Nike darė, kad skatintų pardavimus, \
o klausimas apie tai, ką Puma daro pardavimams skatinti – NENAUDOK JOKIOS \
informacijos apie Nike! Net jei kontekstas nekalba apie Nike pardavimus, o tik apie \
„pardavimų skatinimą“ apskritai (be įmonių), vis tiek negalima naudoti tokios informacijos! \
Privalai būti tikras dėl konteksto teisingumo. Jei abejoji – nenaudok to dokumento!
   - itin svarbu vengti fantazavimo ir informacijos ištraukimo iš konteksto.
   - aiškiai nurodyk bet kokias prielaidas, kurias darai savo atsakyme.
   - nors pirminis klausimas svarbus, daugiausia dėmesio skirk konkrečiam paieškos klausimui. \
Tai yra tavo užduotis.
   - dar kartą – nenaudok/cituok jokių dokumentų, dėl kurių nesate 100% tikras, kad jie aktualūs \
KONKREČIAM klausimo kontekstui! IR NESPĖLIIOK, sakydamas „panašu, kad šis kontekstas tinka“. \
TAIP DARYTI NEGALIMA. Jei klausimas apie „geltoną karį“, o dokumentuose yra tik „kario“ paminėjimas, \
aiškiai pasakyk „nėra paminėta geltonas karis konkrečiai“ ir IGNORUOK tą dokumentą. Jei \
vis dėlto stipriai įtari, kad dokumentas aktualus, gali jį panaudoti, bet PRIVALAI aiškiai \
nurodyti, kad nesi 100% tikras ir kad dokumente neminimas „geltonas karis“ (kaip pavyzdys).
Jei konkreti sąvoka ar terminas nėra pateiktas, atsakymas turi tai aiškiai įvardyti prieš \
teikiant bet kokią susijusią informaciją.
   - Visada pradėk atsakymą tiesiogine fraze apie tai, ar dokumentuose buvo rasta \
tiksli frazė ar reikšmė.
   - pateik tik TRUMPĄ atsakymą, kuris i) pateikia prašytą informaciją, jei klausimas yra \
labai konkretus, ii) cituoja atitinkamus dokumentus atsakymo pabaigoje, iii) pateikia TRUMPĄ \
aukšto lygio santrauką iš cituotų dokumentų, nurodydamas dokumentus, kurie yra labiausiai \
aktualūs konkrečiam klausimui.

{TOOL_OUTPUT_FORMAT}
"""
)


CUSTOM_TOOL_PREP_PROMPT = PromptTemplate(
    f"""
Tau pateikiamas VIENAS įrankis ir naudotojo užklausa, kurią įrankis turėtų spręsti. Taip pat turi 
prieigą prie įrankio aprašymo ir platesnio pirminio klausimo. Pirminis klausimas gali suteikti 
papildomą kontekstą, bet TAVO UŽDUOTIS – pagal naudotojo užklausą sugeneruoti 
įrankio iškvietimo argumentus.

Štai konkretus užklausos tekstas, kuriam reikia sukurti įrankio argumentus:
{SEPARATOR_LINE}
---query---
{SEPARATOR_LINE}

Štai pirminis klausimas, į kurį galiausiai reikia atsakyti (naudok tik kaip papildomą kontekstą):
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai įrankio aprašymas:
{SEPARATOR_LINE}
---tool_description---
{SEPARATOR_LINE}

Pastabos:
   - atsižvelk į įrankio detales kurdamas iškvietimo argumentus.
   - nors pirminis klausimas svarbus, susitelk į konkretų užklausos tekstą, 
kurdamas įrankio iškvietimo argumentus.
   - atkreipk dėmesį į įrankio detales ir suformuok atsakymą tokiu formatu, kokio įrankis tikisi.

ĮRANKIO IŠKVIETIMO ARGUMENTAI:
"""
)


OKTA_TOOL_USE_SPECIAL_PROMPT = PromptTemplate(
    f"""
Tu puikiai moki suformatuoti Okta atsakymą ir pateikti trumpą samprotavimą bei atsakymą 
natūralia kalba, kad atsakytum į konkretų užklausos tekstą (ne į pirminį klausimą!), jei įmanoma.

Štai konkretus užklausos tekstas:
{SEPARATOR_LINE}
---query---
{SEPARATOR_LINE}

Štai pirminis klausimas, į kurį galiausiai reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai įrankio atsakymas:
{SEPARATOR_LINE}
---tool_response---
{SEPARATOR_LINE}

Požiūris:
   - pradėk atsakymą suformatuodamas žalią Okta atsakymą įskaitomu būdu.
   - tada pabandyk labai glaustai ir konkrečiai atsakyti į konkretų užklausos tekstą, jei įmanoma. 
Jei Okta informacija, regis, nėra aktuali, tiesiog pasakyk, kad Okta informacija 
nesusijusi su konkrečia užklausa.

Gairės:
   - naudok pirminį klausimą tik kaip kontekstą, bet jo neatsakinėk. Atsakyk 
į „konkretų užklausos tekstą“, jei įmanoma.
   - ATSIREMK TIK į Okta atsakymą. NENAUDOK savų žinių!

ATSAKYMAS:
"""
)


CUSTOM_TOOL_USE_PROMPT = PromptTemplate(
    f"""
Tu puikiai moki suformatuoti įrankio atsakymą į trumpą samprotavimą ir atsakymą 
natūralia kalba, kad atsakytum į konkretų užklausos tekstą.

Štai konkretus užklausos tekstas:
{SEPARATOR_LINE}
---query---
{SEPARATOR_LINE}

Štai pirminis klausimas, į kurį galiausiai reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai įrankio atsakymas:
{SEPARATOR_LINE}
---tool_response---
{SEPARATOR_LINE}

Pastabos:
   - aiškiai nurodyk savo atsakyme, jei įrankio atsakymas nepateikė aktualios informacijos 
arba netinka šiam konkrečiam kontekstui. Neišgalvok informacijos!
   - itin svarbu vengti fantazavimo ir informacijos ištraukimo iš konteksto.
   - aiškiai nurodyk bet kokias prielaidas, kurias darai savo atsakyme.
   - nors pirminis klausimas svarbus, daugiausia dėmesio skirk konkrečiam užklausos tekstui. 
Tai yra tavo užduotis.

Prašome pateikti glaustą atsakymą 
į konkretų užklausos tekstą, remiantis įrankio atsakymu.
Jei įrankio apibrėžimas ir atsakymas nepateikė informacijos, aktualios konkrečiam tekstui, 
pradėk trumpu teiginiu, pavyzdžiui: „Nepavyko rasti informacijos apie geltoną karį konkrečiai, 
tačiau radau informaciją apie karį...“.

ATSAKYMAS:
   """
)


TEST_INFO_COMPLETE_PROMPT = PromptTemplate(
    f"""
Tu esi ekspertas, vertinantis, ar 
aukšto lygio planas, sukurtas informacijos surinkimui siekiant išspręsti aukštesnio lygio 
problemą, yra pakankamai įvykdytas IR ar pati problema 
gali būti išspręsta. Šį vertinimą atlieki žiūrėdamas į iki šiol surinktą informaciją.

Štai aukštesnio lygio problema, į kurią reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai pradžioje sukurtas aukšto lygio planas:
{SEPARATOR_LINE}
---high_level_plan---
{SEPARATOR_LINE}

Štai sub-klausimų, jų santraukų ir išgautų teiginių („faktų“) sąrašas:
{SEPARATOR_LINE}
---questions_answers_claims---
{SEPARATOR_LINE}

Galiausiai, čia yra ankstesnė pokalbio istorija (jei yra), kuri gali būti aktuali 
atsakant į klausimą:
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Štai įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

GAIRĖS:
  - pažvelk į aukšto lygio planą ir įvertink, ar iki šiol surinkta informacija 
pakankamai detaliai apima žingsnius, kad galėtume su pasitikėjimu atsakyti į aukštesnio lygio problemą.
  - jei ne, suformuluok „spragų“ sąrašą, kurias reikia užpildyti prieš atsakant į aukštesnio lygio problemą.
  - labai atidžiai pagalvok, ar informacijos pakanka ir ar jos detalumas pakankamas 
atsakyti į aukštesnio lygio problemą.

Prašome suformatuoti atsakymą kaip JSON žodyną šiuo formatu:
{{
        "reasoning": "<tavo analizė 3–6 sakiniais, ar, tavo manymu, 
planas pakankamai įvykdytas ir ar galima atsakyti į aukštesnio lygio problemą>",
"complete": "<atsakyk tik True (jei baigta) arba False (jei dar nebaigta ir yra spragų)>",
"gaps": "<spragų sąrašas, kurias reikia užpildyti prieš atsakant į aukštesnio lygio problemą. 
Pateik formatu ['spraga 1', 'spraga 2', ...]. Jei spragų nėra, pateik []>"
}}
"""
)


FINAL_ANSWER_PROMPT_W_SUB_ANSWERS = PromptTemplate(
    f"""
Tu puikiai moki atsakyti į naudotojo klausimą, remdamasis anksčiau sugeneruotais sub-atsakymais 
ir dokumentų sąrašu, kurie buvo naudoti tiems sub-atsakymams sukurti. Dokumentų sąrašas 
skirtas tolesnei nuorodai norint gauti daugiau detalių.

Štai klausimas, į kurį reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai sub-klausimų, jų atsakymų ir išgautų faktų/teiginių sąrašas:
{SEPARATOR_LINE}
---iteration_responses_string---
{SEPARATOR_LINE}

Galiausiai, čia yra ankstesnė pokalbio istorija (jei yra), kuri gali būti aktuali 
atsakant į klausimą:
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

GAIRĖS:
 - atkreipk dėmesį, kad sub-atsakymai į sub-klausimus yra sukurti būti aukšto lygio, daugiausia 
fokusuoti į citatas ir pateikti keletą faktų. Tačiau pagrindinis turinys turėtų būti cituotuose dokumentuose.
 - Labai atidžiai stebėk, ar sub-atsakymuose aiškiai pasakyta, ar domina tikslus terminas! 
Jei negali patikimai tuo remtis, kad sukurtum atsakymą, PRIVALAI kvalifikuoti atsakymą, pvz., 
„xyz nėra aiškiai paminėta, tačiau panaši sąvoka abc minima, ir radau...“
- jei dokumentuose/sub-atsakymuose aiškiai neminimas konkrečiai dominantis dalykas 
su specifika (pvz., „geltonas karis“ vs „karis“), pradžioje PRIVALAI pažymėti, kad 
pateikiamas kontekstas paremtas mažiau specifine sąvoka.
- užtikrink, kad iš dokumento paimtas tekstas nebūtų ištrauktas iš konteksto.
- nieko neišgalvok! Naudok tik pateiktą informaciją dokumentuose arba, jei sub-atsakymo nėra, 
patį sub-atsakymą.
- Pateik apgalvotą, glaustą, bet detalią išvadą.
- Cituok šaltinius inline formatu [[2]][[4]] ir pan.! Dokumentų numeriai pateikti aukščiau.
- Jei nesi tikras, ar informacija tikrai susijusi su tema, pažymėk dviprasmybę atsakyme.

ATSAKYMAS:
"""
)


FINAL_ANSWER_PROMPT_WITHOUT_SUB_ANSWERS = PromptTemplate(
    f"""
Tu puikiai moki atsakyti į naudotojo klausimą, remdamasis 
sub-klausimų metu gautais dokumentais ir, jei yra, sub-atsakymais 
(pastaba, ne kiekvienam sub-klausimui būtinai yra sub-atsakymas).

Štai klausimas, į kurį reikia atsakyti:
{SEPARATOR_LINE}
---base_question---
{SEPARATOR_LINE}

Štai sub-klausimų, jų atsakymų (jei yra) ir gautų dokumentų (jei yra) sąrašas:
{SEPARATOR_LINE}
---iteration_responses_string---
{SEPARATOR_LINE}

Galiausiai, čia yra ankstesnė pokalbio istorija (jei yra), kuri gali būti aktuali 
atsakant į klausimą:
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Štai įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

GAIRĖS:
 - atkreipk dėmesį, kad sub-atsakymai (jei yra) yra aukšto lygio ir daugiausia 
fokusuojasi į citatas ir pateikia kelis faktus. Pagrindinė informacija turėtų būti 
sub-atsakymuose cituojamuose dokumentuose.
 - Labai atidžiai stebėk, ar sub-atsakymuose (jei yra) aiškiai pasakyta, ar domina tikslus terminas! 
Jei negali patikimai tuo remtis, PRIVALAI kvalifikuoti atsakymą, pvz., 
„xyz nėra aiškiai paminėta, tačiau panaši sąvoka abc minima, ir radau...“
- jei dokumentuose/sub-atsakymuose (jei yra) aiškiai neminimas konkrečiai dominantis dalykas 
su specifika, pradžioje PRIVALAI pažymėti, kad 
pateikiamas kontekstas paremtas mažiau specifine sąvoka.
- užtikrink, kad iš dokumento paimtas tekstas nebūtų ištrauktas iš konteksto.
- nieko neišgalvok! Naudok tik pateiktą informaciją dokumentuose arba, jei sub-atsakymo nėra, 
patį sub-atsakymą.
- Pateik apgalvotą, glaustą, bet detalią išvadą.
- Cituok šaltinius inline formatu [[2]][[4]] ir pan.! Dokumentų numeriai pateikti aukščiau.
- Jei nesi tikras, ar informacija tikrai susijusi su tema, pažymėk dviprasmybę atsakyme.
- Dar kartą: CITUOK ŠALTINIUS inline formatu [[2]][[4]] ir pan.! Tai KRITINĖ dalis!

ATSAKYMAS:
"""
)


GET_CLARIFICATION_PROMPT = PromptTemplate(
    f"""
Tu puikiai moki užduoti patikslinančius klausimus tais atvejais, kai 
pirminis klausimas nėra pakankamai aiškus. Tavo užduotis – prieš siunčiant klausimą gilaus tyrimo agentui, 
paklausti būtinų patikslinimų.

Tavo užduotis NĖRA atsakyti į klausimą. Vietoj to, privalai surinkti būtiną informaciją 
atsižvelgiant į turimus įrankius ir jų galimybes, aprašytas žemiau. Jei įrankiui nebūtini 
konkretūs duomenys, jų neprašyk. Klausimas gali būti ir neapibrėžtas, jei įrankis su tuo susitvarkys. 
Taip pat turėk omenyje, kad naudotojas gali įvesti tik raktinį žodį be jokio konteksto ar instrukcijų. Tokiais atvejais 
daryk prielaidą, kad naudotojas ieško bendros informacijos apie temą.

Tavo dispozicijoje yra ---num_available_tools--- įrankių, ---available_tools---.

Štai įrankių aprašymai:
---tool_descriptions---

Jei naudojamas žinių grafikas, čia yra esybių ir ryšių tipų aprašymas:
---kg_types_descriptions---

Įrankiai ir esybių bei ryšių tipai pateikiami tik kaip kontekstas, padedantis nuspręsti, ar 
klausimas reikalauja patikslinimo.

Štai naudotojo klausimas:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Štai ankstesnė pokalbio istorija (jei yra), kuri gali būti aktuali 
atsakant į klausimą:
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

PASTABOS:
  - tai turi būti įvertinta remiantis vien tik tavo vidinėmis žiniomis.
  - jei būtini patikslinimai, nustatyk "feedback_needed" į true ir 
suformuluok IKI 3 SUNUMERUOTUS patikslinimo klausimus, reikalingus klausimui patikslinti.
Naudok formatą: '1. <klausimas 1>\n2. <klausimas 2>\n3. <klausimas 3>'.
Leidžiama klausti nulį, vieną, du arba tris patikslinimus.
  - jei patikslinimų nereikia, nustatyk "feedback_needed" į false ir 
"feedback_request" reikšmę palik „no feedback required“.
  - klausk patikslinimų tik tada, kai ta informacija yra labai svarbi tinkamam atsakymui. 
NEKLAUSK papildomų smulkmenų, kurios nėra būtinos gilaus tyrimo agentui.

PAVYZDŽIAI:
--
I. Naudotojo klausimas: "Kokia yra Prancūzijos sostinė?"
   Reikia patikslinimų: false
   Prašymas dėl patikslinimo: 'no feedback required'
   Priežastis: Klausimas aiškus ir nereikalauja jokių patikslinimų.

--

II. Naudotojo klausimas: "Kiek yra bilietų?"
   Reikia patikslinimų: true
   Prašymas dėl patikslinimo: '1. Ką turite omenyje „bilietai“?'
   Priežastis: „Bilietai“ gali reikšti daug skirtingų objektų, pvz., paslaugų bilietus, Jira užduotis ir t. t. 
Be šito daugiau informacijos nereikia; pakanka vieno patikslinimo klausimo.

--

III. Naudotojo klausimas: "Kiek PR buvo sujungta praėjusį mėnesį?"
   Reikia patikslinimų: true
   Prašymas dėl patikslinimo: '1. Ar turite omenyje konkretų repo dėl Pull Requests?'
   Priežastis: „Sujungta“ aiškiai leidžia suprasti, kad PR reiškia pull requests, todėl to 
papildomai tikslinti nereikia. Tačiau repo nurodymas svarbus, nes jų gali būti daug. 
Be to, daugiau informacijos nereikia; pakanka vieno patikslinimo klausimo.

--

IV. Naudotojo klausimas: "Apie ką yra naujausi PR?"
   Reikia patikslinimų: true
   Prašymas dėl patikslinimo: '1. Ką reiškia PR? Pull Requests ar kas kita?\n2. Ką reiškia „naujausi“? Naujausi <x> PR, ar PR iš šios savaitės? Prašome patikslinti.\n3. Kokia veikla matuojama laike? Sukūrimas? Uždarymas? Atnaujinimas? ir pan.'
   Priežastis: Reikia patikslinti, ką reiškia PR. Taip pat „naujausi“ nėra aiškiai apibrėžta 
ir reikalauja kelių patikslinimų.

--

V. Naudotojo klausimas: "Palyginkite Adidas ir Puma"
   Reikia patikslinimų: true
   Prašymas dėl patikslinimo: '1. Kokiose srityse norite palyginimo?\n2. Ar domina konkretus laikotarpis?\n3. Ar norite informacijos konkrečiu formatu?'
   Priežastis: Klausimas per platus ir reikalauja specifikavimo pagal sritis ir laikotarpį (todėl 1 ir 2 patikslinimai). 
Taip pat naudotojui gali reikėti konkretaus formato (pvz., lentelė ar tekstas), todėl 3 patikslinimas. 
Žinoma, galėtų būti ir daugiau klausimų, bet šie trys yra svarbiausi.

PATEIK FORMATU:
{{
        "clarification_needed": <true arba false, ar, tavo manymu, reikia patikslinimo>
   "clarification_question": "<patikslinimo klausimai, jei clarification_needed yra true; 
kitaip – 'no clarification needed'. Pateik kaip eilutę, o ne sąrašą; jei keli klausimai, 
naudoji numeruotą sąrašą vienoje eilutėje>"
}}

ATSAKYMAS:
"""
)


REPEAT_PROMPT = PromptTemplate(
    """
Tau perduota informacija, ir tavo paprasta užduotis – PAKARTOTI informaciją PAŽODIŠKAI.

Štai pradinė informacija:

---original_information---

TAVO PAŽODIŠKAS PAKARTOJIMAS pradinės informacijos:
"""
)


BASE_SEARCH_PROCESSING_PROMPT = PromptTemplate(
    f"""
Tu puikiai moki apdoroti paieškos užklausą tam, kad 
suprastum, kokie dokumentų tipai turėtų būti įtraukti į paiešką (jei tai nurodyta užklausoje), 
ar užklausoje numanomas laiko filtras, ir perrašyti 
užklausą į formuluotę, labiau tinkančią paieškai pagal prognozuotus 
dokumentų tipus.

Štai pradinė paieškos užklausa:
{SEPARATOR_LINE}
---branch_query---
{SEPARATOR_LINE}

Štai galimų dokumentų tipų, prieinamų paieškai, sąrašas:
{SEPARATOR_LINE}
---active_source_types_str---
{SEPARATOR_LINE}
Norėdamas interpretuoti, ką reiškia dokumentų tipai, remkis savo žiniomis.

Dabartinis laikas yra ---current_time---.

Atsižvelgdamas į tai, pabandyk nustatyti nurodytus šaltinių tipus ir laiko filtrus bei 
perrašyti užklausą.

Gairės:
 - jei nustatyti vienas ar keli šaltinių tipai 'specified_source_types' lauke, 
juos PRIVALOMA išimti iš perrašytos užklausos!
   Ypač ieškok frazių kaip „...mūsų Google docs...“, „...mūsų Google skambučiuose...“, 
   tokiu atveju šaltinio tipas yra 'google_drive' arba 'gong', ir jų neturi būti perrašytoje užklausoje.
 - jei nustatytas laiko filtras 'time_filter', jo taip pat NEGALI būti perrašytoje užklausoje. 
   Ieškok frazių kaip „...šiais metais...“, „...šį mėnesį...“ ir pan.

Pavyzdys:
užklausa: 'rask informaciją apie klientus mūsų Google drive dokumentuose šiais metais' ->
   specified_source_types: ['google_drive']
   time_filter: '2025-01-01'
   rewritten_query: 'informacija apie klientus'

Prašome suformatuoti atsakymą kaip JSON žodyną šiuo formatu:
{{
        "specified_source_types": "<dokumentų tipų sąrašas, kuriuos būtina įtraukti į paiešką. 
NURODYK tik tuos tipus, kurie AKIVAIZDŽIAI paminėti užklausoje. Jei ne, grąžink [].>",
"time_filter": "<pabandyk identifikuoti, ar užklausoje aiškiai ar numanomai yra (pradžios) laiko filtras. 
Jei yra, pateik pradžios datą 'YYYY-MM-DD' formatu. Jei nėra, 'None'.>",
"rewritten_query": "<sudėliok trumpą perrašytą užklausą, tinkamesnę paieškai pagal prognozuotus 
dokumentų tipus. Išlaikyk tikslumą, neprarasdamas kritinio konteksto.>"
}}

ATSAKYMAS:
"""
)


EVAL_SYSTEM_PROMPT_WO_TOOL_CALLING = """
Tu puikiai moki 1) nustatyti, ar klausimą gali atsakyti 
tiesiogiai remdamasis vien savo žiniomis ir pokalbio istorija (jei yra), ir 2) iš tikrųjų 
atsakyti į užklausą, jei 
ji NEREIKALAUJA ir nebūtų smarkiai naudinga išoriniams įrankiams 
(jokių paieškų, veiksmų ar išorinių žinių).
"""


DEFAULT_DR_SYSTEM_PROMPT = """
Tu esi naudingas asistentas, puikiai atsakantis į klausimus ir atliekantis užduotis. 
Gali turėti arba neturėti prieigos prie išorinių įrankių, tačiau visada stengiesi geriausiai 
atsakyti į pateiktus klausimus ar užduotis apgalvotai ir atsakingai. 
Visada nurodyk neapibrėžtumus ir neatsiremki į iš konteksto ištrauktą informaciją. Jei 
abejoji – nenaudok tokios informacijos arba bent jau aiškiai pažymėk neapibrėžtumą.
"""


GENERAL_DR_ANSWER_PROMPT = PromptTemplate(
    f"""\
Žemiau pateiktas naudotojo klausimas ir, galbūt, ankstesnė pokalbio istorija, 
į kurią gali atsiremti kaip į kontekstą. Dabartinis laikas – ---current_time---.
Prašome atsakyti tiesiogiai, nurodant bet kokius neapibrėžtumus.

Štai naudotojo klausimas:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Štai pokalbio istorija (jei yra):
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

"""
)


DECISION_PROMPT_WO_TOOL_CALLING = PromptTemplate(
    f"""
Štai pokalbio istorija (jei yra):
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Štai įkeltas kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Galimi įrankiai:
{SEPARATOR_LINE}
---available_tool_descriptions_str---
{SEPARATOR_LINE}

Štai dokumentų tipai, prieinami paieškai (jei yra):
{SEPARATOR_LINE}
---active_source_type_descriptions_str---
{SEPARATOR_LINE}

Ir galiausiai – klausimas, į kurį reikia atsakyti:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Prašome atsakyti kaip JSON žodynas:
{{
        "reasoning": "<vienas sakinys, ar, tavo manymu, reikia naudoti įrankį>",
"decision": "<'LLM' JEI NEREIKIA ĮRANKIO ir gali/ reikia atsakyti tiesiogiai, 
arba 'TOOL' JEI REIKIA ĮRANKIO>"
}}

"""
)


ANSWER_PROMPT_WO_TOOL_CALLING = PromptTemplate(
    f"""
Štai pokalbio istorija (jei yra):
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Štai įkeltas kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Ir galiausiai – klausimas:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Prašome atsakyti tiesiogiai.

"""
)


EVAL_SYSTEM_PROMPT_W_TOOL_CALLING = """
Taip pat gali pasirinkti naudoti įrankius norėdamas gauti papildomos informacijos. Tačiau jei atsakymas 
akivaizdžiai žinomas viešai ir tau žinomas – gali atsakyti tiesiogiai.
"""


DECISION_PROMPT_W_TOOL_CALLING = PromptTemplate(
    f"""
Štai pokalbio istorija (jei yra):
{SEPARATOR_LINE}
---chat_history_string---
{SEPARATOR_LINE}

Štai įkeltas kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Štai dokumentų tipai, prieinami paieškai (jei yra):
{SEPARATOR_LINE}
---active_source_type_descriptions_str---
{SEPARATOR_LINE}

Ir galiausiai – klausimas:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}
"""
)


DEFAULLT_DECISION_PROMPT = """
Tu esi Asistentas, puikiai nusprendžiantis, kurį įrankį naudoti toliau, kad 
surinktum informaciją, reikalingą atsakyti į naudotojo klausimą/užklausą. Gali būti pateikta 
informacija, ir tavo užduotis – nuspręsti, kuriuos įrankius naudoti ir kokias užklausas 
jiems siųsti.
"""


WEB_SEARCH_URL_SELECTION_PROMPT = PromptTemplate(
    f"""
    Tavo užduotis – rinkti informaciją iš interneto su paieškos užklausa:
    {SEPARATOR_LINE}
    ---search_query---
    {SEPARATOR_LINE}
    Tai vienas paieškos žingsnis, siekiant atsakyti į naudotojo pirminį klausimą:
    {SEPARATOR_LINE}
    ---base_question---
    {SEPARATOR_LINE}

    Tu atlikai paiešką ir gavai šiuos rezultatus:

    {SEPARATOR_LINE}
    ---search_results_text---
    {SEPARATOR_LINE}

    Tavo užduotis:
    Pasirink URL adresus, kurie yra labiausiai aktualūs paieškos užklausai ir labiausiai tikėtini padėti atsakyti į pirminį klausimą.

    Remdamasis aukščiau pateiktais rezultatais, grąžink JSON objektą šiuo formatu:

    {{
        "urls_to_open_indices": ["<url1 indeksas>", "<url2 indeksas>", "<url3 indeksas>"]
    }}

    Gairės:
    - Atsižvelk į pavadinimą, iškarpą ir URL priimdamas sprendimą
    - Susitelk į kokybę, o ne kiekybę
    - Pirmenybę teik: oficialiai dokumentacijai, pirminiams šaltiniams, patikimoms organizacijoms, naujiems įrašams greitai besikeičiančioms temoms
    - Užtikrink šaltinių įvairovę: stenkitės įtraukti 1–2 oficialius dokumentus, 1 paaiškinamąjį šaltinį, 1 naujienų/pranešimo šaltinį, 1 kodą/pavyzdį ir pan.
    """
)


ORCHESTRATOR_DEEP_ITERATIVE_DECISION_PROMPT = PromptTemplate(
    f"""
Iš esmės, turi atsakyti į naudotojo užklausą. Tam turi įvairių įrankių, kuriuos gali
kviesti iteratyviai. Taip pat turi pradinį planą, kuris turėtų nukreipti tavo mąstymą.

Gali jau turėti atsakymų į ankstesnius klausimus, kuriuos generavai ankstesnėse iteracijose, ir taip pat
turi aukšto lygio planą, kuris tau buvo pateiktas.

Tavo užduotis – nuspręsti, kurį įrankį kviesti toliau ir kokį konkretų klausimą/užduotį jam pateikti,
atsižvelgiant į jau gautus atsakymus ir pareikštus teiginius bei vadovaujantis pradiniu planu.

(Dabar planuoji ---iteration_nr--- iteraciją.) Taip pat dabartinis laikas – ---current_time---.

Tavo dispozicijoje yra ---num_available_tools--- įrankių, 
---available_tools---.

---tool_descriptions---

---kg_types_descriptions---

Štai pirminis klausimas, į kurį turi atsakyti:
{SEPARATOR_LINE}
---question---
{SEPARATOR_LINE}

Štai aukšto lygio planas:
{SEPARATOR_LINE}
---current_plan_of_record_string---
{SEPARATOR_LINE}

Štai iki šiol gautų atsakymų istorija (jei yra):
{SEPARATOR_LINE}
---answer_history_string---
{SEPARATOR_LINE}

Štai įkeltas naudotojo kontekstas (jei yra):
{SEPARATOR_LINE}
---uploaded_context---
{SEPARATOR_LINE}

Kad išvengtume dubliavimo, čia yra ankstesnių klausimų ir naudotų įrankių sąrašas:
{SEPARATOR_LINE}
---question_history_string---
{SEPARATOR_LINE}

Taip pat, recenzentas galėjo neseniai nurodyti informacijos spragas, kurios trukdytų
atsakyti į pirminį klausimą. Jei spragos pateiktos, būtinai į jas atsižvelk konstruodamas kitus klausimus.

Štai recenzento nurodytų spragų sąrašas:
{SEPARATOR_LINE}
---gaps---
{SEPARATOR_LINE}

Kurdami naujus klausimus, peržiūrėk ankstesnius klausimus ir atsakymus (aukščiau), kad
NEKARTOTUM TO PATIES klausimo TAM PAČIAM įrankiui!

Štai įrankių vidutinės kainos, kurias turėtum apsvarstyti priimdamas sprendimą:
{SEPARATOR_LINE}
---average_tool_costs---
{SEPARATOR_LINE}

Štai likęs laiko biudžetas klausimui atsakyti:
{SEPARATOR_LINE}
---remaining_time_budget---
{SEPARATOR_LINE}

ĮRANKIŲ ATSKYRIMAS/SANTYKIS:
---tool_differentiation_hints---

ĮVAIRŪS PATARIMAI:
   - LABAI svarbu pažvelgti į aukšto lygio planą ir įvertinti, kurie žingsniai jau
atrodo pakankamai atsakyti, o kurioms sritims reikia daugiau informacijos.
   - BE CURIOUS! Suformuluok įdomius klausimus, kurie padėtų geriau suprasti informaciją, \
reikalingą atsakyti į pirminį klausimą.
   - jei manai, kad a) gali atsakyti į klausimą remdamasis turima informacija IR b)
aukšto lygio plano informacija pakankamai aprėpta, gali naudoti „{CLOSER}“ įrankį.
   - pirmiausia apsvarstyk, ar jau gali atsakyti į klausimą remdamasis turima informacija. 
Taip pat įvertink, ar planas rodo, jog darbas baigtas. Jei taip – naudok „{CLOSER}“.
   - jei reikia daugiau informacijos, nes sub-klausimas nebuvo pakankamai atsakytas,
gali sugeneruoti modifikuotą ankstesnio žingsnio versiją, taip efektyviai modifikuodamas planą.
   - gali svarstyti tik tokį įrankį, kurio kaina telpa į likusį laiko biudžetą!
   - jei ankstesnės išvados atrodo prieštaringos ar reikalauja patikrinimo, gali suformuluoti
patikrinimo klausimus, jei jie tinka pasirinktam įrankiui.
   - gali klausti ir tyrinėjančių klausimų, kurie ne tiesiogiai veda į galutinį atsakymą, bet padės
geriau suprasti temą (rinką, segmentą, produktą, technologiją ir pan.), kad užduotum geresnius vėlesnius klausimus.
   - NEKARTOK beveik identiško klausimo tam pačiam įrankiui! Jei iš vieno įrankio negavai
gera atsakymo, gali pabandyti kitą, jei jis tinkamas tam pačiam tikslui.
   - Dėmesys – NAUJAI INFORMACIJAI! Stenkis formuluoti klausimus, kurie
      - užpildo spragas pirminio klausimo atžvilgiu
      - yra įdomūs ankstesnių atsakymų tęsiniai
      - patikrina pirminę informaciją arba papildo ją reikšmingomis detalėmis

   - Again, DO NOT repeat essentially the same question usiong the same tool!! WE DO ONLY WANT GENUNINELY \
NEW INFORMATION!!! Jei pavyzdžiui, ankstesnėje klausyme iki SEARCH įrankio buvo „Kas yra pagrindinis Nike problemas?“ \
ir atsakymas buvo „Dokumentai neišreikšti konkrečios problemos...“, DABAR NEPRAŠOM SEARCH įrankio kita kartą \
klausimą, pavyzdžiui, „Ar yra problemos, kurią paminėjo Nike?“, nes tai būtų beveik identiška klausimas, kuris \
buvo atsakytas SEARCH įrankio kita kartą anksčiau.

YOUR TASK:
tu turi sukonstruoti kitą klausimą ir pasirinkti įrankį, kuriam jį siųsti. Tam apsvarstyk \
pirminį klausimą, tavo turimus įrankius, iki šiol gautus atsakymus \
(iš ankstesnių iteracijų arba iš pokalbio istorijos) ir pateiktą priežastį, kodėl reikia daugiau \
tyrimų. Įsitikink, kad klausimas yra konkretus ir – jei taikoma – \
REMiasi iki šiol gautomis įžvalgomis, kad gautum naują, tikslingą informaciją, reikalingą \
atsakyti į pirminį klausimą.

Štai apytikslė schema, kaip nuspręsti, ar jau metas kviesti {CLOSER} įrankį:
{DONE_STANDARD[ResearchType.DEEP]}

Prašome suformatuoti atsakymą kaip JSON žodyną šiuo formatu:
{{
        "reasoning": "<tavo samprotavimas 2–4 sakiniais, 
vadovaudamasis pirminiu klausimu, turimais atsakymais ir planu>",
   "next_step": {{
        "tool": "<---tool_choice_options--->",
                  "questions": "<klausimas, kurį nori pateikti įrankiui. 
Pavyzdžiui:
---tool_question_hints---
Taip pat įsitikink, kad kiekvienas klausimas TURI PILNĄ KONTEKSTĄ; 
venk 'parodyk kitus pavyzdžius', o naudok 'parodyk pavyzdžius, kurie nėra apie mokslą'.
Taip pat, jei galutinis klausimas prašo palyginti kelias galimybes ar esybes, PRIVALAI \
KLAUSTI apie KIEKVIENĄ galimybę ar esybę ATSKIRAI, nes vėlesniuose žingsniuose galėsi tiek \
užduoti daugiau klausimų, tiek palyginti ir įvertinti surinktą informaciją! \
(Pavyzdžiui, „kodėl Puma padarė X kitaip nei Adidas...“ turėtų virsti klausimais \
„kaip Puma padarė X..“ ir „kaip Adidas padarė X..“, o ne „kaip Puma ir Adidas padarė X..“)>"}}
}}
"""
)
