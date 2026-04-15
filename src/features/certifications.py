def extract_certifications(text):
    
    keywords = ["certified", "certificate", "aws", "google cloud", "azure"]
    
    found = []
    
    for k in keywords:
        if k in text.lower():
            found.append(k)
    
    return list(set(found))