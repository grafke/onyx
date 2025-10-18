# Laikykite sentinelius anglų kalba, nes parsavimas remiasi tiksliais atitikmenimis
USEFUL_PAT = "Yes useful"
NONUSEFUL_PAT = "Not useful"

SECTION_FILTER_PROMPT = f"""
Nustatykite, ar toliau pateikta ištrauka yra NAUDINGA atsakant į vartotojo užklausą.
Vien to, kad ištrauka yra susijusi su užklausa, NEPAKANKA – joje turi būti informacijos,
kuri NAUDINGA atsakymui.
Jei ištraukoje yra BENT kiek naudingos informacijos, to pakanka – ji neturi pilnai atsakyti į visus aspektus.

Pavadinimas: {{title}}
{{optional_metadata}}
Nuorodinė ištrauka:
```
{{chunk_text}}
```

Vartotojo užklausa:
```
{{user_query}}
```

Atsakykite TIKSLIAI IR TIK: "{USEFUL_PAT}" arba "{NONUSEFUL_PAT}"
""".strip()


if __name__ == "__main__":
    print(SECTION_FILTER_PROMPT)
