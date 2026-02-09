# System prompt (always used)
SYSTEM_PROMPT = """
You are an AI Operations Assistant for Small and Medium Businesses (SMEs).

Goals:
- Increase profit
- Reduce costs
- Save owner's time

Rules:
- Use very simple language
- Give clear, practical actions
- Focus on money and growth
"""

def business_health_prompt(data):
    return f"""
Analyze SME business data:

Sales: {data['sales']}
Expenses: {data['expenses']}
Profit: {data['profit']}

Tasks:
1. Give a health score (0–100)
2. List top 3 problems
3. Suggest 3 simple actions
"""

def sales_prompt(data):
    return f"""
Analyze SME sales data:

{data}

Tasks:
- Identify sales trend
- Detect risks
- Suggest 3 ways to improve sales
"""

def expense_prompt(data):
    return f"""
Analyze SME expense data:

{data}

Tasks:
- Find unnecessary expenses
- Suggest cost-saving actions
"""