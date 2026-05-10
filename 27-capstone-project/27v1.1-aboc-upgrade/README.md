### Run with out UI and API
pip install -U langchain-huggingface # for ingest.py HuggingFaceEmbeddings

pip install -r requirements.txt

python rag/ingest.py -> python -m rag.ingest
Note: delete chromadb -> if taking into a different environment or if there are errors

python app.py

### Run with UI and API

uvicorn api.main:app --reload
streamlit run ui/app.py

Test: Create a PO for 50 sensors from VendorA under 400000 INR

### Notes

In approval_agent.py

```python
if "streamlit" in state:
    return True  # auto approve for UI
```

👉 Avoids blocking input in UI mode

### Final system capability


You now have:

✔ Multi-agent system
✔ LangGraph orchestration
✔ LLM (Groq)
✔ RAG (Chroma)
✔ Memory (DB + semantic)
✔ Tool usage
✔ Human-in-loop
✔ API layer
✔ UI layer