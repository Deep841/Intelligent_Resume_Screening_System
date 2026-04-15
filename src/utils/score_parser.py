import re

def extract_ai_score(ai_text):
    try:
        match = re.search(r"Score:\s*(\d+)", ai_text)
        if match:
            return int(match.group(1))
    except:
        pass
    return 0