# PDF Financial Statement Extractor 📄🤖

A Python tool that leverages a local Large Language Model (LLM) via LM Studio to intelligently identify and extract pages containing financial statements (balance sheets, income statements, cash flow statements) from bond prospectus PDFs.

---

## 🧠 Features

- Parses and extracts text from every page of a PDF document.
- Sends page text to a locally hosted LLM (e.g., SmolLM2 via LM Studio) for classification.
- Classifies pages into:
  - `"suite"`: continuation of a financial table → **included** in the output PDF.
  - `"annexe"` or `"autre"`: supplementary or unrelated content → **excluded**.
- Produces a new PDF containing **only relevant financial tables** for streamlined analysis.

---

## 📄 Extended Description

This tool automates the extraction and processing of financial data from bond prospectuses, enabling the transformation of unstructured PDF documents into clean, structured data formats such as Excel spreadsheets. By filtering out irrelevant pages and isolating financial tables, it significantly accelerates the work of financial analysts.

### Workflow Overview

1. **PDF Parsing**: Reads each page from the input PDF.
2. **Content Analysis**: Sends page text to the LLM to determine if the page contains financial statement data.
3. **Page Classification**: Receives classification labels from the LLM.
4. **Filtered PDF Output**: Generates a PDF containing only pages classified as financial tables.

### Practical Benefits

- Automates the calculation of intermediate management balances and key financial ratios.
- Reduces manual extraction time and human error.
- Allows analysts to focus on interpreting data rather than formatting it.

---

## 🧰 Tech Stack

- [`PyPDF2`](https://pypi.org/project/PyPDF2/) for PDF reading and writing
- [`requests`](https://pypi.org/project/requests/) to communicate with the LLM API
- [LM Studio](https://lmstudio.ai/) to run the LLM locally with configurable models and ports
- Example model: `undreamai/SmolLM2-360M-Instruct`

---

## 🛠️ Usage

1. **Start your LLM** instance in LM Studio.  
2. **Configure the script** with the correct model name and LM Studio port (see variables `MODEL_NAME` and `LMSTUDIO_PORT` in the script).  
3. **Run the script** from your terminal:

   ```bash
   python extract_pdf_financial_statements.py
