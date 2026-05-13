from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Filesystem MCP Server")

# 🔒 Restrict access to this directory
ROOT_DIR = os.path.abspath("./data")

# Ensure root exists
os.makedirs(ROOT_DIR, exist_ok=True)

# -----------------------------
# REQUEST MODEL
# -----------------------------
class FileRequest(BaseModel):
    path: str
    content: str = None


# -----------------------------
# TOOL DEFINITIONS (MCP STYLE)
# -----------------------------
TOOLS = {
    "read_file": {
        "description": "Read contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    "write_file": {
        "description": "Write content to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    "list_files": {
        "description": "List files in directory",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

# -----------------------------
# HELPER (SECURITY)
# -----------------------------
def safe_path(path: str):
    full_path = os.path.abspath(os.path.join(ROOT_DIR, path))
    if not full_path.startswith(ROOT_DIR):
        raise HTTPException(status_code=403, detail="Access denied")
    return full_path


# -----------------------------
# MCP ENDPOINTS
# -----------------------------
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