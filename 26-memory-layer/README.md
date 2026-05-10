Start with dbagent-structured-tools.py

Add memory layer:

### Short-term memory (session-level)
Remembers:
    last user added
    previous question
Purpose:
    👉 multi-turn interaction
    (“Add user… now list them” without repeating context)

### Long-term memory (persistent)
Remembers:
    past operations
    frequently accessed users
Purpose:
    👉 personalization + recall across runs