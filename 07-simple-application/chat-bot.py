# Use Groq
from groq import Groq

# Read the key from the file
f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt", "r")
api_key = f.read().strip()
f.close()

# Intialize the Groq client
client = Groq(api_key=api_key)

# Select a model
MODEL = "llama-3.1-8b-instant"


### VIBE CODED USING GITHUB COPILOT
# Create a function to generate responses from the model

def chat():

    # Welcome message
    print("Welcome to the Groq Chat Bot! Type 'exit' to quit.")

    # Create a messages queue and initialize with a system message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    # Chat loop
    while True:

        # user input
        user_input = input("You: ")

        # check for the exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        # inject the user query into messages
        messages.append({"role": "user", "content": user_input})

        try:

            # invoke the LLM
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
    
            # extract the LLM response
            ai_reply = response.choices[0].message.content
    
            # Update messages
            messages.append({"role": "assistant", "content": ai_reply})
    
            # OUtput the response to the user
            print(f"Chatbot: {ai_reply}")

        except:

            # exception logic
            print("An error occurred while generating the response.")

### DEVELOPED FROM SCRATCH WITHOUT COPILOT
def chat2():

    # Welcome message
    print("Welcome to the chatbot! Type 'exit' to end the chat. \n")
    print("Chatbot: Hello! How can I assit you today?")
    
    # Create a messages queue and initialize with a system message
    messages = [
        {"role": "system", "content":"You are a helpful assistant with a respectful tone"}
    ]

    # Chat loop
    while True:

        # user input
        user_input = input("You: ")

        # check for the exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Good bye!")
            break

        # inject the user query into messages
        messages.append({"role":"user", "context": user_input})

        try:
   
            # invoke the LLM
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
    
            # extract the LLM response
            ai_reply = response.choices[0].message.content

            # Update messages
            message.append({"role":"assistant", "content": ai_reply})
    
            # OUtput the response to the user
            print(f"Chatbot: {ai_reply}")

        except:

            # exception logic
            print("An error occured")
    

# Launch the model
if __name__ == "__main__":
    chat()