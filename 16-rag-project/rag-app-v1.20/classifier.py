from groq import Groq
from config import *

groq_path = r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt"

with open(groq_path) as f:
    api_key = f.read().strip()

llm = Groq(api_key=api_key)

def classify_query(query):

    prompt = f"""
Classify the user query into one of the following categories:

1. Medical Condition
2. General

Rules:
- If query is about diseases, symptoms, diagnosis → Medical Condition
- Otherwise → General

Return ONLY one label.

Query: {query}
"""

    response = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )

    label = response.choices[0].message.content.strip()

    return label