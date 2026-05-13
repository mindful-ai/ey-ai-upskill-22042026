from langchain_openai import ChatOpenAI
from retrieval.retriever import get_retriever

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    retriever = get_retriever()

    def run(query):
        docs = retriever.invoke(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a CIS Policy Intelligence Agent.

Use the context below to answer the query.

CONTEXT:
{context}

QUERY:
{query}

Respond in this structured format:

1. Answer:
- Direct answer

2. Relevant CIS Controls:
- List controls if found

3. Summary:
- Short explanation

4. Recommendations:
- Actionable security steps

Rules:
- Be precise
- Do not hallucinate
- Use only provided context
"""

        response = llm.invoke(prompt)

        return {
            "query": query,
            "answer": response.content,
            "source_docs": docs
        }

    return run