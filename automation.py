def decide_automation(ai_text):
    text = ai_text.lower()

    if "high risk" in text or "urgent" in text:
        return {
            "action": "Send WhatsApp alert to owner",
            "priority": "High"
        }

    if "medium risk" in text:
        return {
            "action": "Send email report",
            "priority": "Medium"
        }

    return {
        "action": "No action required",
        "priority": "Low"
    }