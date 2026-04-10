import re

def clean_text(text):
    
    # remove newlines
    text = re.sub(r'\n+', ' ', text)
    
    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # convert to lowercase
    text = text.lower()
    
    return text.strip()