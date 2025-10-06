from onyx.configs.app_configs import CUSTOM_ANSWER_VALIDITY_CONDITIONS
from onyx.prompts.constants import ANSWER_PAT, QUESTION_PAT

ANSWER_VALIDITY_CONDITIONS = (
    """
1. Užklausa prašo informacijos, kuri skiriasi priklausomai nuo asmens ar yra subjektyvi. Jei nėra
visuotinio teisingo atsakymo, modelis neturėtų atsakyti, todėl bet koks atsakymas yra neteisingas.
2. Atsakymas adresuoja susijusią, bet kitokią užklausą. Kad būtų naudingas, modelis gali pateikti
su užklausa susijusią informaciją, tačiau jei ji neatitinka prašymo, toks atsakymas neteisingas.
3. Atsakymas yra tik „Nežinau“ arba „Per mažai informacijos“ be reikšmingos papildomos
naudingos informacijos. Paaiškinimas, kodėl nežino ar negali atsakyti, nėra pakankamas.
"""
    if not CUSTOM_ANSWER_VALIDITY_CONDITIONS
    else "\n".join([f"{indice + 1}. {condition}" for indice, condition in enumerate(CUSTOM_ANSWER_VALIDITY_CONDITIONS)])
)


ANSWER_FORMAT = (
    """
1. True or False
2. True or False
3. True or False
"""
    if not CUSTOM_ANSWER_VALIDITY_CONDITIONS
    else "\n".join([f"{indice + 1}. True or False" for indice, _ in enumerate(CUSTOM_ANSWER_VALIDITY_CONDITIONS)])
)


ANSWER_VALIDITY_PROMPT = f"""
Jūs esate asistentas, padedantis identifikuoti neteisingas užklausos/atsakymo poras iš didelio kalbos modelio.
Pora yra neteisinga, jei bent viena iš sąlygų yra teisinga:
{ANSWER_VALIDITY_CONDITIONS}

{QUESTION_PAT} {{user_query}}
{ANSWER_PAT} {{llm_answer}}

------------------------
PRIVALOTE atsakyti TIKSLIAI šiuo formatu:
```
{ANSWER_FORMAT}
Final Answer: Valid or Invalid
```

Užuomina: prisiminkite, jei BENT viena sąlyga teisinga, atsakymas – Invalid.
""".strip()


if __name__ == "__main__":
    print(ANSWER_VALIDITY_PROMPT)
