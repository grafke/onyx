PERSONA_CATEGORY_GENERATION_PROMPT = """
Remiantis asistento vardu, aprašu ir instrukcijomis, sugeneruokite {num_categories}
**unikalias ir įvairias** kategorijas, atspindinčias skirtingus pradinės žinutės tipus,
kurias vartotojas gali parašyti pokalbio pradžiai su šiuo asistentu.

**Įsitikinkite, kad kategorijos yra aktualios ir apima temas, susijusias su asistento galimybėmis.**

Pateikite kategorijas kaip JSON masyvą iš eilučių **be kodo blokų ir papildomo teksto**.

**Kontekstas apie asistentą:**
- **Vardas**: {name}
- **Aprašymas**: {description}
- **Instrukcijos**: {instructions}
"""

PERSONA_STARTER_MESSAGE_CREATION_PROMPT = """
Sukurkite pradinę žinutę, kurią **vartotojas** galėtų parašyti pokalbį pradedančiai su pokalbių asistentu.

{category_prompt}

Jūsų atsakymas turėtų apimti tik pačią žinutę, kurią vartotojas siųstų asistentui.
Ji turi būti natūrali, įtrauki anti ir paskatinanti naudingą asistento reakciją.
**Venkite pernelyg specifinių detalių; žinutė turi būti bendra ir plačiai taikoma.**

Pavyzdžiui:
- Vietoj „Ką tik įsigijau 6 mėn. Labradoro šuniuką, kuris tempia pavadėlį,“
rašykite „Man sunku išmokyti savo naują šuniuką gražiai eiti su pavadėliu.“
Nepateikite jokio papildomo teksto ar paaiškinimų ir būkite labai glausti.

**Kontekstas apie asistentą:**
- **Vardas**: {name}
- **Aprašymas**: {description}
- **Instrukcijos**: {instructions}
""".strip()


def format_persona_starter_message_prompt(name: str, description: str, instructions: str, category: str | None = None) -> str:
    category_prompt = f"**Kategorija**: {category}" if category else ""
    return PERSONA_STARTER_MESSAGE_CREATION_PROMPT.format(
        category_prompt=category_prompt,
        name=name,
        description=description,
        instructions=instructions,
    )


if __name__ == "__main__":
    print(PERSONA_CATEGORY_GENERATION_PROMPT)
    print(PERSONA_STARTER_MESSAGE_CREATION_PROMPT)
