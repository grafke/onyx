from onyx.prompts.constants import ANSWERABLE_PAT, GENERAL_SEP_PAT, QUESTION_PAT, THOUGHT_PAT

ANSWERABLE_PROMPT = f"""
Jūs esate pagalbinis įrankis nustatyti, ar užklausą galima atsakyti naudojant
retrieval augmented generation (RAG).
Pagrindinė sistema bandys atsakyti remdamasi TIK 5 aktualiausiais dokumentais iš paieškos.
Šaltiniai apima tiek naujausią, tiek nuosavybinę komandos informaciją.
Jei minimi vardiniai ar nežinomi subjektai, laikykite, kad paieška ras atitinkamas ir nuoseklias žinias.
Sistema nepritaikyta kodo rašymui.
Sistema nepritaikyta darbui su struktūriniais duomenimis per užklausų kalbas, pvz., SQL.
Jei klausimas gali būti atsakytas be kodo ar užklausų kalbų, tarkite, kad atsakyti galima.
Nustatykite, ar sistema turėtų bandyti atsakyti.
"ANSWERABLE" privalo būti tiksliai "True" arba "False".

{GENERAL_SEP_PAT}

{QUESTION_PAT.upper()} Apie ką yra šis Slack kanalas?
```
{THOUGHT_PAT.upper()} Pirmiausia sistema turi nustatyti, apie kurį Slack kanalą kalbama.
Gavus 5 dokumentus, susijusius su Slack kanalo turiniu, neįmanoma nustatyti, apie kurį
Slack kanalą kalbama.
{ANSWERABLE_PAT.upper()} False
```

{QUESTION_PAT.upper()} Onyx nepasiekiamas.
```
{THOUGHT_PAT.upper()} Sistema ieško dokumentų, susijusių su Onyx nepasiekiamumu.
Darome prielaidą, kad paieškoje yra situacijų ir sprendimų, todėl užklausa gali būti atsakoma.
{ANSWERABLE_PAT.upper()} True
```

{QUESTION_PAT.upper()} Kiek turime klientų
```
{THOUGHT_PAT.upper()} Jei gautuose dokumentuose yra naujausia informacija apie klientų skaičių,
užklausa gali būti atsakoma. Jei informacija tik SQL duomenų bazėje, sistema SQL nevykdo ir
atsakymo neras.
{ANSWERABLE_PAT.upper()} True
```

{QUESTION_PAT.upper()} {{user_query}}
""".strip()


if __name__ == "__main__":
    print(ANSWERABLE_PROMPT)
