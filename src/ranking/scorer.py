from sentence_transformers import SentenceTransformer, util

# 🔥 Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_score(resume_skills, jd_skills):
    
    if not jd_skills:
        return 0, [], "No JD skills found"
    
    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))
    
    score = (len(matched) / len(jd_skills)) * 100
    
    reason = f"Matched: {matched}, Missing: {missing}"
    
    return round(score, 2), matched, reason


def semantic_score(resume_text, jd_text):
    
    if not resume_text or not jd_text:
        return 0
    
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    
    similarity = util.cos_sim(emb1, emb2)
    
    return float(similarity) * 100