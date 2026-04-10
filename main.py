import os
from src.extraction.extractor import extract_text
from src.preprocessing.clean import clean_text
from src.jd_parser.parser import parse_job_description
from src.features.skills import extract_skills
from src.ranking.scorer import calculate_score, semantic_score
from src.features.experience import extract_experience


RESUME_FOLDER = "data/resumes"

def process_resumes():
    
    jd_skills = []
    jd_clean = ""
    resumes = []
    results = []

    # 🔴 PASS 1: Extract JD first
    for file in os.listdir(RESUME_FOLDER):
        
        # skip hidden/system files
        if file.startswith("."):
            continue
        
        # skip unsupported files
        if not (file.endswith(".pdf") or file.endswith(".docx")):
            continue

        file_path = os.path.join(RESUME_FOLDER, file)
        
        raw_text = extract_text(file_path)
        clean = clean_text(raw_text)
        
        if "jd" in file.lower():
            jd_clean = clean
            jd_data = parse_job_description(clean)
            jd_skills = jd_data["required_skills"]
            
            print("\nJD SKILLS:", jd_skills)
        
        else:
            resumes.append((file, clean))

    # 🟢 PASS 2: Process resumes
    for file, clean in resumes:
        
        skills = extract_skills(clean)
        
        score, matched, reason = calculate_score(skills, jd_skills)
        
        # 🔥 Semantic matching
        semantic = semantic_score(clean, jd_clean)
        
        exp = extract_experience(clean)

        
        final_score = (0.5 * score) + (0.2 * semantic) + (0.3 * exp * 10)
        
        results.append({
            "name": file,
            "score": round(final_score, 2),
            "matched_skills": matched,
            "reason": reason
        })

    return results


if __name__ == "__main__":
    
    results = process_resumes()
    
    print("\n===== FINAL RANKING =====\n")
    
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    for r in results:
        print(f"{r['name']} → Score: {r['score']}%")
        print(f"Matched Skills: {r['matched_skills']}")
        print(f"Reason: {r['reason']}")
        print("------------------------")