from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def gemma_ai_feedback(resume_text, jd_text):

    prompt = f"""
    Compare resume with job description and give:
    - Score out of 100
    - Strengths
    - Missing skills
    - Recommendation
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "google/gemma-3-12b-it:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )

    return response.json()