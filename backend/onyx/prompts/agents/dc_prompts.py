SEPARATOR_LINE = "-------"
SEPARATOR_LINE_LONG = "---------------"
NO_EXTRACTION = "No extraction of knowledge graph objects was feasable."
YES = "yes"
NO = "no"
DC_OBJECT_SEPARATOR = ";"


DC_OBJECT_NO_BASE_DATA_EXTRACTION_PROMPT = f"""
Jūs esate ekspertas, ieškantis susijusių objektų / objektų specifikacijų to paties tipo
keliose dokumentuose. Šiuo atveju jus domina: {{objects_of_interest}}.
Peržiūrėkite dokumentus – bet kokia tvarka! – ir išskirkite kiekvieną objektą, kurį randate.
{SEPARATOR_LINE}
Štai dokumentai, kuriuos turite peržiūrėti:
--
{{document_text}}
{SEPARATOR_LINE}
Tai – užduoties instrukcijos, kurios padės surasti norimus objektus:
{SEPARATOR_LINE}
{{task}}
{SEPARATOR_LINE}
Štai klausimas, suteikiantis papildomo konteksto užduočiai:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}
Atsakykite šiuo formatu:
REASONING: <jūsų pagrindimas klasifikacijai> - OBJECTS: <objektai – tik jų pavadinimai – rikiuojami „;“>
""".strip()


DC_OBJECT_WITH_BASE_DATA_EXTRACTION_PROMPT = f"""
Jūs esate ekspertas, ieškantis susijusių objektų / objektų specifikacijų to paties tipo
keliose dokumentuose. Šiuo atveju jus domina: {{objects_of_interest}}.
Peržiūrėkite pateiktus duomenis – bet kokia tvarka! – ir išskirkite kiekvieną objektą, kurį randate.
{SEPARATOR_LINE}
Štai pradiniai naudotojo duomenys:
--
{{base_data}}
{SEPARATOR_LINE}
Tai – užduoties instrukcijos, kurios padės surasti norimus objektus:
{SEPARATOR_LINE}
{{task}}
{SEPARATOR_LINE}
Štai užklausa, suteikianti papildomo konteksto:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}
Atsakykite šiuo formatu:
REASONING: <jūsų pagrindimas klasifikacijai> - OBJECTS: <objektai – tik jų pavadinimai – rikiuojami „;“>
""".strip()


DC_OBJECT_SOURCE_RESEARCH_PROMPT = f"""
Šiandien yra {{today}}. Jūs esate ekspertas, išgaunantis susistemintą informaciją
iš kelių dokumentų apie VIENĄ objektą (įsitikinkite, kad tai tikrai tas pats objektas!).
Peržiūrėkite dokumentus – bet kokia tvarka! – ir išskirkite užduotyje nurodytą informaciją:
{SEPARATOR_LINE}
{{task}}
{SEPARATOR_LINE}

Štai naudotojo klausimas, suteikiantis papildomo konteksto:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Štai dokumentai, kuriuos turite peržiūrėti:
--
{{document_text}}
{SEPARATOR_LINE}
Pastaba: cituokite šaltinius tekste, kai pateikiate rezultatus! Naudokite formatą [1] ir t. t. Numerį
nustatykite pagal konteksto dokumentus. Tai labai svarbu!
Atsakykite šiuo formatu:
REASONING:
 -- <jūsų svarstymai klasifikacijai>
RESEARCH RESULTS:
{{format}}
""".strip()


DC_OBJECT_CONSOLIDATION_PROMPT = f"""
Jūs esate naudingas asistentas, konsoliduojantis informaciją apie konkretų objektą
iš kelių šaltinių.
Objektas:
{SEPARATOR_LINE}
{{object}}
{SEPARATOR_LINE}
ir informacija:
{SEPARATOR_LINE}
{{information}}
{SEPARATOR_LINE}
Štai naudotojo klausimas, suteikiantis papildomo konteksto:
{SEPARATOR_LINE}
{{question}}
{SEPARATOR_LINE}

Sujunkite informaciją į vieną, glaustą atsakymą. Konsoliduota informacija apie objektą
turi atitikti šį formatą:
{SEPARATOR_LINE}
{{format}}
{SEPARATOR_LINE}
Bendra struktūra:
{SEPARATOR_LINE}
REASONING: <jūsų pagrindimas konsolidavimui>
INFORMATION:
<konsoliduota informacija tinkamu formatu>
"""


DC_FORMATTING_NO_BASE_DATA_PROMPT = f"""
Jūs esate teksto formatavimo ekspertas. Jūsų užduotis – pateiktą tekstą 100 procentų tikslumu
perkelti į naują formatą.
Štai tekstas, kurį turite suformatuoti:
{SEPARATOR_LINE}
{{text}}
{SEPARATOR_LINE}
Štai formatas, kurį turite naudoti:
{SEPARATOR_LINE}
{{format}}
{SEPARATOR_LINE}
Pateikite atsakymą tiesiogiai su suformatuotu tekstu. (Išvestis turi būti ne kodas, o tekstas.)
"""


DC_FORMATTING_WITH_BASE_DATA_PROMPT = f"""
Jūs esate teksto formatavimo ekspertas. Jūsų užduotis – pateiktą tekstą ir naudotojo pradinius duomenis
100 procentų tikslumu perkelti į naują formatą. Pradiniai duomenys gali apimti svarbius ryšius,
kurie būtini formatavimui.
Štai pradiniai naudotojo duomenys:
{SEPARATOR_LINE}
{{base_data}}
{SEPARATOR_LINE}
Štai tekstas, kurį turite sujungti (ir suformatuoti) su pradiniais duomenimis, laikydamiesi
formatavimo instrukcijų vėliau:
{SEPARATOR_LINE}
{{text}}
{SEPARATOR_LINE}
O čia – formatavimo instrukcijos:
{SEPARATOR_LINE}
{{format}}
{SEPARATOR_LINE}
Pateikite atsakymą tiesiogiai su suformatuotu tekstu. (Išvestis turi būti ne kodas, o tekstas.)
"""
