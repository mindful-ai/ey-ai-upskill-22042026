import json
from langchain_community.vectorstores import Chroma
from rag.vectorstore import get_embeddings

DB_DIR = "rag/chroma_db"


def generate_synthetic_data():
    data = []

    for i in range(100):
        data.append({
            "text": f"Policy {i}: Purchases under {500000 + i*1000} INR allowed for VendorA and VendorB."
        })

    with open("data/synthetic_data.json", "w") as f:
        json.dump(data, f, indent=2)


def ingest_data():
    with open("data/synthetic_data.json") as f:
        data = json.load(f)

    docs = [d["text"] for d in data]

    Chroma.from_texts(
        docs,
        embedding=get_embeddings(),
        persist_directory=DB_DIR
    )

    print("✅ Data ingested into Chroma")


if __name__ == "__main__":
    generate_synthetic_data()
    ingest_data()