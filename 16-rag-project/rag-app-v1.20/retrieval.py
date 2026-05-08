import chromadb
from chromadb.utils import embedding_functions
from config import *

from rank_bm25 import BM25Okapi
import re

# ---------------- INIT ---------------- #
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# ---------------- LOAD ALL DOCS FOR BM25 ---------------- #
all_docs_data = collection.get(include=["documents"])
corpus = all_docs_data["documents"]

# tokenize corpus
tokenized_corpus = [doc.lower().split() for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

# ---------------- QUERY EXPANSION ---------------- #
def expand_query(query):
    return [
        query,
        f"{query} symptoms",
        f"{query} definition",
        f"{query} causes"
    ]

# ---------------- BM25 RETRIEVAL ---------------- #
def bm25_retrieve(query, k=TOP_K):
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        list(zip(corpus, scores)),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:k]]

# ---------------- VECTOR RETRIEVAL ---------------- #
def vector_retrieve(query, k=TOP_K):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results.get("documents", [[]])[0]

# ---------------- HYBRID RETRIEVAL ---------------- #
def retrieve(query, k=TOP_K):

    queries = expand_query(query)

    vector_docs = []
    bm25_docs = []

    for q in queries:
        vector_docs.extend(vector_retrieve(q, k))
        bm25_docs.extend(bm25_retrieve(q, k))

    # ---------------- MERGE ---------------- #
    combined = list(set(vector_docs + bm25_docs))

    # ---------------- FORMAT ---------------- #
    docs = [{"page_content": d} for d in combined[:k]]

    print(f"Hybrid retrieved docs: {len(docs)}")
    return docs

if __name__ == "__main__":
    test_query = "What are the symptoms of diabetes?"
    retrieved_docs = retrieve(test_query)
    for i, doc in enumerate(retrieved_docs):
        print(f"Doc {i+1}: {doc['page_content'][:100]}...")