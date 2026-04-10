from src.features.skills import extract_skills

def parse_job_description(text):
    
    skills = extract_skills(text)
    
    return {
        "required_skills": skills
    }