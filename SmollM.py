import requests

def ask_lm_studio_simple(text):
    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": "undreamai/SmolLM2-360M-Instruct",  # adapte si ton modèle a un nom différent dans LM Studio
        "messages": [
            {"role": "user",
             "content": (
                 "Réponds uniquement par 'suite' si le texte suivant est la suite d’un tableau d’état financier (bilan, compte de résultat, etc). "
                 "Sinon réponds 'annexe' ou 'autre'.\n\n"
                 f"{text}"
             )
            }
        ],
        "temperature": 0,
        "max_tokens": 10
    }
    response = requests.post(url, json=payload)
    if response.ok:
        print("Réponse du modèle :", response.json()["choices"][0]["message"]["content"].strip())
    else:
        print("Erreur API :", response.text)

# Exemple à tester
texte_exemple = """
Cash Flow from operating activities  123.4  234.5  345.6
Cash Flow from investing activities -78.0  -45.2  -32.1
Cash Flow from financing activities  12.0   18.5   24.6
"""
ask_lm_studio_simple(texte_exemple)
