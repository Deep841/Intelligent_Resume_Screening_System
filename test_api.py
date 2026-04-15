from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

print("API KEY:", API_KEY)  # should NOT be None

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "google/gemma-3-12b-it:free",
        "messages": [
            {"role": "user", "content": "Say hello in one line"}
        ]
    }
)

print("\nSTATUS:", response.status_code)
print("\nRESPONSE:", response.text)