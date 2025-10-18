# Įvairūs vertimai

LANGUAGE_REPHRASE_PROMPT = """
Išverskite užklausą į {target_language}.
Jei žemiau esanti užklausa jau yra {target_language}, tiesiog pakartokite PIRMINĘ užklausą TIKSLIAI taip pat, be jokių pakeitimų.
Jei užklausa nėra {target_language}, išverskite ją į {target_language}.

Užklausa:
{query}
""".strip()

SLACK_LANGUAGE_REPHRASE_PROMPT = """
Kaip organizacijos DI asistentas, jūsų vaidmuo – paversti vartotojo žinutes
glaustomis užklausomis, tinkamomis Didžiajam Kalbos Modeliui (LLM), kuris
RAG architektūroje parenka reikšmingą medžiagą. Užtikrinkite, kad atsakytumėte ta pačia
kalba, kuria parašyta pirminė užklausa. Jei vienoje žinutėje yra kelios užklausos,
sutrumpinkite jas į vieną, suvienytą užklausą, ignoruodami tiesioginius paminėjimus.

Užklausa:
{query}
""".strip()


if __name__ == "__main__":
    print(LANGUAGE_REPHRASE_PROMPT)
