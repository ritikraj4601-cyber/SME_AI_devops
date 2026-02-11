import os, io, requests, json
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- ENV VARS ---
GROQ_KEY = os.environ.get("GROQ_API_KEY")
MJ_KEY = os.environ.get("MJ_APIKEY_PUBLIC")
MJ_SECRET = os.environ.get("MJ_APIKEY_PRIVATE")
SENDER = os.environ.get("SENDER_EMAIL")

class SMETask(BaseModel):
    objective: str
    csv_url: Optional[str] = None
    email_to: Optional[str] = None

@app.post("/auto-ops")
async def execute_sme_operation(request: SMETask):
    # 1. DATA ANALYSIS
    insight = "No data source."
    if request.csv_url:
        try:
            r = requests.get(request.csv_url, timeout=10)
            df = pd.read_csv(io.StringIO(r.text))
            insight = df.describe().to_json() # Extracting stats
        except: insight = "Data link error."

    # 2. PROMPT ENGINEERING
    prompt = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an SME Operations Expert. Always output JSON with 'strategy' and 'email_body' keys."},
            {"role": "user", "content": f"Task: {request.objective}\nData: {insight}"}
        ],
        "response_format": {"type": "json_object"} # Ensuring structured output
    }

    # 3. AI EXECUTION
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {GROQ_KEY}"}, json=prompt)
        ai_output = json.loads(res.json()['choices'][0]['message']['content'])
    except Exception as e:
        ai_output = {"strategy": "System Error", "email_body": str(e)}

    # 4. EMAIL AUTOMATION
    if request.email_to and MJ_KEY:
        mail_data = {
            "Messages": [{"From": {"Email": SENDER}, "To": [{"Email": request.email_to}],
            "Subject": "SME Operational Report", "HTMLPart": ai_output['email_body']}]
        }
        requests.post("https://api.mailjet.com/v3.1/send", auth=(MJ_KEY, MJ_SECRET), json=mail_data)

    return ai_output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
