from PyPDF2 import PdfReader, PdfWriter
import re

# Mots-clés de titres d'états financiers
BALANCE_SHEET_KEYWORDS = [r"Balance Sheet", r"Statement of Financial Position", r"Bilan"]
INCOME_STATEMENT_KEYWORDS = [r"Income Statement", r"Statement of Income", r"Compte de résultat", r"Profit and Loss", r"P&L"]
CASH_FLOW_STATEMENT_KEYWORDS = [r"Cash Flow Statement", r"Statement of Cash Flows", r"Tableau des flux de trésorerie"]

ALL_STATEMENT_KEYWORDS = BALANCE_SHEET_KEYWORDS + INCOME_STATEMENT_KEYWORDS + CASH_FLOW_STATEMENT_KEYWORDS

def match_statement_type(text):
    if not text:
        return None
    for pattern in BALANCE_SHEET_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Balance Sheet"
    for pattern in INCOME_STATEMENT_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Income Statement"
    for pattern in CASH_FLOW_STATEMENT_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Cash Flow Statement"
    return None

def is_table_like(page_text):
    if not page_text:
        return False
    lines = page_text.splitlines()
    # Par exemple, on garde si au moins 2 lignes contiennent 3 chiffres
    table_lines = [line for line in lines if len(re.findall(r'\d[\d.,]*', line)) >= 3]
    return len(table_lines) >= 2

def extract_statements_with_continuation(pdf_path, output_pdf):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    n_pages = len(reader.pages)
    i = 0
    while i < n_pages:
        page = reader.pages[i]
        text = page.extract_text()
        st_type = match_statement_type(text)
        if st_type and is_table_like(text):
            print(f"Début d’un {st_type} à la page {i+1}")
            # Ajouter la page courante
            writer.add_page(page)
            # Extraire les pages suivantes qui continuent le tableau
            j = i + 1
            while j < n_pages:
                next_page = reader.pages[j]
                next_text = next_page.extract_text()
                # S’il y a un autre mot-clé de titre, on arrête la séquence
                if match_statement_type(next_text):
                    break
                if is_table_like(next_text):
                    print(f"Tableau continué à la page {j+1}")
                    writer.add_page(next_page)
                    j += 1
                else:
                    break
            i = j  # On saute directement à la page suivante après le tableau
        else:
            i += 1
    if writer.pages:
        with open(output_pdf, "wb") as f:
            writer.write(f)
        print(f"Pages extraites dans {output_pdf}")
    else:
        print("Aucune page trouvée.")

# Utilisation
extract_statements_with_continuation("mon_prospectus.pdf", "etats_financiers_avec_suites.pdf")
