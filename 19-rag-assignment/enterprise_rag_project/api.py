
from fastapi import FastAPI
from rag_pipeline import ask

app=FastAPI()

@app.get("/ask")
def query(q:str):
    return ask(q)
