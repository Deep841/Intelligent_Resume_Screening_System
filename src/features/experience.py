import re

def extract_experience(text):
    
    matches = re.findall(r'(\d+)\+?\s*(years|year)', text)
    
    if matches:
        return max([int(m[0]) for m in matches])
    
    return 0