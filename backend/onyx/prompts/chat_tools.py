DANSWER_TOOL_NAME = "Current Search"
DANSWER_TOOL_DESCRIPTION = (
    "Paieškos priemonė, galinti rasti informaciją bet kuria tema, įskaitant naujausias ir nuosavybines žinias."
)


TOOL_TEMPLATE = """
TOOLS
------
Galite naudoti įrankius informacijai paieškoti, kuri gali padėti atsakyti į vartotojo
pradinį klausimą. Galimi įrankiai:

{tool_overviews}

RESPONSE FORMAT INSTRUCTIONS
----------------------------
Atsakydami pateikite vieną iš dviejų formatų:

**1 parinktis:**
Naudokite, jei norite pasitelkti įrankį. Markdown kodo ištrauka pagal schemą:

```json
{
    "action": string, \\ Veiksmas. {tool_names}
    "action_input": string \\ Veiksmo įvestis
}
```

**2 parinktis:**
Naudokite, jei norite atsakyti tiesiogiai. Markdown kodo ištrauka pagal schemą:

```json
{
    "action": "Final Answer",
    "action_input": string \\ Turinys, kurį norite grąžinti vartotojui
}
```
"""


TOOL_LESS_PROMPT = """
Atsakykite markdown kodo ištrauka pagal šią schemą:

```json
{
    "action": "Final Answer",
    "action_input": string \\ Turinys, kurį norite grąžinti vartotojui
}
```
"""


USER_INPUT = """
USER'S INPUT
--------------------
Štai vartotojo įvestis \
(atsakykite markdown kodo ištrauka su vienu json veiksmu ir NIEKUO daugiau):

{user_input}
"""


TOOL_FOLLOWUP = """
TOOL RESPONSE:
---------------------
{tool_output}

USER'S INPUT
--------------------
Gerai, koks atsakymas į mano paskutinį komentarą? Jei naudojate informaciją iš įrankių,
aiškiai tai paminėkite, neminėdami įrankių pavadinimų – pamiršau visus TOOL RESPONSES!
Jei įrankio atsakymas nenaudingas, visiškai jį ignoruokite.
{optional_reminder}{hint}
SVARBU! PRIVALOTE atsakyti markdown kodo ištrauka su vienu json veiksmu ir NIEKUO daugiau.
"""


TOOL_LESS_FOLLOWUP = """
Remkitės toliau pateiktais dokumentais atsakydami į galutinę užklausą. Ignoruokite bet kuriuos
neaktualius dokumentus.

KONTEKSTO DOKUMENTAI:
---------------------
{context_str}

GALUTINĖ UŽKLAUSA:
--------------------
{user_query}

{hint_text}
"""
