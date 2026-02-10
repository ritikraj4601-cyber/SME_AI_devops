from fastapi import FastAPI
from pydantic import BaseModel
import json

from db import get_db
from ai_groq import groq_ai
from ai_gemini import gemini_ai
from prompts import business_analysis_prompt

app = FastAPI(title="SME AI Platform", version="1.0")


# ---------- DATA MODEL ----------
class BusinessInput(BaseModel):
    sales: int
    expenses: int
    profit: int


# ---------- HEALTH CHECK ----------
@app.get("/")
def health():
    return {"status": "running"}


# ---------- SAFE JSON PARSER ----------
def safe_parse(ai_text: str) -> dict:
    try:
        return json.loads(ai_text)
    except Exception:
        return {
            "health_score": 50,
            "risk_level": "Medium",
            "summary": "AI response could not be parsed",
            "recommendation": "Review the business data manually"
        }


# ---------- MAIN ANALYSIS API ----------
@app.post("/analyze")
def analyze_business(data: BusinessInput):
    # 1. Build prompt
    prompt = business_analysis_prompt({
        "sales": data.sales,
        "expenses": data.expenses,
        "profit": data.profit
    })

    # 2. Call AI (Groq → Gemini fallback)
    try:
        ai_raw = groq_ai(prompt)
        ai_source = "groq"
    except Exception:
        ai_raw = gemini_ai(prompt)
        ai_source = "gemini"

    # 3. Parse AI output safely
    ai_result = safe_parse(ai_raw)

    # 4. Save to database
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO business_health
        (sales, expenses, profit, ai_source, ai_output)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data.sales,
            data.expenses,
            data.profit,
            ai_source,
            json.dumps(ai_result)
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    # 5. Return response
    return {
        "ai_source": ai_source,
        "result": ai_result
    }


# ---------- HISTORY API ----------
@app.get("/history")
def history():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            sales,
            expenses,
            profit,
            ai_source,
            ai_output,
            created_at
        FROM business_health
        ORDER BY created_at DESC
        LIMIT 10
        """
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "sales": r[0],
            "expenses": r[1],
            "profit": r[2],
            "ai_source": r[3],
            "ai_output": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]


# ---------- LOCAL RUN (OPTIONAL) ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)