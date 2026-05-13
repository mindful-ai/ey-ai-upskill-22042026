# ==============================
# 1. INSTALL (run once)
# ==============================
# pip install crewai openai

# ==============================
# 2. IMPORTS
# ==============================
import sqlite3
import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# ==============================
# 3. SET OPENAI API KEY
# ==============================
f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\openai\ne-openai-api-key.txt")
apikey = f.read()
f.close()
os.environ["OPENAI_API_KEY"] = apikey

# ==============================
# 4. LLM (OPENAI)
# ==============================
llm = LLM(
    model="gpt-4o-mini",  # fast + cheap + stable for demos
    temperature=0
)

# ==============================
# 5. DATABASE SETUP
# ==============================
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ==============================
# 6. CRUD TOOLS
# ==============================

@tool("Add User")
def add_user(name: str, email: str) -> str:
    """Add a new user to the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()
    return f"User {name} added successfully"


@tool("Get Users")
def get_users() -> str:
    """Fetch all users from the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()
    return str(rows)


@tool("Update User")
def update_user(user_id: int, name: str, email: str) -> str:
    """Update a user's name and email by ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name=?, email=? WHERE id=?",
        (name, email, user_id)
    )

    conn.commit()
    conn.close()
    return f"User {user_id} updated"


@tool("Delete User")
def delete_user(user_id: int) -> str:
    """Delete a user by ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()
    return f"User {user_id} deleted"


# ==============================
# 7. AGENT
# ==============================
db_agent = Agent(
    role="Database Manager",
    goal="Perform CRUD operations on a SQLite database based on instructions",
    backstory="You are an expert database assistant who manages user records accurately.",
    tools=[add_user, get_users, update_user, delete_user],
    llm=llm,
    verbose=True
)

# ==============================
# 8. TASK
# ==============================
task = Task(
    description="""
    Execute the following steps:

    1. Add user: John Doe, john@example.com
    2. Add user: Alice, alice@example.com
    3. Show all users
    4. Update user with id 1 to name: Johnny Doe and email: johnny@example.com
    5. Delete user with id 2
    6. Show all users again
    """,
    expected_output="Final list of users after all operations",
    agent=db_agent
)

# ==============================
# 9. CREW
# ==============================
crew = Crew(
    agents=[db_agent],
    tasks=[task],
    verbose=True
)

# ==============================
# 10. RUN
# ==============================
if __name__ == "__main__":
    result = crew.kickoff()
    print("\nFINAL RESULT:\n", result)