def business_analysis_prompt(data: dict) -> str:
    """
    Stable, JSON-only business analysis prompt
    """

    return f"""
You are a professional SME business advisor.

Your task:
- Analyze the business numbers
- Be practical and conservative
- Do NOT exaggerate
- Do NOT add explanations outside JSON

Business data:
Sales: {data['sales']}
Expenses: {data['expenses']}
Profit: {data['profit']}

Rules:
- Respond ONLY in valid JSON
- Do NOT add markdown
- Do NOT add extra text
- Do NOT change key names
- Values must be realistic

Output format (STRICT):
{{
  "health_score": number (0-100),
  "risk_level": "Low" | "Medium" | "High",
  "summary": "1-line business condition",
  "recommendation": "1 practical action step"
}}

Now respond.
"""