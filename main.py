import os
import json
from src.extraction.extractor import extract_text
from src.preprocessing.clean import clean_text
from src.jd_parser.parser import parse_job_description
from src.features.skills import extract_skills
from src.ranking.scorer import calculate_score, semantic_score
from src.features.experience import extract_experience
from src.features.education import extract_education
from src.features.certifications import extract_certifications
from src.rag.retriever import get_company_score_rag
from src.utils.github_ai import github_ai_feedback
from src.utils.score_parser import extract_ai_score

RESUME_FOLDER = "data/resumes"


def process_resumes():

    jd_skills = []
    jd_clean = ""
    resumes = []
    results = []

    # 🔴 PASS 1: Extract JD
    for file in os.listdir(RESUME_FOLDER):

        if file.startswith("."):
            continue

        if not (file.endswith(".pdf") or file.endswith(".docx")):
            continue

        file_path = os.path.join(RESUME_FOLDER, file)

        raw_text = extract_text(file_path)
        clean = clean_text(raw_text)

        if "jd" in file.lower():
            jd_clean = clean
            jd_data = parse_job_description(clean)
            jd_skills = jd_data.get("required_skills", [])

        else:
            resumes.append((file, clean))

    # ❌ Safety check (IMPORTANT FIX)
    if not jd_skills:
        return []

    # 🟢 PASS 2: Base scoring
    for file, clean in resumes:

        skills = extract_skills(clean)

        skill_score, matched, reason = calculate_score(skills, jd_skills)
        semantic = semantic_score(clean, jd_clean)

        exp = extract_experience(clean)
        education = extract_education(clean)
        certs = extract_certifications(clean)

        company_score = get_company_score_rag(clean)

        experience_score = min(exp * 10, 100)
        education_score = 10 if education else 0
        cert_score = 10 if certs else 0

        base_score = (
            0.35 * skill_score +
            0.2 * semantic +
            0.2 * experience_score +
            0.1 * company_score * 10 +
            0.15 * education_score
        )

        results.append({
            "name": file,
            "score": round(base_score, 2),
            "matched_skills": matched,
            "education": education,
            "certifications": certs,
            "experience": exp,
            "company_score": company_score,
            "reason": reason,
            "clean_text": clean,   # 🔥 IMPORTANT (for AI)
            "ai_feedback": "",
            "ai_score": 0
        })

    # 🔥 Sort before AI
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # 🔥 AI only for top 2 (FIXED PROPERLY)
    for i, r in enumerate(results):
        if i < 2:
            try:
                ai_feedback = github_ai_feedback(r["clean_text"], jd_clean)
                r["ai_feedback"] = ai_feedback

                ai_score = extract_ai_score(ai_feedback)

                if ai_score > 0:
                    r["ai_score"] = ai_score
                    r["score"] = round((0.8 * r["score"]) + (0.2 * ai_score), 2)

            except Exception as e:
                r["ai_feedback"] = f"AI error: {str(e)}"

        else:
            r["ai_feedback"] = "Skipped to save API usage"

        # 🔥 CLEAN MEMORY (IMPORTANT)
        if "clean_text" in r:
            del r["clean_text"]

    # 🔥 Final sort after AI
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results


# 🚀 ENTRY POINT (CLEAN JSON ONLY)
if __name__ == "__main__":
    try:
        results = process_resumes()
        print(json.dumps(results))
    except Exception as e:
        print(json.dumps({"error": str(e)}))