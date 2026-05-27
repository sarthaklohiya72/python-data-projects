import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

body = {
    "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # ✅ Updated model
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Say hello in 10 words."
        }
    ],
    "max_tokens": 100
}

response = requests.post(url, headers=headers, json=body)
data = response.json()
print(data["choices"][0]["message"]["content"])  # Print just the reply