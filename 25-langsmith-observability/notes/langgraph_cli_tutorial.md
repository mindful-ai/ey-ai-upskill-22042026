# 🚀 LangGraph CLI Tutorial (Step-by-Step)

## 🧠 Overview
This guide shows how to run your LangGraph project as a CLI app, integrate with LangSmith, and serve it as an API.

---

## 📦 Step 1 — Install CLI

```bash
pip install langgraph-cli
```

---

## 📁 Step 2 — Project Structure

```
project/
│
├── app.py
├── graph.yaml
└── requirements.txt
```

---

## ✂️ Step 3 — app.py

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input: str
    plan: dict
    result: str
    status: str

def build_graph():
    # initialize llm here
    llm = get_llm(...)

    graph = StateGraph(AgentState)

    graph.add_node("planner", create_planner_node(llm))
    graph.add_node("executor", executor_node)
    graph.add_node("validator", create_validator_node(llm))

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "validator")

    graph.add_conditional_edges("validator", route)

    return graph.compile()
```

---

## 📄 Step 4 — graph.yaml

```yaml
graphs:
  agent:
    path: app:build_graph
```

---

## 📦 Step 5 — requirements.txt

```
langchain
langgraph
langchain-openai
langsmith
groq
```

---

## ▶️ Step 6 — Run CLI

```bash
langgraph run agent
```

---

## 🧪 Step 7 — Run with Input

```bash
langgraph run agent --input '{"input": "List all users"}'
```

---

## 🔥 Step 8 — Enable LangSmith

```bash
set LANGCHAIN_TRACING_V2=true
set LANGCHAIN_API_KEY=your_key
```

---

## 🔍 Step 9 — Debug

Check LangSmith UI:
- Planner decisions
- Tool execution
- Validation

---

## 🌐 Step 10 — Serve as API

```bash
langgraph serve
```

---

## Example API Call

```bash
curl -X POST http://localhost:8000/runs   -H "Content-Type: application/json"   -d '{"input": {"input": "List all users"}}'
```

---

## ⚠️ Common Issues

### Missing LLM
Ensure build_graph initializes LLM.

### Wrong input format
```
{"input": "query"}
```

### Wrong path
```
path: app:build_graph
```

---

## 🧠 Key Insight

Script → CLI → API → Production System

---

## 🚀 Next Steps

- Add LangSmith tracing
- Add parallel execution
- Deploy with Docker
