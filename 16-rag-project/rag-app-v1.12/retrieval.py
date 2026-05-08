import chromadb
from chromadb.utils import embedding_functions
from config import *
from groq import Groq

# ---------------- GROQ CLIENT ---------------- #
groq_path = r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt"

with open(groq_path, "r") as f:
    api_key = f.read().strip()

llm_client = Groq(api_key=api_key)

# ---------------- INIT ---------------- #
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# ---------------- QUERY EXPANSION ---------------- #
def expand_query(query):
    return [
        query,
        f"{query} symptoms",
        f"{query} signs",
        f"{query} definition",
        f"{query} causes"
    ]

# ---------------- QUERY REWRITE ---------------- #
def rewrite_query(query):
    prompt = f"""
    Rewrite this medical query for better retrieval:\n{query}
    Return only the rewritten query, nothing else.
    """

    response = llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

# ---------------- RETRIEVE ---------------- #
def retrieve(query, k=TOP_K):
    queries = expand_query(query)

    all_docs = []

    for q in queries:
        results = collection.query(
            query_texts=[q],
            n_results=k
        )

        docs = results.get("documents", [[]])[0]
        all_docs.extend(docs)

    # ---------------- DEDUP ---------------- #
    unique_docs = list(dict.fromkeys(all_docs))

    docs = [{"page_content": d} for d in unique_docs]

    # ---------------- DIVERSITY FILTER ---------------- #
    selected = []
    for d in docs:
        if all(d["page_content"][:50] not in s["page_content"] for s in selected):
            selected.append(d)
        if len(selected) >= k:
            break

    print(f"Documents retrieved: {len(selected)}")
    return selected

if __name__ == "__main__":
    query = "What are the symptoms of diabetes?"
    results = retrieve(query)
    for i, doc in enumerate(results):
        print(f"Doc {i+1}:\n{doc['page_content']}\n{'-'*50}")