from db import get_db
from fastapi import FastAPI
from ai_engine import run_ai
from prompts import (
    business_health_prompt,
    sales_prompt,
    expense_prompt
)
from automation import decide_automation

app = FastAPI(title="SME AI Operations App (Mobile Built)")

@app.get("/")
def home():
    return {
        "status": "SME AI Operations Backend running on mobile"
    }

from schemas import BusinessHealthRequest

@app.post("/business-health")
def business_health(data: BusinessHealthRequest):
    prompt = business_health_prompt(data.dict())
    ai_result = run_ai(prompt)
    automation = decide_automation(ai_result)
    from db import conn, cursor
import json

@app.post("/business-health")
def business_health(data: BusinessHealthRequest):
    prompt = business_health_prompt(data.dict())
    ai_result = run_ai(prompt)

    try:
        result = json.loads(ai_result)
    except:
        return {"error": "AI output not JSON", "raw": ai_result}

    # Save to DB
    cursor.execute("""
        INSERT INTO business_health 
        (sales, expenses, profit, health_score, risk_level)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.sales,
        data.expenses,
        data.profit,
        result.get("health_score"),
        result.get("risk_level")
    ))
    conn.commit()

    return resulto

    return {
        "ai_insight": ai_result,
        "automation": automation
    }
    

    return {
        "ai_insight": ai_result,
        "automation": automation
    }

@app.post("/sales-analysis")
def sales_analysis(data: dict):
    prompt = sales_prompt(data)
    ai_result = run_ai(prompt)

    return {
        "ai_insight": ai_result
    }

@app.post("/expense-analysis")
def expense_analysis(data: dict):
    prompt = expense_prompt(data)
    ai_result = run_ai(prompt)

    return {
        "ai_insight": ai_result
    }
    import json

@app.post("/business-health")
def business_health(data: BusinessHealthRequest):
    prompt = business_health_prompt(data.dict())
    ai_result = run_ai(prompt)

    try:
        structured = json.loads(ai_result)
    except:
        structured = {
            "error": "AI response could not be parsed",
            "raw_output": ai_result
        }
@app.get("/history")
def get_history():
    try:
        conn, cursor = get_db()

        cursor.execute("""
            SELECT id, sales, expenses, profit, health_score, risk_level, created_at
            FROM business_health
            ORDER BY created_at DESC
            LIMIT 20
        """)
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "sales": r[1],
                "expenses": r[2],
                "profit": r[3],
                "health_score": r[4],
                "risk_level": r[5],
                "created_at": r[6]
            }
            for r in rows
        ]
    except Exception as e:
        return {
            "error": "DB read failed",
            "details": str(e)
        }
@app.get("/history")
def history():
    try:
        from db import get_db   # force import inside function

        conn, cursor = get_db()

        cursor.execute("""
            SELECT id, sales, expenses, profit, health_score, risk_level, created_at
            FROM business_health
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return {
            "count": len(rows),
            "rows": rows
        }

    except Exception as e:
        return {
            "error": "HISTORY_FAILED",
            "type": str(type(e)),
            "details": str(e)
        }
    return structured