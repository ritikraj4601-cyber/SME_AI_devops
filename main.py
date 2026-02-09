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

@app.post("/business-health")
def business_health(data: dict):
    prompt = business_health_prompt(data)
    ai_result = run_ai(prompt)
    automation = decide_automation(ai_result)

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