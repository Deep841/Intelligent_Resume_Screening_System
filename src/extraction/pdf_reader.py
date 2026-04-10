import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                    
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return text