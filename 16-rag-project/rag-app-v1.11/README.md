
# Medical RAG Assistant using ChromaDB



## Overview

This project demonstrates a **production-style Retrieval Augmented Generation (RAG) system** using a medical knowledge dataset.

The dataset contains **2000 medical entries** including:

- symptoms
- diagnosis
- treatment
- prevention

Example questions the system can answer:

- What is the course of treatment for type-2 diabetes?
- What are the symptoms of high blood pressure?
- How is asthma diagnosed?
- What lifestyle changes help manage hypertension?

## Architecture

User Question
↓
Embedding Model
↓
ChromaDB Vector Search
↓
Relevant Medical Context
↓
Prompt Construction
↓
LLM Response

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

## Ingest Dataset

```
python ingest.py
```

## Run API

```
uvicorn api:app --reload
```

Open:

```
http://localhost:8000/ask?q=What are the symptoms of high blood pressure?
```

## Files

medical_knowledge_dataset.docx → dataset  
ingest.py → loads data into ChromaDB  
retrieval.py → semantic search  
rag_pipeline.py → RAG logic  
api.py → FastAPI server  

