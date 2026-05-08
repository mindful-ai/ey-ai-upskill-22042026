
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd

client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection("policies")

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_markdown("enterprise_500_policy_dataset.md")

docs = df['text'].tolist()

embeddings = model.encode(docs).tolist()

collection.add(documents=docs, embeddings=embeddings, ids=[str(i) for i in range(len(docs))])

print("Data ingested")
