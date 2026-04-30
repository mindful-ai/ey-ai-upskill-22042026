
# Replace this with real LLM API

def model_call(prompt, question):
    q = question.lower()
    if "diabetes" in q:
        return "A metabolic disorder"
    if "hypertension" in q:
        return "High blood pressure"
    if "capital" in q:
        return "New Delhi"
    return "Unknown"
