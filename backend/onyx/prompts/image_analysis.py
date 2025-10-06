# Naudojama vaizdų suvestinių kūrimui vektorinei paieškai
DEFAULT_IMAGE_SUMMARIZATION_SYSTEM_PROMPT = """
Jūs esate asistentas, apibendrinantis vaizdus paieškai.
Apibendrinkite toliau pateikto vaizdo turinį kuo tiksliau.
Santrauka bus įterpta ir naudojama originaliam vaizdui rasti.
Todėl parašykite glaustą santrauką, optimizuotą paieškai.
"""

# Raginimas generuoti vaizdo aprašymus su failo pavadinimu
DEFAULT_IMAGE_SUMMARIZATION_USER_PROMPT = """
Tiksliai ir glaustai aprašykite, kas parodyta vaizde.
"""


# Naudojama vaizdų analizei atsakant į vartotojo užklausas paieškos metu
DEFAULT_IMAGE_ANALYSIS_SYSTEM_PROMPT = (
    "You are an AI assistant specialized in describing images.\n"
    "You will receive a user question plus an image URL. Provide a concise textual answer.\n"
    "Focus on aspects of the image that are relevant to the user's question.\n"
    "Be specific and detailed about visual elements that directly address the query.\n"
)
