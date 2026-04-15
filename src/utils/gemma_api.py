from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def gemma_ai_feedback(resume_text, jd_text):

    prompt = f"""
    You are an AI hiring assistant.

    Compare the following resume with the job description.

    Return STRICT FORMAT:

    Score: <number>/100
    Strengths: <points>
    Missing Skills: <points>
    Recommendation: <short>

    Resume:
    {resume_text[:2000]}

    Job Description:
    {jd_text[:1000]}
    """

    for attempt in range(3):  # 🔥 retry logic
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemma-3-12b-it:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        # 🔴 HANDLE ERROR
        if "error" in data:
            print("Retrying due to rate limit...")
            time.sleep(2)
            continue

        try:
            return data["choices"][0]["message"]["content"]
        except:
            return "AI parsing error"

    return "AI temporarily unavailable"