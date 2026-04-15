from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def ai_enhanced_score(resume_text, jd_text):
    
    prompt = f"""
    Compare the following resume with the job description.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Give:
    1. A score out of 100
    2. Short reason
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except:
        return "AI scoring failed"
    
# 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