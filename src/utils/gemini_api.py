from dotenv import load_dotenv
import os
import google.generativeai as genai

# load env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# configure Gemini
genai.configure(api_key=API_KEY)

# load model
model = genai.GenerativeModel("gemini-1.5-flash")


def gemini_ai_feedback(resume_text, jd_text):

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
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "AI feedback unavailable"