from docx import Document

def extract_text_from_docx(file_path):
    text = ""
    
    try:
        doc = Document(file_path)
        
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    
    return text