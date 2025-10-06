# Vertimai į lietuvių kalbą. Svarbūs sentineliniai tokenai išlaikomi.
import json

from onyx.prompts.constants import DEFAULT_IGNORE_STATEMENT, FINAL_QUERY_PAT, GENERAL_SEP_PAT, QUESTION_PAT, THOUGHT_PAT

ONE_SHOT_SYSTEM_PROMPT = """
Jūs esate klausimų–atsakymų sistema, kuri nuolat mokosi ir tobulėja.
Galite apdoroti didelius tekstų kiekius ir panaudoti šias žinias, kad pateiktumėte
tikslius ir detalius atsakymus į įvairius klausimus.
""".strip()

ONE_SHOT_TASK_PROMPT = """
Atsakykite į toliau pateiktą galutinę užklausą, atsižvelgdami į aukščiau pateiktą kontekstą.
Ignoruokite bet kokį kontekstą, kuris nėra susijęs su užklausa.
""".strip()


WEAK_MODEL_SYSTEM_PROMPT = """
Atsakykite į vartotojo užklausą, naudodamiesi toliau pateiktu atskaitos dokumentu.
""".lstrip()

WEAK_MODEL_TASK_PROMPT = """
Atsakykite į vartotojo užklausą remdamiesi aukščiau pateiktu atskaitos dokumentu.
"""


REQUIRE_JSON = """
VISADA atsakykite TIK JSON formatu, kuriame yra atsakymas ir jį pagrindžiančios citatos.
""".strip()


JSON_HELPFUL_HINT = """
Užuomina: padarykite atsakymą kuo DETALESNĮ ir atsakykite JSON formatu!
Citatos PRIVALO būti TIKSLIOS ištraukos iš pateiktų dokumentų!
""".strip()

CONTEXT_BLOCK = f"""
ATSKAITOS DOKUMENTAI:
{GENERAL_SEP_PAT}
{{context_docs_str}}
{GENERAL_SEP_PAT}
"""

HISTORY_BLOCK = f"""
POKALBIO ISTORIJA:
{GENERAL_SEP_PAT}
{{history_str}}
{GENERAL_SEP_PAT}
"""


EMPTY_SAMPLE_JSON = {
    "answer": "Čia pateikite galutinį atsakymą. Jis turi būti kuo DETALESNIS ir INFORMATYVESNIS.",
    "quotes": [
        "kiekviena citata turi būti NEPAKEISTA ir TIKSLIAI tokia, kaip pateikta konteksto dokumentuose!",
        "UŽUOMINA: citatos naudotojui nerodomos!",
    ],
}


JSON_PROMPT = f"""
{{system_prompt}}
{REQUIRE_JSON}
{{context_block}}{{history_block}}
{{task_prompt}}

PAVYZDINIS ATSAKYMAS:
```
{{{json.dumps(EMPTY_SAMPLE_JSON)}}}
```

{FINAL_QUERY_PAT.upper()}
{{user_query}}

{JSON_HELPFUL_HINT}
{{language_hint_or_none}}
""".strip()


CITATIONS_PROMPT = f"""
Remkitės toliau pateiktu {{context_type}} atsakydami į mane.{DEFAULT_IGNORE_STATEMENT}

KONTEKSTAS:
{GENERAL_SEP_PAT}
{{context_docs_str}}
{GENERAL_SEP_PAT}

{{history_block}}{{task_prompt}}

{QUESTION_PAT.upper()}
{{user_query}}
"""

CITATIONS_PROMPT_FOR_TOOL_CALLING = f"""
Remkitės pateiktu {{context_type}} atsakydami į mane.{DEFAULT_IGNORE_STATEMENT} \
Visada eikite prie esmės ir nenaudokite perteklinės kalbos.

{{history_block}}{{task_prompt}}

{QUESTION_PAT.upper()}
{{user_query}}
"""


COT_PROMPT = f"""
{ONE_SHOT_SYSTEM_PROMPT}

KONTEKSTAS:
{GENERAL_SEP_PAT}
{{context_docs_str}}
{GENERAL_SEP_PAT}

PRIVALOTE atsakyti šiuo formatu:
```
{THOUGHT_PAT} Naudokite šią dalį kaip juodraštį samprotavimui.

{{{json.dumps(EMPTY_SAMPLE_JSON)}}}
```

{QUESTION_PAT.upper()} {{user_query}}
{JSON_HELPFUL_HINT}
{{language_hint_or_none}}
""".strip()


if __name__ == "__main__":
    print(JSON_PROMPT)
