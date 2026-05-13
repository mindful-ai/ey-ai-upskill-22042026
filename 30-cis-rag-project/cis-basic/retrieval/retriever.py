from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


from dotenv import load_dotenv
load_dotenv()

def get_retriever():
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local(
        "vectorstore/",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 10}  # top 4 chunks
    )

    return retriever