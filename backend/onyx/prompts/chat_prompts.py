from pydantic import BaseModel

from onyx.prompts.constants import GENERAL_SEP_PAT, QUESTION_PAT

REQUIRE_CITATION_STATEMENT = """
Cituokite atitinkamas ištraukas EILUTĖJE, naudodami formatą [1], [2], [3] ir t. t.,
kad nurodytumėte dokumento numerį. NESUTEIKITE jokių nuorodų po citatomis.
Venkite dvigubų skliaustų kaip [[1]]. Norėdami cituoti kelis dokumentus,
naudokite [1], [2] vietoje [1, 2]. Stenkitės cituoti tekste, o ne tik gale.
""".rstrip()

NO_CITATION_STATEMENT = """
Neteikite jokių citatų, net jei jos yra pavyzdžiuose pokalbių istorijoje.
""".rstrip()

CITATION_REMINDER = """
Nepamirškite pateikti eilučių citatų formatu [1], [2], [3] ir t. t.
"""

PROJECT_INSTRUCTIONS_SEPARATOR = (
    "\n\n[[NAUDOTOJO PATEIKTI INSTRUKCIJOS — leidžiamos perrašyti numatytąsias prompt'o nuorodas, "
    "bet tik stilių, formatavimo ir konteksto nuorodoms]]\n"
)

ADDITIONAL_INFO = "\n\nPapildoma informacija:\n\t- {datetime_info}."

CODE_BLOCK_MARKDOWN = "Formatavimas vėl įjungtas. "


CHAT_USER_PROMPT = f"""
Remkitės toliau pateiktais konteksto dokumentais atsakydami į mane.{{optional_ignore_statement}}
KONTEKSTAS:
{GENERAL_SEP_PAT}
{{context_docs_str}}
{GENERAL_SEP_PAT}

{{task_prompt}}

{QUESTION_PAT.upper()}
{{user_query}}
""".strip()


CHAT_USER_CONTEXT_FREE_PROMPT = f"""
{{history_block}}{{task_prompt}}

{QUESTION_PAT.upper()}
{{user_query}}
""".strip()


SKIP_SEARCH = "Skip Search"
YES_SEARCH = "Yes Search"


class AggressiveSearchTemplateParams(BaseModel):
    chat_history: str
    final_query: str


def build_aggressive_search_template(params: AggressiveSearchTemplateParams) -> str:
    return f"""
Atsižvelgiant į pokalbio istoriją ir papildomą užklausą, nustatykite,
ar sistemai reikėtų kviesti išorinę paieškos priemonę, kad geriau atsakytų į naujausią įvestį.
Numatytasis atsakymas yra {YES_SEARCH}.

Atsakykite „{SKIP_SEARCH}“, jei:
- Pokalbio istorijoje yra pakankamai informacijos PILNAI ir TIKSLIAI atsakyti į užklausą IR
papildoma informacija būtų menkos vertės.
- Uždavinys nereikalauja papildomos informacijos.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{params.chat_history}
{GENERAL_SEP_PAT}

Jei abejojate, atsakykite {YES_SEARCH}.
Atsakykite TIKSLIAI IR TIK „{YES_SEARCH}“ arba „{SKIP_SEARCH}“

Papildoma užklausa:
{params.final_query}
""".strip()


AGGRESSIVE_SEARCH_TEMPLATE_LLAMA2 = f"""
Jūs esate kritinės sistemos ekspertas. Atsižvelgdami į pokalbio istoriją ir papildomą užklausą,
nustatykite, ar sistemai reikėtų kviesti išorinę paieškos priemonę, kad geriau atsakytų į naujausią įvestį.

Numatytasis atsakymas yra {YES_SEARCH}.
Jei bent šiek tiek abejojate, atsakykite {YES_SEARCH}.

Atsakykite „{SKIP_SEARCH}“, jei bet kuri iš sąlygų teisinga:
- Pokalbio istorijoje yra pakankamai informacijos PILNAI ir TIKSLIAI atsakyti į užklausą.
- Uždavinys nereikalauja papildomos informacijos.
- Visiškai aiški tema ir nėra dviprasmiškumo.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Atsakykite TIKSLIAI IR TIK „{YES_SEARCH}“ arba „{SKIP_SEARCH}“

Papildoma užklausa:
{{final_query}}
""".strip()


REQUIRE_SEARCH_SINGLE_MSG = f"""
Atsižvelgiant į pokalbio istoriją ir papildomą užklausą, nustatykite,
ar sistemai reikėtų kviesti išorinę paieškos priemonę, kad geriau atsakytų į naujausią įvestį.

Atsakykite „{YES_SEARCH}“, jei:
- Konkretūs duomenys ar papildomos žinios gali pagerinti atsakymą.
- Yra naujų ar neaiškių terminų, arba neaišku, į ką vartotojas remiasi.
- Gali būti naudinga perskaityti anksčiau minėtą dokumentą.

Atsakykite „{SKIP_SEARCH}“, jei:
- Pokalbio istorijoje pakanka informacijos PILNAI ir TIKSLIAI atsakyti į užklausą
ir papildoma informacija būtų menkos vertės.
- Uždavinys nereikalauja papildomos informacijos.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Net jei tema jau paliesta, jei detalesnė informacija būtų naudinga, atsakykite „{YES_SEARCH}“.
Jei abejojate, atsakykite „{YES_SEARCH}“.

Atsakykite TIKSLIAI IR TIK „{YES_SEARCH}“ arba „{SKIP_SEARCH}“

Papildoma užklausa:
{{final_query}}
""".strip()


HISTORY_QUERY_REPHRASE = f"""
Atsižvelgiant į toliau pateiktą pokalbį ir papildomą įvestį, perfrazuokite papildymą į TRUMPĄ,
savarankišką užklausą (kuri apima reikšmingą kontekstą), skirtą vektorių paieškai.
SVARBU: PARUOŠKITE KIEK ĮMANOMA TRUMPEAUŽKLAUSĄ – naudokite raktinius žodžius.
Jei aiški temos kaita, ignoruokite ankstesnius pranešimus.
Pašalinkite nereikšmingą informaciją paieškai.
Jei įvestis yra klaida ar kodo ištrauka, grąžinkite ją NEPAKEISTĄ.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Papildoma įvestis: {{question}}
Savarankiška užklausa (atsakykite tik trumpa užklausa):
""".strip()


INTERNET_SEARCH_QUERY_REPHRASE = f"""
Atsižvelgiant į toliau pateiktą pokalbį ir papildomą įvestį, perfrazuokite ją į TRUMPĄ,
savarankišką užklausą, tinkamą interneto paieškos varikliui.
SVARBU: jei konkreti užklausa gali riboti rezultatus, palaikykite ją platesnę;
jei pernelyg plati duos per daug rezultatų, padarykite detalesnę.
Jei aiški temos kaita, užklausa turi atitikti naują temą.
Pašalinkite nereikšmingą informaciją internetinei paieškai.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Papildoma įvestis: {{question}}
Interneto paieškos užklausa (atsakykite detalia ir konkrečia užklausa):
""".strip()


# Retired prompts kept aligned with English for structure, not used in main flow
NO_SEARCH = "No Search"
REQUIRE_SEARCH_SYSTEM_MSG = f"""
Jūs esate didelis kalbos modelis, kurio vienintelis darbas – nustatyti, ar sistema turėtų kviesti
išorinę paieškos priemonę, kad galėtų atsakyti į paskutinę vartotojo žinutę.

Atsakykite „{{NO_SEARCH}}“, jei:
- pokalbio istorijoje pakanka informacijos pilnai atsakyti į užklausą
- modelio žinios pakankamos pilnam atsakymui
- užklausa nereikalauja specifinių žinių

Atsakykite „{YES_SEARCH}“, jei:
- papildomos žinios gali pagerinti atsakymą
- neaišku, į ką remiasi vartotojas

Atsakykite TIKSLIAI IR TIK „{YES_SEARCH}“ arba „{{NO_SEARCH}}“
"""


REQUIRE_SEARCH_HINT = f"""
Užuomina: atsakykite TIKSLIAI {YES_SEARCH} arba {{NO_SEARCH}}
""".strip()


QUERY_REPHRASE_SYSTEM_MSG = """
Atsižvelgiant į pokalbį (tarp Žmogaus ir Asistento) ir galutinę Žmogaus žinutę,
perrašykite paskutinę žinutę į glaustą savarankišką užklausą, kuri apimtų reikalingą
kontekstą iš ankstesnių žinučių. Užklausa bus naudojama semantinei paieškai.
""".strip()


QUERY_REPHRASE_USER_MSG = """
Padėkite perrašyti šią galutinę žinutę į savarankišką užklausą, kuri, jei reikia,
atsižvelgtų į ankstesnes pokalbio žinutes. Ši užklausa naudojama semantinei paieškai
norint gauti dokumentus. PRIVALOTE grąžinti TIK perrašytą užklausą ir NIEKO DAUGIAU.
SVARBU: paieškos sistema neturi prieigos prie pokalbio istorijos!

Užklausa:
{final_query}
""".strip()


CHAT_NAMING = f"""
Atsižvelgiant į žemiau pateiktą pokalbį, pateikite TRUMPĄ pokalbio pavadinimą.{{language_hint_or_empty}}
SVARBU: STENKITES NEVIRŠYTI 5 ŽODŽIŲ, BŪKITE KIEK ĮMANOMA KONKRETESNI.
Pavadinimas turi atspindėti pagrindinius raktažodžius, perteikiančius temą.

Pokalbio istorija:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Remiantis aukščiau pateikta informacija, koks trumpas pavadinimas geriausiai perteikia pokalbio temą?
""".strip()


# Pastabos: žemiau esančių raginimų atskyrimas padeda efektyvumui ir saugo nuo {} formatavimo kolizijų
CONTEXTUAL_RAG_PROMPT1 = """<document>
{document}
</document>
Štai ištrauka, kurią norime įterpti į viso dokumento kontekstą"""

CONTEXTUAL_RAG_PROMPT2 = """<chunk>
{chunk}
</chunk>
Pateikite trumpą, glaustą kontekstą, padedantį įterpti šią ištrauką į viso dokumento vaizdą
paieškos (retrieval) tikslumui pagerinti. Atsakykite tik glaustu kontekstu ir niekuo daugiau. """

CONTEXTUAL_RAG_TOKEN_ESTIMATE = 64  # 19 + 45

DOCUMENT_SUMMARY_PROMPT = """<document>
{document}
</document>
Pateikite trumpą, glaustą viso dokumento santrauką. Atsakykite tik glausta santrauka ir niekuo daugiau. """

DOCUMENT_SUMMARY_TOKEN_ESTIMATE = 29


QUERY_SEMANTIC_EXPANSION_WITHOUT_HISTORY_PROMPT = """
Perfrazuokite toliau pateiktą naudotojo klausimą/užklausą į semantinę užklausą, tinkamą paieškos varikliui.

Pastaba:
 - nekeiskite klausimo prasmės! Jei užklausa yra instrukcija, palikite ją instrukcija!

Štai naudotojo klausimas/užklausa:
{question}

Atsakykite TIKSLIAI IR TIK viena perfrazuota užklausa.

Perfrazuota užklausa paieškos varikliui:
""".strip()


QUERY_SEMANTIC_EXPANSION_WITH_HISTORY_PROMPT = """
Turėdami ankstesnę žinučių istoriją, perfrazuokite tolesnį klausimą/užklausą į semantinę užklausą,
kuri tiktų PAIEŠKOS VARIKLIUI. Naudokite tik tiek istorijos informacijos, kiek būtina suteikti
reikalingą kontekstą, kad gauta užklausa būtų savarankiška.

Pastaba:
 - nekeiskite klausimo prasmės! Jei užklausa yra instrukcija, palikite ją instrukcija!

Aktuali žinučių istorija:
{history}

Naudotojo klausimas:
{question}

Atsakykite TIKSLIAI IR TIK viena perfrazuota užklausa.

Perfrazuota užklausa paieškos varikliui:
""".strip()


QUERY_KEYWORD_EXPANSION_WITHOUT_HISTORY_PROMPT = """
Perfrazuokite toliau pateiktą naudotojo klausimą į GRYNŲ RAKTINIŲ ŽODŽIŲ užklausą, tinkančią paieškos varikliui.
SVARBU: perfrazuota užklausa PRIVALO NAUDOTI TIK EGZISTUOJANČIUS RAKTINIUS ŽODŽIUS iš pradinės užklausos
(išimtis: kritinius veiksmažodžius galima paversti daiktavardžiais)!
Paprastai raktiniai žodžiai – daiktavardžiai ar būdvardžiai, tad dažnai veiksmažodžius reikės atmesti.
JEI IR TIK JEI manote, kad veiksmažodis būtinas dokumentui RASTI, paverskite jį daiktavardžiu.
Tai turėtų būti reta. Veiksmažodžius kaip „rasti, apibendrinti, aprašyti“ pašalinkite.

Štai naudotojo klausimas:
{question}

Atsakykite TIKSLIAI IR TIK viena perfrazuota raktinių žodžių užklausa.

Perfrazuota raktinių žodžių užklausa paieškos varikliui:
""".strip()


QUERY_KEYWORD_EXPANSION_WITH_HISTORY_PROMPT = """
Turėdami ankstesnę žinučių istoriją, perfrazuokite tolesnį klausimą/užklausą į RAKTINIŲ ŽODŽIŲ užklausą,
tinkančią PAIEŠKOS VARIKLIUI. Naudokite tik tiek istorijos informacijos, kiek būtina suteikti
reikalingą kontekstą, kad gauta užklausa būtų savarankiška.

Aktuali žinučių istorija:
{history}

Naudotojo klausimas:
{question}

Atsakykite TIKSLIAI IR TIK viena perfrazuota užklausa.

Perfrazuota užklausa paieškos varikliui:
""".strip()
