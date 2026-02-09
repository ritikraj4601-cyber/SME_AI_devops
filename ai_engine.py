import requests
from config import GROQ_API_KEY
from prompts import SYSTEM_PROMPT

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

import requests
import os
from prompts import SYSTEM_PROMPT

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def run_ai(user_prompt):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "ERROR: GROQ_API_KEY is missing in environment variables"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"GROQ ERROR: {str(e)}"