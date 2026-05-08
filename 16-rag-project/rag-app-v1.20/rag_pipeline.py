from retrieval import retrieve
from config import *
from sentence_transformers import CrossEncoder
from groq import Groq
import re

# ---------------- GROQ ---------------- #
groq_path = r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt"

with open(groq_path) as f:
    api_key = f.read().strip()

llm = Groq(api_key=api_key)

# ---------------- RERANK ---------------- #
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, docs):
    pairs = [[query, d["page_content"]] for d in docs]
    scores = cross_encoder.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [d for d, _ in ranked[:FINAL_K]]

# ---------------- GENERATE ---------------- #
SYSTEM_PROMPT = """
You are a medical assistant.

STRICT RULES:
- Answer ONLY from context
- If not present → say "I don't know"
"""

def generate(query, docs):
    context = "\n".join([d["page_content"] for d in docs])

    prompt = f"""
Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content.strip(), context

# ---------------- VALIDATE ---------------- #
def extract_score(text):
    match = re.search(r"\d*\.?\d+", text)
    return float(match.group()) if match else 0.0

def validate(query, answer, context):
    prompt = f"""
Score from 0 to 1.

Question: {query}
Context: {context}
Answer: {answer}
"""

    response = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )

    return extract_score(response.choices[0].message.content)

# ---------------- MAIN ---------------- #
def rag_answer(query):

    docs = retrieve(query)

    if not docs:
        return {"answer": "I don't know"}

    docs = rerank(query, docs)

    answer, context = generate(query, docs)

    score = validate(query, answer, context)

    return {
        "answer": answer,
        "confidence": score
    }

if __name__ == "__main__":
    test_query = "What are the symptoms of diabetes?"
    result = rag_answer(test_query)
    print("Answer:", result["answer"])
