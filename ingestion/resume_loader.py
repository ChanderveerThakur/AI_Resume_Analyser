# This file extracts raw text from uploaded resume PDF

import fitz  # PyMuPDF

def load_resume_text(pdf_file):
    text = ""

    # Open PDF using streamlit uploaded file
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text
