from langchain_openai import ChatOpenAI
from langchain.tools import tool
import sqlite3
import json
import re

# ============================================================
# DATABASE SETUP
# ============================================================

def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        authenticated INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    users = [
        ("ML001", "Raj", 1),
        ("ML002", "Ram", 0),
        ("ML003", "Sham", 1)
    ]

    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

    conn.commit()
    conn.close()

# ============================================================
# TOOLS (All tools should have docstrings explaining their purpose and inputs/outputs)
# Langchain expects tool functions to be decorated with @tool and to have clear type annotations.
# ============================================================


@tool
def add_user(name: str, user_id: str) -> str:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()
        return f"SUCCESS: Added {name}"
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        conn.close()


@tool
def list_users() -> str:
    """Return all users in the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


@tool
def get_user_by_id(user_id: str) -> str:
    """Retrieve a user by their ID"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return json.dumps(row)


@tool
def update_user_auth(user_id: str, authenticated: int) -> str:
    """Update authentication status of a user (0 or 1)"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET authenticated=? WHERE id=?",
        (authenticated, user_id)
    )
    conn.commit()
    conn.close()
    return "SUCCESS: Updated authentication"


@tool
def delete_user(user_id: str) -> str:
    """Delete a user from the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "SUCCESS: User deleted"


@tool
def count_users() -> str:
    """Return total number of users in the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search users by name (partial match supported)"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)

# ============================================================
# LLM
# ============================================================

def get_llm(api_key):
    return ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

# ============================================================
# PLANNER
# ============================================================

def planner(llm, user_input):
    # -------- Logic for planner to generate a plan (action + action inputs) based on user input and available tools
    print("[INFO] Invoking planner with user input:", user_input)
    prompt=f"""
You are a planner that generates a plan to achieve a user's request using available tools.

Available tools:
- add_user(name, user_id): Add a new user to the database
- list_users(): List all users in the database   
- get_user_by_id(user_id): Retrieve a user by their ID
- update_user_auth(user_id, authenticated): Update authentication status of a user (0 or 1)
- delete_user(user_id): Delete a user from the database 
- count_users(): Return total number of users in the database
- search_user_by_name(name): Search users by name (partial match supported)

User request: {user_input}

Return ONLY JSON:
{{
    "action": "tool_name",
    "args": {{...}}
}}
    """
    response = llm.invoke(prompt)
    # Safely extract text from the LLM response
    raw = None
    if hasattr(response, "content"):
        raw = response.content
    elif isinstance(response, str):
        raw = response
    else:
        raw = str(response)

    raw = (raw or "").strip()
    print("[INFO] Planner raw response:", raw)

    if not raw:
        raise ValueError("Planner returned empty response; cannot parse JSON plan.")

    # Try parsing direct JSON, otherwise attempt to recover a JSON object embedded in text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"(\{.*\})", raw, re.DOTALL)
        if m:
            candidate = m.group(1)
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    raise ValueError(
        "Planner returned non-JSON response. Raw response:\n"
        f"{raw}\n\n"
        "Consider adjusting the prompt to return strict JSON or inspect the LLM output above."
    )

# ============================================================
# EXECUTOR
# ============================================================

# Tool Registry
TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
    "get_user_by_id": get_user_by_id,
    "update_user_auth": update_user_auth,
    "delete_user": delete_user,
    "count_users": count_users,
    "search_user_by_name": search_user_by_name,
}

def executor(plan):
    # -------- Logic for executor
    print("[INFO] Executing plan:", plan)
    action = plan.get("action")
    args = plan.get("args", {})
    if action not in TOOLS:
        return f"ERROR: Unknown action '{action}'"

    tool_fn = TOOLS[action]

    # If the tool is a LangChain Tool wrapper it may expose `.invoke` or `.run`.
    # Prefer calling the function directly with kwargs/args when possible.
    try:
        if isinstance(args, dict):
            # If the tool is a wrapper object with `invoke`, call the underlying callable if available
            if hasattr(tool_fn, "invoke") and not callable(tool_fn):
                return tool_fn.invoke(args)
            return tool_fn(**args)
        elif args is None:
            return tool_fn()
        else:
            if isinstance(args, (list, tuple)):
                return tool_fn(*args)
            return tool_fn(args)
    except TypeError as e:
        return f"ERROR: tool call failed: {e}"

# ============================================================
# VALIDATOR
# ============================================================

def validator(llm, user_input, result):
    # ------- Logic for valdator
    print("[INFO] Validating result:", result)
    prompt = f"""
You are a validator that checks if the result of an action correctly fulfills the user's request.

User request: {user_input}
Result: {result}

Answer with "VALID" if the result fulfills the request, otherwise answer with "INVALID".
    """
    return llm.invoke(prompt).content.strip()

# ============================================================
# ORCHESTRATOR
# ============================================================

def run_agent(llm, user_input, retries=1):

    for _ in range(retries):
        # ---------- Demo: Logic for orchestrating the planner, executor and validator
        print(f"\n[ORCHESTRATOR] Attempt {_+1} for user input: {user_input}")
        plan = planner(llm, user_input)
        print("[ORCHESTRATOR] Generated plan:", plan)
        result = executor(plan)
        print("[ORCHESTRATOR] Execution result:", result)
        status = validator(llm, user_input, result)
        print(f"[ORCHESTRATOR] Status: {status}")
        if status.strip() == "VALID":
            return result
        else:
            return "FAILED"

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    setup_db()
    seed_data()

    with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt") as f:
        api_key = f.read().strip()

    llm = get_llm(api_key)

    print("\n=== ADD USER ===")
    print(run_agent(llm, "Add user named Alice with id ML200"))

    print("\n=== SEARCH USER ===")
    print(run_agent(llm, "Find user with name Raj"))

    print("\n=== COUNT USERS ===")
    print(run_agent(llm, "How many users exist?"))

    print("\n=== UPDATE USER ===")
    print(run_agent(llm, "Set authentication of ML002 to 1"))

    print("\n=== DELETE USER ===")
    print(run_agent(llm, "Delete user ML003"))

    print("\n=== LIST USERS ===")
    print(run_agent(llm, "List all users"))