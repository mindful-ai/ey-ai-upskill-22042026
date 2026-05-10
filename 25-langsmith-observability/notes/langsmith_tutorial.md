# 🧠 LangSmith Tutorial: Observability for Agentic AI Systems

---

## 📌 What is LangSmith?

LangSmith is an observability and debugging platform for LLM applications. It allows developers to trace, inspect, evaluate, and debug AI workflows built using LangChain, LangGraph, and related frameworks.

---

## 🚀 Why Use LangSmith?

Traditional AI debugging:
- Print statements
- Hard to trace LLM reasoning
- No visibility into intermediate steps

LangSmith provides:
- ✅ Full execution traces
- ✅ Node-level visibility (LangGraph)
- ✅ Prompt + response inspection
- ✅ Debugging of tool calls
- ✅ Evaluation and monitoring

---

## 🏗️ Key Features

### 🔍 Tracing
- Track every LLM call
- See inputs, outputs, latency

### 🧠 Agent Debugging
- Inspect planner decisions
- View tool execution steps

### 📊 Evaluation
- Measure accuracy
- Compare model outputs

### 🧪 Experimentation
- Test prompt variations
- Compare runs

---

## ⚙️ Setup Guide

### Step 1: Install

```bash
pip install langsmith
pip install --upgrade "langgraph-cli[inmem]"
```
The LangGraph CLI provides a local development server (also called Agent Server) that connects your agent to Studio.

You'll need:

A LangSmith account: Sign up (for free) or log in at smith.langchain.com.
A LangSmith API key: Follow the Create an API key guide.
---

### Step 2: Set Environment Variables

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_api_key
export LANGCHAIN_PROJECT=langgraph-demo
```

(Use `set` instead of `export` on Windows)

---

## 🔧 Basic Usage

No code change required for basic tracing.

Example:

```python
response = llm.invoke("Hello")
```

➡️ Automatically logged in LangSmith

---

## 🧩 Using with LangGraph

Each node becomes a trace span.

Example:

```python
from langsmith import traceable

@traceable(name="planner_node")
def planner_node(state):
    ...
```

---

## 🔍 Debugging Workflow

### Step 1: Run your app

### Step 2: Open LangSmith UI
https://smith.langchain.com

---

### Step 3: Inspect traces

You will see:
- Input
- Output
- Intermediate steps

---

## 🧠 Debugging Planner Errors

Example issue:

User: "Find user ML001"

Planner output:
```json
{"action": "list_users"}
```

Fix:
- Improve prompt
- Add examples

---

## 🔧 Improve Prompt

```text
Examples:
"Find user ML001" → get_user_by_id(user_id="ML001")
```

---

## 📊 Debugging Tools

### Planner
- Wrong tool?
- Missing arguments?

### Executor
- Tool failure?
- DB issues?

### Validator
- Always VALID?
- Infinite loop?

---

## 🏷️ Advanced Tracing

```python
@traceable(name="executor_node", tags=["executor", "tool"])
```

---

## 📈 Best Practices

- Use structured tools
- Add examples in prompts
- Validate outputs
- Monitor traces regularly

---

## 🔥 Real Use Cases

- Debug agent workflows
- Monitor production AI systems
- Compare model performance
- Optimize prompts

---

## 🧠 Key Insight

LangSmith enables:

👉 Observability-driven AI development

---

## 🚀 Next Steps

- Add evaluation pipelines
- Integrate with LangGraph
- Monitor production systems

---

## 🎯 Final Takeaway

LangSmith transforms AI development from:

❌ Guess-based debugging  
➡️  
✅ Data-driven debugging

---

