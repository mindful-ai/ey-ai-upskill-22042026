"""
FastAPI backend using lifespan (modern approach)
"""

from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from graph.workflow import build_workflow
from tools.database_tool import init_db


# Shared state
workflow = None


# ✅ Lifespan handler (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global workflow

    print("🚀 Starting ABOC API...")

    # Initialize DB + workflow
    init_db()
    workflow = build_workflow()

    yield  # app runs here

    print("🛑 Shutting down ABOC API...")


# Create app with lifespan
app = FastAPI(lifespan=lifespan)


class RequestModel(BaseModel):
    query: str


@app.post("/run")
def run_workflow(request: RequestModel):
    result = workflow.invoke({
        "user_input": request.query
    })

    return {
        "status": "success",
        "result": result
    }


@app.get("/")
def health():
    return {"message": "ABOC API is running"}