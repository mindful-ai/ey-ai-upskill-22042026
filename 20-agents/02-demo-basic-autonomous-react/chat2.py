# main.py

from groq import Groq
from agent_tools import handle_tool_call

# ------ Initialize OpenAI client here ------

# Read the key from the file
with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt", "r") as f:
    api_key = f.read().strip()

# Initialize the Groq client
client = Groq(api_key=api_key)

# Select a model
MODEL = "llama-3.1-8b-instant"

# ----------------------------
# CHAT FUNCTION
# ----------------------------
def chat():
    print("Welcome to the ChatBot! Type 'exit' or 'quit' to end the chat.\n")
    print("ChatBot: Hello! How can I assist you today?")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:

        # ----------------------------
        # USER INPUT
        # ----------------------------
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        # ----------------------------
        # REACT LOOP
        # ----------------------------
        react_messages = messages.copy()

        # ------ Insert your ReAct prompt here ------

        react_messages.append({
            "role": "system",
            "content": """
You are a ReAct style AI assistant.

Follow STRICTLY:

Thought: Reasoning
Action: one of [get_time, get_date, get_day, get_weather]
Action Input: input or NONE
Observation: tool result
Final Answer: final answer to the user

Rules:
- Use tools when needed
- For weather pass city name as input
- If no tool is needed, directly give the final answer

"""
        })

        # --------------------------------------------------

        # react_messages.append({
        #     "role": "system",
        #     "content": """You are a ReAct-style AI assistant."""
        # })

        final_answer = None
        reasoning_steps = []

        for step in range(4):

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=react_messages,
                    temperature=0
                )

                reply = response.choices[0].message.content.strip()
                #print(f"\n[LLM Reply {step}]\n", reply)

                react_messages.append({"role": "assistant", "content": reply})
                reasoning_steps.append(reply)

                # ----------------------------
                # TOOL EXECUTION
                # ----------------------------
                observation = handle_tool_call(reply, step)

                if observation:
                    react_messages.append({
                        "role": "user",
                        "content": observation
                    })
                    continue

            except Exception as e:
                print(f"Error during LLM call: {e}")
                break
        else:

            # ----------------------------
            # FINAL ANSWER FIRST
            # ----------------------------
            if "Final Answer:" in reply:
                final_answer = reply.split("Final Answer:")[-1].strip()

        # ----------------------------
        # PRINT CLEAN OUTPUT
        # ----------------------------
        print("\n--- ReAct Reasoning ---")

        for i, step in enumerate(reasoning_steps, 1):
            print(f"\nStep {i}:\n{step}")

        if final_answer:
            print(f"\nChatBot: {final_answer}")
            messages.append({"role": "assistant", "content": final_answer})
        else:
            print("\nChatBot: Sorry, I couldn't complete the reasoning.")


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    chat()