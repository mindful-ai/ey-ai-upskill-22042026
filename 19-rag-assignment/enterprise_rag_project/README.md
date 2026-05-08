
# Enterprise RAG Project

Steps

1 Install dependencies
pip install -r requirements.txt

2 Ingest dataset
python ingest.py

3 Run API
uvicorn api:app --reload

4 Query
http://localhost:8000/ask?q=leave policy
