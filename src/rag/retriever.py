from src.rag.knowledge_loader import load_knowledge

def extract_company_name(text):
    # simple heuristic (can improve later)
    keywords = ["google", "amazon", "microsoft", "tcs", "infosys", "mphasis"]
    
    for k in keywords:
        if k in text.lower():
            return k
    
    return None


def get_company_score_rag(text):
    company = extract_company_name(text)

    if not company:
        return 5   # neutral

    knowledge = load_knowledge(company)

    if not knowledge:
        return 5

    knowledge = knowledge.lower()

    # simple scoring logic
    if "technology" in knowledge or "ai" in knowledge:
        return 8
    elif "services" in knowledge:
        return 6
    else:
        return 5