import re

def extract_education(text):
    
    degrees = ["b.tech", "m.tech", "b.sc", "m.sc", "mba", "mca", "bachelor", "master"]
    
    found = []
    
    for degree in degrees:
        if degree in text.lower():
            found.append(degree)
    
    return list(set(found))