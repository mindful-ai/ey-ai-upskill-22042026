pip uninstall langchain langchain-core langchain-openai langchain-community -y
pip cache purge

pip install --no-cache-dir langchain==1.2.15 langchain-core langchain-openai langchain-community 
pip install --no-cache-dir langgraph langsmith groq tiktoken pydantic sqlalchemy


---

pip install crewai

