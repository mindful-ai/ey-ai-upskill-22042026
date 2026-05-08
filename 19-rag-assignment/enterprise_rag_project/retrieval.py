
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_collection("policies")

model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query,k=5):
    emb=model.encode([query]).tolist()
    res=collection.query(query_embeddings=emb,n_results=k)
    return res["documents"][0]
