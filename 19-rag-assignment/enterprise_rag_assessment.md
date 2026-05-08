
# Enterprise RAG Assessment – ChromaDB Policy Assistant

Generated: 2026-03-12

## Background

You are provided with an enterprise dataset containing **500 detailed policy documents** across five domains:

- HR Policies
- Data Governance Policies
- Network Management Policies
- Employee Conduct Policies
- Security Policies

Each policy document contains structured sections:

- Scope
- Policy Statement
- Responsibilities
- Procedures
- Compliance
- References

The dataset simulates a **corporate policy knowledge base**.

---

# Objective

Build a **Retrieval Augmented Generation (RAG) system** using **ChromaDB** that allows employees to query company policies and receive accurate answers grounded in official policy documentation.

---

# Tasks

## Task 1 – Data Processing
- Parse the markdown dataset
- Split policies into chunks
- Prepare metadata (policy id, domain)

## Task 2 – Vector Database
- Generate embeddings
- Store documents in ChromaDB
- Attach metadata

## Task 3 – Retrieval
Implement:
- Semantic vector search
- Top-k retrieval

## Task 4 – Advanced Retrieval
Add:
- Hybrid search (vector + keyword)
- Cross-encoder reranking

## Task 5 – RAG Pipeline

Pipeline:

User Query → Query Rewriting → Retrieval → Context Selection → Prompt → LLM Answer

## Task 6 – Evaluation
Measure:
- Recall@k
- qualitative answer grounding

---

# Deliverables

1. Working Python implementation
2. Demonstration queries
3. Evaluation results
4. Architecture explanation

---

# Bonus Challenges

- Multi-collection retrieval
- Metadata filtering
- FastAPI service endpoint
- RAG monitoring metrics
