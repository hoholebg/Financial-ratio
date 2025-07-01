# PDF Financial Statement Extractor 📄🤖

This Python script uses a local LLM (via LM Studio) to identify and extract pages from a PDF that correspond to financial statements (balance sheets, income statements, cash flow).

## 🧠 Features

- Extracts text from each page of a PDF
- Sends the text to a locally hosted LLM (e.g. SmolLM2 via LM Studio)
- Classifies pages as:
  - "suite" → part of a financial table → included in final PDF
  - "annexe" or "autre" → ignored
- Outputs a new PDF containing only relevant financial tables

## 🧰 Tech Stack

- `PyPDF2` for PDF manipulation
- `requests` to query the LLM API
- `LM Studio` for running the LLM locally (adjustable model & port)
- Model example: `undreamai/SmolLM2-360M-Instruct`

## 🛠️ Usage

1. Start your LLM in [LM Studio](https://lmstudio.ai/)  
2. Set the right model and port in the config section of the script  
3. Run the script:

```bash
python extract_pdf_financial_statements.py
