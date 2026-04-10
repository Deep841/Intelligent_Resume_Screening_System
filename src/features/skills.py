import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    
    skills_dict = {
        "python": ["python"],
        "sql": ["sql", "database"],
        "machine learning": ["machine learning", "ml"],
        "fastapi": ["fastapi", "api", "rest api"],
        "docker": ["docker", "container"],
        "pandas": ["pandas", "data analysis"],
        "numpy": ["numpy"]
    }

    doc = nlp(text)
    
    # 🟢 Extract phrases
    phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
    
    combined_text = text + " " + " ".join(phrases)

    found_skills = []

    for skill, keywords in skills_dict.items():
        for keyword in keywords:
            if keyword in combined_text:
                found_skills.append(skill)
                break

    return list(set(found_skills))