from onyx.prompts.constants import SOURCES_KEY

# Mažesni papildomi raginimai – laiko filtro nustatymui (atitinka time_filter.py naudojimą)
TIME_FILTER_PROMPT = """
Jūs esate įrankis nustatyti laiko filtrus, taikomus naudotojo užklausai paieškos programoje.
Žemiau sistema gali naudoti naujumo poslinkį arba griežtą atkirpimą (prieš ribą esantys dokumentai atmetami).
Nustatykite tinkamus filtrus naudotojo užklausai.

Dabartinė data ir laikas: {current_day_time_str}.

VISADA atsakykite TIK JSON, kuriame yra raktai "filter_type", "filter_value", \
"value_multiple" ir "date".

Leistinos "filter_type" reikšmės: "hard cutoff", "favors recent", "not time sensitive".
Leistinos "filter_value" reikšmės: "day", "week", "month", "quarter", "half", "year".
Leistina "value_multiple" reikšmė: bet koks skaičius.
Leistina "date" reikšmė: data MM/DD/YYYY formatu – VISADA laikykitės šio formato.
""".strip()


# Šaltinių filtrai
SOURCE_FILTER_PROMPT = f"""
Pagal naudotojo užklausą ištraukite aktualius šaltinių filtrus, skirtus tolesnei paieškai.
Atsakykite JSON su šaltinių filtrais arba null, jei nenurodyti konkretūs šaltiniai.
ŠALTINIUS IŠTRAUKITE TIK tada, kai naudotojas aiškiai apriboja, iš kur informacija turi būti gaunama.
Naudotojas gali pateikti neteisingus šaltinius – ignoruokite juos.

Leistini šaltiniai:
{{valid_sources}}
{{web_source_warning}}
{{file_source_warning}}


VISADA atsakykite TIK JSON su raktu "{SOURCES_KEY}". \
Reikšmė "{SOURCES_KEY}" turi būti null arba leistinų šaltinių sąrašas.

Pavyzdinis atsakymas:
{{sample_response}}
""".strip()


WEB_SOURCE_WARNING = """
Pastaba: „web“ šaltinis taikomas tik tada, kai naudotojas užklausoje aiškiai mini „svetainę“.
Jis NETAIKOMAS tokiems įrankiams kaip Confluence, GitHub ir pan., kurie turi svetainę.
""".strip()

FILE_SOURCE_WARNING = """
Pastaba: „file“ šaltinis taikomas tik tada, kai naudotojas užklausoje mini įkeltus failus.
""".strip()


if __name__ == "__main__":
    print(TIME_FILTER_PROMPT)
    print("------------------")
    print(SOURCE_FILTER_PROMPT)
