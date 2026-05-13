# 📁 LangChain File Explorer Agent with MCP (Full Working Example)

This guide shows how to build a **working file explorer agent** using:
- LangChain
- Local MCP Filesystem Server (FastAPI)

---

## 🧠 What This Builds

An AI agent that can:
- 📄 Read files  
- ✍️ Write files  
- 📂 List directory contents  

---

## 🚀 1. Prerequisites

### ✅ Start MCP Server

```bash
uvicorn mcp_filesystem_server:app --reload --port 8000
```

---

### ✅ Install Dependencies

```bash
pip install langchain langchain-openai requests
```

---

## 📦 2. Full Working Code

Save as `file_agent.py`

```python
import requests
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

# -----------------------------
# CONFIG
# -----------------------------
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
MCP_BASE_URL = "http://127.0.0.1:8000"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)

# -----------------------------
# MCP TOOL WRAPPERS
# -----------------------------

def list_files(_=""):
    res = requests.post(f"{MCP_BASE_URL}/tools/list_files")
    return str(res.json())


def read_file(path):
    res = requests.post(
        f"{MCP_BASE_URL}/tools/read_file",
        json={"path": path}
    )
    return res.json().get("content", "Error reading file")


def write_file(input_str):
    try:
        path, content = input_str.split("|", 1)
        res = requests.post(
            f"{MCP_BASE_URL}/tools/write_file",
            json={"path": path.strip(), "content": content.strip()}
        )
        return str(res.json())
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL DEFINITIONS
# -----------------------------
tools = [
    Tool(
        name="List Files",
        func=list_files,
        description="List all files in the directory"
    ),
    Tool(
        name="Read File",
        func=read_file,
        description="Read file content. Input should be a filename"
    ),
    Tool(
        name="Write File",
        func=write_file,
        description="Write to a file. Input format: filename|content"
    ),
]

# -----------------------------
# AGENT
# -----------------------------
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# -----------------------------
# RUN LOOP
# -----------------------------
if __name__ == "__main__":
    print("\n📁 MCP File Explorer Agent Ready!\n")

    while True:
        query = input("🧑 You: ")

        if query.lower() in ["exit", "quit"]:
            break

        response = agent.run(query)
        print(f"\n🤖 Agent: {response}\n")
```

---

## ▶️ 3. Run the Agent

```bash
python file_agent.py
```

---

## 🧪 4. Example Prompts

```
List all files
Create a file called test.txt with content Hello MCP world
Read test.txt
Summarize the contents of test.txt
```

---

## 🔥 How It Works

```
User → LangChain Agent → LLM → Tool Decision
                        ↓
                  MCP Server
                        ↓
                File System Action
                        ↓
                Response → LLM → User
```

---

## ⚡ Key Takeaways

- This is a **true MCP-style integration**
- Agent dynamically selects tools
- MCP server executes real-world actions
- Fully extensible architecture

---

## 🚀 Next Steps

- Add RAG over files  
- Add Browser MCP  
- Add Database MCP  
- Move to LangGraph for advanced orchestration  

