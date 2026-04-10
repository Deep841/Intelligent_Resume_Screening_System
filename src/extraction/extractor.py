import os
from .pdf_reader import extract_text_from_pdf
from .docx_reader import extract_text_from_docx

def extract_text(file_path):
    
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    
    else:
        return ""