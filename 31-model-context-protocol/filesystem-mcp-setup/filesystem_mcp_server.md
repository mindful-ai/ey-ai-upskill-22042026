# 📁 Local Filesystem MCP Server (FastAPI)

This guide helps you run a **working local MCP-style filesystem server**.

---

## 🚀 Features

- `/tools` → list tools  
- `/tools/read_file` → read file  
- `/tools/write_file` → write file  
- `/tools/list_files` → list files  
- 🔒 Restricted to a safe root directory  

---

## 📦 1. Install Dependencies

```bash
pip install fastapi uvicorn
```

---

## 🧠 2. Server Code

Save as `mcp_filesystem_server.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Filesystem MCP Server")

ROOT_DIR = os.path.abspath("./data")
os.makedirs(ROOT_DIR, exist_ok=True)

class FileRequest(BaseModel):
    path: str
    content: str = None

TOOLS = {
    "read_file": {
        "description": "Read contents of a file"
    },
    "write_file": {
        "description": "Write content to a file"
    },
    "list_files": {
        "description": "List files"
    }
}

def safe_path(path: str):
    full_path = os.path.abspath(os.path.join(ROOT_DIR, path))
    if not full_path.startswith(ROOT_DIR):
        raise HTTPException(status_code=403, detail="Access denied")
    return full_path

@app.get("/tools")
def list_tools():
    return TOOLS

@app.post("/tools/read_file")
def read_file(req: FileRequest):
    file_path = safe_path(req.path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}

@app.post("/tools/write_file")
def write_file(req: FileRequest):
    file_path = safe_path(req.path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(req.content)
    return {"status": "written"}

@app.post("/tools/list_files")
def list_files():
    return {"files": os.listdir(ROOT_DIR)}
```

---

## ▶️ 3. Run Server

```bash
uvicorn mcp_filesystem_server:app --reload --port 8000
```

---

## 🧪 4. Test

### Write file
```bash
curl -X POST http://127.0.0.1:8000/tools/write_file \
-H "Content-Type: application/json" \
-d "{\"path\": \"notes.txt\", \"content\": \"Hello MCP\"}"
```

### Read file
```bash
curl -X POST http://127.0.0.1:8000/tools/read_file \
-H "Content-Type: application/json" \
-d "{\"path\": \"notes.txt\"}"
```

### List files
```bash
curl -X POST http://127.0.0.1:8000/tools/list_files
```

---

## 🔗 5. LangChain Integration

```python
import requests
from langchain.tools import Tool

def read_file_tool(filename):
    res = requests.post(
        "http://127.0.0.1:8000/tools/read_file",
        json={"path": filename}
    )
    return res.json()["content"]

tool = Tool(
    name="Read File",
    func=read_file_tool,
    description="Read file contents"
)
```

---

## ⚡ Summary

This is a **simple, reliable MCP-style server**:
- No broken packages  
- Fully extensible  
- Works immediately  
