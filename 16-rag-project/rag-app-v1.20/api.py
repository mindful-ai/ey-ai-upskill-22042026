from fastapi import FastAPI
from rag_pipeline import rag_answer
from classifier import classify_query
from groq import Groq
from config import *

app = FastAPI()

# fallback LLM
groq_path = r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt"

with open(groq_path) as f:
    api_key = f.read().strip()

llm = Groq(api_key=api_key)

def general_answer(query):
    response = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": query}],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

@app.get("/ask")
def ask(q: str):

    label = classify_query(q)
    print("Query Type:", label)

    if "Medical" in label:
        result = rag_answer(q)
        result["type"] = "medical"
        return result

    else:
        return {
            "type": "general",
            "answer": general_answer(q)
        }
    
if __name__ == "__main__":
    #import uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=8000)
    query = "What is the color of the sky?"
    print("Query:", query)  
    result = ask(query)
    print("Result:", result)