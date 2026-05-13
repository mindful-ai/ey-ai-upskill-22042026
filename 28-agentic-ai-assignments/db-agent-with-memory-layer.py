from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import sqlite3

# ============================================================
# DB SETUP
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

    # 🔥 Long-term memory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
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
# TOOLS (STRUCTURED)
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a user to the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, name, authenticated) VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()

        # 🔥 Save last user to long-term memory
        cursor.execute(
            "INSERT OR REPLACE INTO memory VALUES (?, ?)",
            ("last_user", f"{name}:{user_id}")
        )
        conn.commit()

        return f"User {name} added with ID {user_id}"

    except Exception as e:
        return f"ERROR: {str(e)}"

    finally:
        conn.close()


@tool
def list_users() -> str:
    """List all users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, authenticated FROM users")
    rows = cursor.fetchall()
    conn.close()

    return "\n".join([str(r) for r in rows]) or "No users found"


@tool
def save_memory(key: str, value: str) -> str:
    """Store long-term memory"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO memory VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()

    return "Memory saved"


@tool
def get_memory(key: str) -> str:
    """Retrieve long-term memory"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else "No memory found"


# ============================================================
# SHORT-TERM MEMORY (SESSION)
# ============================================================

chat_history = []


# ============================================================
# MAIN
# ============================================================

with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt") as f:
    groq_api_key = f.read().strip()


def run_agent(agent, user_input):
    global chat_history

    # Add user message
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = agent.invoke({
        "messages": chat_history
    })

    assistant_msg = response["messages"][-1]

    # Save assistant response
    chat_history.append({
        "role": "assistant",
        "content": assistant_msg.content
    })

    return assistant_msg.content


if __name__ == "__main__":

    setup_db()
    seed_data()

    llm = ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

    tools = [add_user, list_users, save_memory, get_memory]

    prompt = """You are a user management assistant.

Capabilities:
- Add users
- List users
- Store memory using save_memory
- Retrieve memory using get_memory

Rules:
- Always use tools
- Return tool output EXACTLY
"""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt
    )

    # ============================================================
    # TEST RUNS
    # ============================================================

    print("\n=== ADD USER ===")
    print(run_agent(agent, "Add a user named Purushotham with id ML501"))

    print("\n=== FOLLOW-UP (SHORT-TERM MEMORY) ===")
    print(run_agent(agent, "Now list all users"))

    print("\n=== LONG-TERM MEMORY ===")
    print(run_agent(agent, "Who was the last user added?"))