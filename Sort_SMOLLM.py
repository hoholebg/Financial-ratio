import requests
from PyPDF2 import PdfReader, PdfWriter

# ---- Configuration ----
PDF_INPUT = "mon_prospectus.pdf"
PDF_OUTPUT = "etats_financiers_filtre_llm.pdf"
MODEL_NAME = "undreamai/SmolLM2-360M-Instruct"   # Change si besoin (voir LM Studio)
LMSTUDIO_PORT = 1234                            # Change si tu as modifié le port

def ask_lm_studio(text):
    url = f"http://localhost:{LMSTUDIO_PORT}/v1/chat/completions"
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user",
             "content": (
                 "Réponds uniquement par 'suite' si le texte suivant est la suite d’un tableau d’état financier (bilan, compte de résultat, flux de trésorerie). "
                 "Sinon réponds 'annexe' ou 'autre'.\n\n"
                 f"{text}"
             )
            }
        ],
        "temperature": 0,
        "max_tokens": 10
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.ok:
            rep = response.json()["choices"][0]["message"]["content"].strip().lower()
            return rep
        else:
            print("Erreur API :", response.text)
            return None
    except Exception as e:
        print("Erreur connexion LM Studio :", e)
        return None

def is_suite(response_text):
    # Tolérant à la casse, espaces, ponctuation
    if not response_text:
        return False
    # Accepte "suite", "suite.", "Suite", "SUiTe", etc.
    return response_text.strip().lower().startswith("suite")

def filter_pdf_with_llm(pdf_in, pdf_out):
    reader = PdfReader(pdf_in)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        print(f"Page {i+1} : interrogation du LLM...")
        llm_response = ask_lm_studio(text)
        print(f"    => Réponse LLM : {llm_response}")
        if is_suite(llm_response):
            writer.add_page(page)
            print(f"    >> Page {i+1} ajoutée au PDF final")
        else:
            print(f"    -- Page {i+1} ignorée")
    if writer.pages:
        with open(pdf_out, "wb") as f:
            writer.write(f)
        print(f"\n✅ Nouveau PDF créé : {pdf_out}")
    else:
        print("\n❌ Aucune page n'a été retenue.")

# -----------------------
# Lance le traitement :
filter_pdf_with_llm(PDF_INPUT, PDF_OUTPUT)
