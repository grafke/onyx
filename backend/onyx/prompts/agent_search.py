from onyx.agents.agent_search.shared_graph_utils.constants import (
    AGENT_ANSWER_SEPARATOR,
)

# Standartai
SEPARATOR_LINE = "-------"
SEPARATOR_LINE_LONG = "---------------"
UNKNOWN_ANSWER = "Neturiu pakankamai informacijos, kad galėčiau atsakyti į šį klausimą."
NO_RECOVERED_DOCS = "Nerasta jokių aktualių duomenų"
YES = "yes"
NO = "no"

# Konteksto rėminimas / šablonai
HISTORY_FRAMING_PROMPT = f"""
Papildomam kontekstui – štai iki šio klausimo buvusi pokalbio istorija:
{SEPARATOR_LINE}
{{history}}
{SEPARATOR_LINE}
""".strip()


COMMON_RAG_RULES = f"""
SVARBIAUSIOS TAISYKLĖS:
 - Jei negalite patikimai atsakyti remdamiesi TIK pateikta informacija, pasakykite, kad negalite patikimai atsakyti. \
Galite pateikti papildomų faktų, kuriuos sužinojote, bet nebandykite išgalvoti atsakymo.

 - Jei informacija tuščia arba neaktuali, tiesiog pasakykite "{UNKNOWN_ANSWER}".

 - Jei informacija aktuali, bet nepakankamai išsami galutinei išvadai, pateikite atsakymą tiek, kiek galite, bet aiškiai nurodykite, \
kad informacija nėra galutinė ir kodėl.

- Kategorijas konstruodami/vertindami daugiau dėmesio skirkite pateiktam kontekstui, o ne pačiam klausimui! \
Pavyzdys: jei klausimas – apie A įmonės produktus, o kontekste pateikiamas produktų sąrašas, \
NESPRESKITE automatiškai, kad jie priklauso A įmonei! Negalite jų nurodyti kaip A įmonės produktų, \
net jei klausimas apie A įmonės produktus. Vietoj to sakykite, pavyzdžiui: \
"Čia yra keli produktai, bet negaliu pasakyti, ar jie priklauso A įmonei: \
<išvardykite produktus>". Ypač SVARBU, kad atsakymas atspindėtų faktus. Taip pat atsižvelkite į \
dokumento pavadinimą ir kitą informaciją. Jei tai nepatvirtina, jog produktai priklauso A įmonei, \
tada taip ir nerašykite – aiškiai pažymėkite neapibrėžtumą.

- Jei kontekste yra sąrašas elementų su susieta informacija, kuri atrodo atitinkanti klausime minimas kategorijas, \
bet nėra aišku, ar tai būtent ta kategorija, pateikite su išlyga. Pavadinkite, pvz.: \
"Nesu tikras, ar šie elementai (ar pateikta informacija) yra būtent [aktuali kategorija] arba ar tai visi [konkretūs]" \
ir po to pateikite sąrašą.

 - Negrupuokite elementų po viena antrašte, jei ne visi elementai atitinka antraštės kategoriją! \
(Pvz.: "Produktai, kuriuos naudoja A įmonė", kai dalis produktų nėra A įmonės arba tai neaišku.) \
Nurodykite tik tai, kuo esate tikri.

 - NEVYKDYKITE jokių skaičiavimų atsakyme! Tiesiog pateikite faktus.

 - Jei tikslinga, atsakymą dažnai patogu struktūruoti punktais.
""".strip()

ASSISTANT_SYSTEM_PROMPT_DEFAULT = "Jūs esate asistentas, padedantis atsakyti į klausimus."

ASSISTANT_SYSTEM_PROMPT_PERSONA = f"""
Jūs esate asistentas, padedantis atsakyti į klausimus. Daugiau informacijos apie jus:
{SEPARATOR_LINE}
{{persona_prompt}}
{SEPARATOR_LINE}
""".strip()


SUB_QUESTION_ANSWER_TEMPLATE = f"""
Sub-klausimas: Q{{sub_question_num}}
Klausimas:
{{sub_question}}
{SEPARATOR_LINE}
Atsakymas:
{{sub_answer}}
""".strip()


SUB_QUESTION_ANSWER_TEMPLATE_REFINED = f"""
Sub-klausimas: Q{{sub_question_num}}
Tipas: {{sub_question_type}}
Sub-klausimas:
{SEPARATOR_LINE}
{{sub_question}}
{SEPARATOR_LINE}
Atsakymas:
{SEPARATOR_LINE}
{{sub_answer}}
{SEPARATOR_LINE}
""".strip()


# Pagalbinių žingsnių raginimai
ENTITY_TERM_EXTRACTION_PROMPT = f"""
Remiantis pradiniu klausimu ir iš duomenų rinkinio gautu kontekstu, sugeneruokite \
sąrašą subjektų (pvz., įmonės, organizacijos, industrijos, produktai, vietovės ir t. t.), terminų ir konceptų \
(pvz., pardavimai, pajamos ir pan.), kurie yra aktualūs klausimui, ir jų tarpusavio ryšius.

Štai pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Štai gautas kontekstas:
{SEPARATOR_LINE}
{{context}}
{SEPARATOR_LINE}

Pateikite atsakymą JSON formatu, kaip nurodyta:
""".lstrip()


ENTITY_TERM_EXTRACTION_PROMPT_JSON_EXAMPLE = """
{
    "retrieved_entities_relationships": {
        "entities": [
            {
                "entity_name": "<suteikite subjekto pavadinimą>",
                "entity_type": "<suteikite trumpo tipo pavadinimą, pvz., 'company', 'location', ...>"
            }
        ],
        "relationships": [
            {
                "relationship_name": "<suteikite ryšio pavadinimą>",
                "relationship_type": "<trumpas ryšio tipas, pvz., 'sales_to', 'is_location_of', ...>",
                "relationship_entities": ["<susijęs subjektas 1>", "<susijęs subjektas 2>", "..."]
            }
        ],
        "terms": [
            {
                "term_name": "<suteikite termino pavadinimą>",
                "term_type": "<trumpas tipo pavadinimas, pvz., 'revenue', 'market_share', ...>",
                "term_similar_to": ["<panašūs terminai>"]
            }
        ]
    }
}
""".strip()


HISTORY_CONTEXT_SUMMARY_PROMPT = f"""
{{persona_specification}}

Jūsų užduotis – apibendrinti svarbiausias pokalbio tarp naudotojo ir agento istorijos dalis. \
Santrauka turi atlikti dvi funkcijas:
  1) pateikti tinkamą kontekstą naujam klausimui,
  2) užfiksuoti svarbią informaciją, dėl kurios naudotojas gali turėti papildomų klausimų.

Štai klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Štai istorija:
{SEPARATOR_LINE}
{{history}}
{SEPARATOR_LINE}

Pateikite glaustą kontekstą iš istorijos, kad klausimas būtų aiškus ir, prireikus su papildoma \
informacija, galėtų būti atsakytas.

Nenaudokite daugiau nei trijų–keturių sakinių.

Istorijos santrauka:
""".strip()


# PRADINĖ FAZĖ – Sub-klausimai
INITIAL_QUESTION_DECOMPOSITION_PROMPT = f"""
Sukurkite ne daugiau kaip 3 sub-klausimų sąrašą, kurių atsakymai padėtų atsakyti į pradinį klausimą.

Šių sub-klausimų paskirtis gali būti:
  1) suskaidyti klausimą, išskiriant atskirus subjektus (pvz., „palyginkite A ir B įmonių pardavimus“ -> \
[„kokie A įmonės pardavimai“, „kokie B įmonės pardavimai“])

  2) paaiškinti ir/arba panaikinti dviprasmybes (pvz., „koks mūsų pasisekimas su A įmone“ -> \
[„kokie mūsų pardavimai su A įmone“, „koks mūsų rinkos dalis su A įmone“, \
„ar A įmonė yra mūsų referencinis klientas“, ir t. t.])

  3) jei terminas ar metrika iš esmės aiškūs, bet gali sietis su įvairiais subjekto aspektais, \
ir esate su jais susipažinę, galite sukurti specifiškesnius sub-klausimus (pvz., \
„ką darome, kad pagerintume X produkto našumą“, „stabilumą“, „mastelį“ ir pan.)

  4) ištirti atskirus klausimus/sritis, kurie padėtų parengti galutinį atsakymą.

Svarbu:

 - Kiekvienas sub-klausimas turi būti atsakomas RAG sistema. Atitinkamai formuluokite klausimą.
 - Ne tik skaidykite – užtikrinkite tinkamą formą (be „aš“ ir pan.).
 - NEdarykite sub-klausimų, kurie būtų aiškinamieji pačiam naudotojui. Priimkite pateiktą informaciją kaip duotą.

Štai pradinis klausimas, kuriam kuriami sub-klausimai:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

{{history}}

NEĮTRAUKITE jokio kito teksto – tik sub-klausimų sąrašą!
Pateikite kiekvieną klausimą naujoje eilutėje (ir atsakykite TIK su sąrašu!):

 <sub-klausimas>
 <sub-klausimas>
 <sub-klausimas>
 ...

Atsakymas:
""".strip()


INITIAL_QUESTION_DECOMPOSITION_PROMPT_ASSUMING_REFINEMENT = f"""
Sukurkite ne daugiau kaip 3 sub-klausimų sąrašą, kurių atsakymai padėtų atsakyti į pradinį klausimą.

Šių sub-klausimų paskirtis gali būti:
  1) suskaidyti klausimą, išskiriant atskirus subjektus (pvz., „palyginkite A ir B įmonių pardavimus“ -> \
[„kokie A įmonės pardavimai“, „kokie B įmonės pardavimai“])
  2) paaiškinti ir/arba panaikinti dviprasmybes (pvz., „koks mūsų pasisekimas su A įmone“ -> \
[„kokie mūsų pardavimai su A įmone“, „koks mūsų rinkos dalis su A įmone“, \
„ar A įmonė yra mūsų referencinis klientas“, ir t. t.])
  3) jei terminas ar metrika aiškūs, bet gali sietis su įvairiais subjekto aspektais – kurkite specifiškesnius sub-klausimus
  4) ištirti atskiras sritis, kurios padėtų parengti galutinį atsakymą
  5) jei prasminga, sukurkite sub-klausimų, kurie padėtų vėlesniame etape generuoti naujus sub-klausimus, remiantis ankstesnių atsakymais

Svarbu: laikykitės RAG tinkamų formuluočių; venkite aiškinamųjų klausimų naudotojui.

Štai pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

{{history}}

NEĮTRAUKITE jokio kito teksto – tik sub-klausimų sąrašą! Pateikite po vieną eilutėje:

 <sub-klausimas>
 <sub-klausimas>
 <sub-klausimas>
 ...

Atsakymas:
""".strip()


INITIAL_DECOMPOSITION_PROMPT_QUESTIONS_AFTER_SEARCH = f"""
Sukurkite ne daugiau kaip 3 sub-klausimų sąrašą, kurių atsakymai padėtų atsakyti į pradinį klausimą.

Gairės – kaip aukščiau. Naudokite toliau pateiktus pavyzdinius dokumentus tik temai suvokti, \
o ne detaliems sub-klausimams konstruoti.

Pavyzdiniai dokumentai:
{SEPARATOR_LINE}
{{sample_doc_str}}
{SEPARATOR_LINE}

Pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

{{history}}

NEĮTRAUKITE jokio kito teksto – tik sub-klausimų sąrašą! Pateikite po vieną eilutėje:

 <sub-klausimas>
 <sub-klausimas>
 <sub-klausimas>
 ...

Atsakymas:
""".strip()


INITIAL_DECOMPOSITION_PROMPT_QUESTIONS_AFTER_SEARCH_ASSUMING_REFINEMENT = f"""
Sukurkite ne daugiau kaip 3 sub-klausimų sąrašą, kurių atsakymai padėtų atsakyti į pradinį klausimą.

Laikykitės RAG gairių; remkitės pavyzdiniais dokumentais tik konteksto suvokimui.

Pavyzdiniai dokumentai:
{SEPARATOR_LINE}
{{sample_doc_str}}
{SEPARATOR_LINE}

Pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

{{history}}

NEĮTRAUKITE jokio kito teksto – tik sub-klausimų sąrašą! Pateikite po vieną eilutėje:

 <sub-klausimas>
 <sub-klausimas>
 <sub-klausimas>
 ...

Atsakymas:
""".strip()


# Ieška
QUERY_REWRITING_PROMPT = f"""
Perkonstruokite pradinį klausimą į 2–3 trumpas ir tikslias paieškos užklausas \
dokumento saugyklai. Spręskite dviprasmybes ir padarykite užklausas specifiškesnes, \
kad sistema galėtų ieškoti plačiau.

Taip pat stenkitės, kad užklausos nesidubliuotų.

Pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

NEĮTRAUKITE jokio kito teksto – tik užklausų sąrašą! Pateikite po vieną eilutėje (be „Query 1:“ ir pan.):
<query 1>
<query 2>
...

Užklausos:
""".strip()


DOCUMENT_VERIFICATION_PROMPT = f"""
Nustatykite, ar toliau pateiktas dokumento tekstas turi duomenų ar informacijos, \
potencialiai aktualios klausimui. Nebūtina, kad būtų pilnai aktualus – pakanka, jei \
jame yra informacijos, kuri (galbūt kartu su kitais dokumentais) padėtų atsakyti.

Atsargiai: nenaudokite dokumento, jei nesate tikri, kad tekstas taikomas būtent klausimui aktualiems \
objektams ar subjektams. Pvz., knyga apie šachmatus gali turėti ilgą ištrauką apie psichologiją \
neminėdama šachmatų. Jei klausimas – apie futbolo psichologiją, toks dokumentas nėra tinkamas.

DOKUMENTO TEKSTAS:
{SEPARATOR_LINE}
{{document_content}}
{SEPARATOR_LINE}

Ar šis dokumentas naudingas/aktualus atsakyti į klausimą?

KLAUSIMAS:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Atsakykite tiksliai ir tik '{YES}' arba '{NO}'. NEĮTRAUKITE jokio kito teksto:

Atsakymas:
""".strip()


# Sub-klausimų atsakymų generavimas
SUB_QUESTION_RAG_PROMPT = f"""
Naudokite žemiau pateiktą kontekstą – ir tik jį – kad atsakytumėte į klausimą. \
(Atsakymas padeda atsakyti į platesnį klausimą – „motyvacija“ nurodyta žemiau.)

Užtikrinkite, kad išsaugote visą aktualią informaciją, ypač susijusią su galutiniu tikslu \
(kitą informaciją taip pat palikite).

{COMMON_RAG_RULES}

 - Nurodykite tik tai, ką tikrai galima patvirtinti iš pateikto konteksto! Neprasimanykite. \
Pvz., jei klausimas – apie konkurentų produktus, o kontekste minimi kelių įmonių produktai, \
NEPRIIMKITE prielaidų, kad jos konkurencinės, jei tai nepatvirtinta.

Labai svarbu cituoti eilutėse formatu [D1], [D2], [D3] ir t. t.! Jei cituojate kelis dokumentus \
vienu metu, naudokite [D1][D2], o ne [D1, D2]. Citata turi būti arti ją pagrindžiančios informacijos.

Štai dokumentų kontekstas:
{SEPARATOR_LINE}
{{context}}
{SEPARATOR_LINE}

Bendram supratimui – štai galutinis tikslas/motyvacija:
{SEPARATOR_LINE}
{{original_question}}
{SEPARATOR_LINE}

Ir štai klausimas, į kurį reikia atsakyti remiantis aukščiau pateiktu kontekstu (turint omenyje motyvaciją):
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Laikykite atsakymą trumpą ir konkretų, orientuotą į faktus ir duomenis.

Atsakymas:
""".strip()


SUB_ANSWER_CHECK_PROMPT = f"""
Nustatykite, ar pateiktas atsakymas adresuoja pateiktą klausimą. \
Nenaudokite vidinių žinių – vertinkite tik pagal tai, ar atsakymas iš esmės \
adresuoja visą arba bent dalį klausimo.

Štai klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Štai siūlomas atsakymas:
{SEPARATOR_LINE}
{{base_answer}}
{SEPARATOR_LINE}

Ar siūlomas atsakymas adresuoja klausimą? Atsakykite "{YES}" arba "{NO}".
""".strip()


# Pradinis atsakymas
INITIAL_ANSWER_PROMPT_W_SUB_QUESTIONS = f"""
{{persona_specification}}

Naudokite žemiau pateiktą informaciją – ir tik ją – kad atsakytumėte į pagrindinį klausimą.

Pateikiama informacija:
  1) keli atsakyti sub-klausimai – jie svarbūs struktūruojant mintis ir atsakymą
  2) keli dokumentai, laikomi aktualiais klausimui

{{history}}

Labai svarbu teisingai cituoti dokumentus eilutėse formatu [D1], [D2], [D3] ir t. t.! \
Citata turi būti arti ją pagrindžiančios informacijos. Jei yra kelios citatos tam pačiam faktui, \
naudokite, pvz., [D1][D3] arba [D2][D4]. Taip pat galite cituoti sub-klausimus, bet visada \
PAPILDYKITE dokumento citata (pvz., [D1][Q3]). NIEKADA necituokite tik sub-klausimų be dokumento.

{COMMON_RAG_RULES}

Vėlgi – užtikrinkite, kad atsakymas pagrįstas pateikta informacija! Pabrėžkite neapibrėžtumus ar prielaidas, jei jos esminės.

Kontextinė informacija:
{SEPARATOR_LINE_LONG}

*Atsakyti sub-klausimai:
{SEPARATOR_LINE}
{{answered_sub_questions}}
{SEPARATOR_LINE}

Aktualūs dokumentai:
{SEPARATOR_LINE}
{{relevant_docs}}
{SEPARATOR_LINE}

Klausimas, į kurį reikia atsakyti, remiantis aukščiau pateikta informacija:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Laikykite atsakymą trumpą ir konkretų, orientuotą į faktus ir duomenis.

Atsakymas:
""".strip()


INITIAL_ANSWER_PROMPT_WO_SUB_QUESTIONS = f"""
{{answered_sub_questions}}{{persona_specification}}

Naudokite žemiau pateiktą informaciją – ir tik ją – kad atsakytumėte į klausimą. \
Informacija sudaryta iš keleto dokumentų, laikomų aktualiais.

{{history}}

{COMMON_RAG_RULES}

Vėlgi – užtikrinkite, kad atsakymas pagrįstas pateikta informacija!

Labai svarbu teisingai cituoti dokumentus eilutėse formatu [D1], [D2], [D3] ir t. t.! \
Jei turite kelias citatas, naudokite, pvz., [D1][D3] arba [D2][D4]. Citatos – labai svarbios naudotojui.

Aktuali kontekstinė informacija:
{SEPARATOR_LINE}
{{relevant_docs}}
{SEPARATOR_LINE}

Klausimas, į kurį reikia atsakyti, remiantis kontekstu:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Laikykite atsakymą trumpą ir konkretų, orientuotą į faktus ir duomenis.

Atsakymas:
""".strip()


# TOBULINIMO FAZĖ – naujų sub-klausimų generavimas
REFINEMENT_QUESTION_DECOMPOSITION_PROMPT = f"""
Reikia atsakyti į pradinį klausimą. Pradinis atsakymas buvo pateiktas, bet jis nepakankamas. \
Taip pat turite kelis atsakytus sub-klausimus, kurie buvo naudoti pradiniam atsakymui. \
Kai kurie kiti sub-klausimai buvo siūlyti, bet neatsakyti. Taip pat pateikiami subjektai, ryšiai ir terminai – \
kad suprastumėte, kaip atrodo turimi duomenys.

Jūsų vaidmuo – sugeneruoti 2–4 naujus sub-klausimus, kurie padėtų atsakyti į pradinį klausimą, atsižvelgiant į:
1) pradinį klausimą
2) nepakankamą pradinį atsakymą
3) atsakytus sub-klausimus
4) siūlytus, bet neatsakytus sub-klausimus
5) iš konteksto išgautus subjektus, ryšius ir terminus

Sub-klausimai turi būti atsakomi gera RAG sistema, padėti šalinti dviprasmybes ar išskaidyti klausimą pagal subjektus, \
nekartojant jau bandytų klausimų.

Papildomos gairės:
- Sub-klausimai turi būti specifiniai ir suteikti turtingesnį kontekstą, spręsti dviprasmybes ar pradinio atsakymo trūkumus
- Kiekvienas sub-klausimas turi būti aktualus pradiniam klausimui
- Venkite palyginimų, dviprasmybių, vertinimų, agregacijų ir pan., jei tam reikia papildomo konteksto
- Sub-klausimai PRIVALO būti pilnai kontekstualizuoti ir vykdomi be pradinio klausimo
- Kiekvienam sub-klausimui pateikite paieškos terminą dokumentų paieškai
- Saugokite nuo jau siūlytų, bet neatsakytų – tai ženklas, kad su turimu kontekstu neatsakoma
- NEdarykite aiškinamųjų klausimų naudotojui

Pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}
{{history}}

Pradinis neoptimalus atsakymas:
{SEPARATOR_LINE}
{{base_answer}}
{SEPARATOR_LINE}

Atsakyti sub-klausimai:
{SEPARATOR_LINE}
{{answered_sub_questions}}
{SEPARATOR_LINE}

Siūlyti, bet neatsakyti sub-klausimai:
{SEPARATOR_LINE}
{{failed_sub_questions}}
{SEPARATOR_LINE}

Iš konteksto išgauti subjektai, ryšiai ir terminai:
{SEPARATOR_LINE}
{{entity_term_extraction_str}}
{SEPARATOR_LINE}

Pateikite gerų, pilnai kontekstualizuotų sub-klausimų sąrašą. Venkite dubliavimo su jau bandytais.
Sugeneruokite sąrašą po vieną eilutėje (ir atsakykite TIK su šiuo sąrašu!):

<sub-klausimas 1>
<sub-klausimas 2>
<sub-klausimas 3>
...""".strip()


REFINEMENT_QUESTION_DECOMPOSITION_PROMPT_W_INITIAL_SUBQUESTION_ANSWERS = f"""
Reikia atsakyti į pradinį klausimą. Pradinis atsakymas buvo pateiktas, bet jis nepakankamas. \
Taip pat turite atsakytus sub-klausimus (ir jų atsakymus), kurie naudoti pradiniam atsakymui. \
Kai kurie kiti sub-klausimai buvo siūlyti, bet neatsakyti. Taip pat pateikiami subjektai, ryšiai ir terminai.

Jūsų vaidmuo – sugeneruoti 2–4 naujus sub-klausimus, atsižvelgiant į:
1) pradinį klausimą
2) nepakankamą pradinį atsakymą
3) atsakytus sub-klausimus IR jų atsakymus
4) siūlytus, bet neatsakytus sub-klausimus (NEKARTOKITE jų!)
5) subjektus, ryšius ir terminus iš konteksto

Sub-klausimai turi būti atsakomi gera RAG sistema; naudokite ankstesnių atsakymų informaciją konkretesniems klausimams.

Papildomos gairės:
- Nauji sub-klausimai – specifiniai, suteikiantys kontekstą, sprendžiantys trūkumus
- Kiekvienas naujas sub-klausimas – aktualus pradiniam klausimui
- Venkite palyginimų, dviprasmybių, vertinimų, agregacijų be papildomo konteksto
- Privalo būti pilnai kontekstualizuoti
- Kiekvienam naujam sub-klausimui pateikite paieškos terminą
- Naudokite ankstesnių sub-klausimų atsakymus, kad būtumėte tikslesni
- Nebūkite perdėtai interpretuojantys; remkitės tik turimais faktais
- NEdarykite aiškinamųjų klausimų naudotojui

Pradinis klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}
{{history}}

Pradinis neoptimalus atsakymas:
{SEPARATOR_LINE}
{{base_answer}}
{SEPARATOR_LINE}

Atsakyti sub-klausimai ir atsakymai:
{SEPARATOR_LINE}
{{answered_subquestions_with_answers}}
{SEPARATOR_LINE}

Siūlyti, bet neatsakyti sub-klausimai:
{SEPARATOR_LINE}
{{failed_sub_questions}}
{SEPARATOR_LINE}

Iš konteksto išgauti subjektai, ryšiai ir terminai:
{SEPARATOR_LINE}
{{entity_term_extraction_str}}
{SEPARATOR_LINE}

Pateikite gerų, pilnai kontekstualizuotų sub-klausimų sąrašą. Venkite dubliavimo su jau bandytais.
Sugeneruokite sąrašą po vieną eilutėje (ir atsakykite TIK su šiuo sąrašu!):

<sub-klausimas 1>
<sub-klausimas 2>
<sub-klausimas 3>
...""".strip()


# Refined atsakymo generavimas
REFINED_ANSWER_PROMPT_W_SUB_QUESTIONS = f"""
{{persona_specification}}

Jūsų užduotis – pagerinti pateiktą atsakymą į klausimą, nes pradinis atsakymas buvo nepakankamas.

Naudokite žemiau pateiktą informaciją – ir tik ją – kad parašytumėte naują, patobulintą atsakymą.

Pateikiama informacija:
  1) pradinis atsakymas, kuris buvo nepakankamas
  2) atsakyti sub-klausimai – jie labai svarbūs ir turi padėti atsakyti į pagrindinį klausimą \
     (yra „initial“ ir „refined“ tipų; naudokite „refined“ ypač atnaujinimams)
  3) keli dokumentai, laikomi aktualiais – kontekstas daugiausia citatoms

Labai svarbu teisingai cituoti dokumentus eilutėse formatu [D1], [D2], [D3] ir t. t.! \
Jei cituojate kelis dokumentus kartu, naudokite [D1][D2], o ne [D1, D2]. Citata turi būti arti fakto.
Galite cituoti ir sub-klausimus kartu su dokumentu (pvz., [D1][Q3]), bet NIEKADA – tik sub-klausimą be dokumento.

{{history}}

{COMMON_RAG_RULES}

Užtikrinkite, kad atsakymas pagrįstas pateikta informacija. Laikykite jį glaustą; paminėkite esminius neapibrėžtumus.

Kontekstas:
{SEPARATOR_LINE_LONG}

*Pradinis nepakankamas atsakymas:
{SEPARATOR_LINE}
{{initial_answer}}
{SEPARATOR_LINE}

*Atsakyti sub-klausimai (ypač naujieji „refined“):
{{answered_sub_questions}}

Aktualūs dokumentai:
{SEPARATOR_LINE}
{{relevant_docs}}
{SEPARATOR_LINE}

Pagrindinis klausimas, į kurį reikia atsakyti:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Laikykite atsakymą trumpą ir konkretų, orientuotą į faktus ir duomenis.

Atsakymas:
""".strip()


REFINED_ANSWER_PROMPT_WO_SUB_QUESTIONS = f"""
{{answered_sub_questions}}{{persona_specification}}

Naudokite žemiau pateiktą informaciją – ir tik ją – kad atsakytumėte į klausimą.

Pateikiama informacija:
  1) pradinis atsakymas, kuris buvo nepakankamas
  2) keli dokumentai, laikomi aktualiais

Labai svarbu teisingai cituoti dokumentus eilutėse formatu [D1], [D2], [D3] ir t. t.! \
Jei cituojate kelis dokumentus kartu, naudokite [D1][D2]. Citata turi būti arti fakto.
NEIŠVARDINKITE visų citatų tik pačioje pabaigoje.

{{history}}

{COMMON_RAG_RULES}

Užtikrinkite, kad atsakymas pagrįstas pateikta informacija. Laikykite jį glaustą; paminėkite esminius neapibrėžtumus.

Kontekstas:
{SEPARATOR_LINE_LONG}

*Pradinis nepakankamas atsakymas:
{SEPARATOR_LINE}
{{initial_answer}}
{SEPARATOR_LINE}

Aktualūs dokumentai:
{SEPARATOR_LINE}
{{relevant_docs}}
{SEPARATOR_LINE}

Pagrindinis klausimas, į kurį reikia atsakyti:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Laikykite atsakymą trumpą ir konkretų, orientuotą į faktus ir duomenis.

Atsakymas:
""".strip()


REFINED_ANSWER_VALIDATION_PROMPT = f"""
{{persona_specification}}

Jūsų užduotis – patikrinti, ar pateiktas atsakymas teisingas, tikslus ir pagrįstas faktais,
kurie bus pateikti.

Pateikiama informacija:
  1) klausimas, į kurį reikėjo atsakyti
  2) siūlomas atsakymas, kurio tikslumą turite įvertinti
  3) (galimai) trumpa pokalbio istorijos santrauka – kontekstui (istorija NĖRA faktai)
  4) keli atsakyti sub-klausimai – jų atsakymai laikomi faktais šiems tikslams
  5) keli aktualūs dokumentai, kuriais remiantis tikrinsite atsakymo teiginius

SVARBŪS PRINCIPAI:
 - Įvertinkite, ar atsakyme esantys teiginiai yra teisingi ir tikslūs, remdamiesi sub-klausimų atsakymais ir dokumentais.
 - Ypač ieškokite:
    * svarbių teiginių, nepagrįstų sub-klausimų atsakymais ar dokumentais
    * priskyrimų ir grupavimų be pagrindo (pvz., A yra B konkurentas) – be aiškių įrodymų
 - Įvertinkite citatas – ar jos tinkamos pateiktiems teiginiams.
 - Ar elementai grupuojami po antrašte, kai ne visi atitinka kategoriją?
 - Ar atsakymas pilnai adresuoja klausimą ir yra specifinis?
 - Patikrinkite skaičiavimus; jei klaidingi – atsakymas nepatikimas.

Štai informacija:
{SEPARATOR_LINE_LONG}

KLAUSIMAS:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

SIŪLOMAS ATSAKYMAS:
{SEPARATOR_LINE}
{{proposed_answer}}
{SEPARATOR_LINE}

Papildomas kontekstas:
{SEPARATOR_LINE_LONG}

{{history}}

Sub-klausimai ir jų atsakymai (laikomi faktais):
{SEPARATOR_LINE}
{{answered_sub_questions}}
{SEPARATOR_LINE}

Aktualūs dokumentai:
{SEPARATOR_LINE}
{{relevant_docs}}
{SEPARATOR_LINE}

Pagalvokite nuosekliai. Suformatuokite atsakymą kaip eilutę šiuo formatu:

Analysis: <trumpa jūsų analizė pagal aukščiau pateiktus principus>
Comments: <trumpos pastabos naudotojui apie tikslumą ir specifiškumą>
{AGENT_ANSWER_SEPARATOR} <atsakykite tik yes arba no, ar atsakymu galima pasitikėti. Remkitės analize; naudokite tik 'yes' arba 'no'>
""".strip()


INITIAL_REFINED_ANSWER_COMPARISON_PROMPT = f"""
Duotam klausimui palyginkite pradinį atsakymą ir patobulintą atsakymą ir nustatykite, \
ar patobulintas atsakymas yra İŠ ESMĖS geresnis (ne tik šiek tiek geresnis). Geresnis gali reikšti:
 - daugiau informacijos
 - išsamesnė informacija
 - glaustesnė informacija
 - geresnė struktūra
 - daugiau detalių
 - nauji punktai
 - žymiai daugiau dokumentų citatų ([D1], [D2], [D3], ...)

Įsijauskite į naudotoją – ar patobulintas atsakymas tikrai teikia naujų įžvalgų ir yra geresnis?

Klausimas:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Pradinis atsakymas:
{SEPARATOR_LINE}
{{initial_answer}}
{SEPARATOR_LINE}

Patobulintas atsakymas:
{SEPARATOR_LINE}
{{refined_answer}}
{SEPARATOR_LINE}

Atsakykite paprastai: "{YES}" arba "{NO}"
""".strip()
