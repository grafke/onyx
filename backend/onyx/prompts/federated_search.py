from onyx.configs.app_configs import MAX_SLACK_QUERY_EXPANSIONS

SLACK_QUERY_EXPANSION_PROMPT = f"""
Perrašykite vartotojo užklausą ir, jei naudinga, padalykite ją į daugiausia {MAX_SLACK_QUERY_EXPANSIONS}
tik raktinių žodžių užklausas, kad Slack raktinių žodžių paieška pateiktų geriausius atitikmenis.

Atsižvelkite į Slack paieškos elgseną:
- Gryna raktinių žodžių AND paieška (be semantikos).
- Žodžių tvarka svarbi.
- Daugiau žodžių = mažiau atitikmenų, todėl kiekviena užklausa turi būti glausta.

Gairės:
1. Pašalinkite stopžodžius ir triukšmą.
2. Pašalinkite arba sumažinkite meta-instrukcijas (pvz., „parodyk“, „santrauka apie“, „kaip padaryti“),
kurios greičiausiai nepasitaikys tiksliniuose pranešimuose.
3. Laikykitės originalios užklausos žodžių. Jei reikia pridėti numanomus raktinius žodžius (pvz., „kada“ -> „data“),
sukurkite atskirą užklausą.
4. Jei užklausa turi daug raktinių žodžių, sukurkite kelias fokusuotas užklausas, išlaikydami giminingus žodžius kartu;
niekada neskaldykite į vieno žodžio užklausas.
5. Išsaugokite prasmines frazes (pvz., „našumo problemos“); žodis gali kartotis keliose užklausose.
6. Jei nesate tikri, sukurkite ir platesnę, ir siauresnę užklausą.
7. Jei vartotojas klausia apie X arba Y, sukurkite atskiras užklausas X ir Y.

Štai pradinė užklausa:
{{query}}

Grąžinkite TIK naują(-as) užklausą(-as), po vieną eilutėje, daugiausia {MAX_SLACK_QUERY_EXPANSIONS}. Nieko daugiau.
"""
