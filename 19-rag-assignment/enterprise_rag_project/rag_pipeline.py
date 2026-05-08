
from retrieval import search
from transformers import pipeline

generator=pipeline("text-generation",model="distilgpt2")

PROMPT="""
Answer the question using the context.

Context:
{context}

Question:
{question}
"""

def ask(query):
    context=search(query)
    prompt=PROMPT.format(context="\n".join(context),question=query)
    return generator(prompt,max_length=150)
