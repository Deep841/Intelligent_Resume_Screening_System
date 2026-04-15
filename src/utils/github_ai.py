from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("GITHUB_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://models.inference.ai.azure.com"   # 🔥 IMPORTANT
)

def github_ai_feedback(resume_text, jd_text):

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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # 🔥 best free GitHub model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("GitHub AI Error:", e)
        return "AI feedback unavailable"