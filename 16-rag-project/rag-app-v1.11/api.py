
from fastapi import FastAPI
from rag_pipeline import ask

app = FastAPI()

@app.get("/ask")  # 127.0.0.1:8000/ask?q=What%20is%20diabetes?
def query(q: str):
    return ask(q)
