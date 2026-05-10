from langchain.tools import tool
from rag.vectorstore import get_vectorstore


@tool
def retrieve_policy_tool(query: str) -> str:
    """
    Retrieve relevant company policies from the vector database
    based on the given query.
    """
    vectordb = get_vectorstore()
    docs = vectordb.similarity_search(query, k=3)

    return "\n".join([d.page_content for d in docs])