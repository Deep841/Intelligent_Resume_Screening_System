from openai import OpenAI

client = OpenAI()

def enrich_profile(text):
    
    prompt = f"""
    Extract:
    - company quality (1-10)
    - role complexity
    - education level
    from this resume:
    {text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content