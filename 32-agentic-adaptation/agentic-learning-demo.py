import random
from openai import OpenAI

f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\openai\ne-openai-api-key.txt")
apikey = f.read()
f.close()

client = OpenAI(api_key=apikey)

# -----------------------------
# MEMORY (learned preference)
# -----------------------------
memory = {
    "detailed_score": 0.5,
    "vague_score": 0.5
}

epsilon = 0.2  # exploration


# -----------------------------
# STEP 1: Generate outputs (LLM)
# -----------------------------
def generate_outputs(prompt):

    detailed_prompt = f"""
    Generate a detailed, structured business report with metrics, insights, and bullet points:
    {prompt}
    """

    vague_prompt = f"""
    Give a very short and vague answer:
    {prompt}
    """

    A = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": detailed_prompt}],
        temperature=0.7
    ).choices[0].message.content

    B = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": vague_prompt}],
        temperature=0.7
    ).choices[0].message.content

    return A, B


# -----------------------------
# STEP 2: Choose output
# -----------------------------
def choose_output():
    if random.random() < epsilon:
        return random.choice(["A", "B"])

    if memory["detailed_score"] > memory["vague_score"]:
        return "A"
    return "B"


# -----------------------------
# STEP 3: Human feedback
# -----------------------------
def human_feedback(A, B):
    
    # OPTION 1: Real human input (uncomment below)

    print("\\n--- OUTPUT A ---\\n", A)
    print("\\n--- OUTPUT B ---\\n", B)
    choice = input("Which is better? (A/B): ")
    return choice.upper()
    

    # OPTION 2: Simulated preference (for demo)
    # return "A"  # humans prefer detailed


# -----------------------------
# STEP 4: Reward
# -----------------------------
def get_reward(chosen, preferred):
    return 1.0 if chosen == preferred else 0.0


# -----------------------------
# STEP 5: Learning update
# -----------------------------
def update_memory(choice, reward):
    lr = 0.1

    if choice == "A":
        memory["detailed_score"] = (
            (1 - lr) * memory["detailed_score"] + lr * reward
        )
    else:
        memory["vague_score"] = (
            (1 - lr) * memory["vague_score"] + lr * reward
        )


# -----------------------------
# MAIN LOOP
# -----------------------------
prompt = "Generate a business report for a retail company"

for i in range(3):

    print(f"\n===== Iteration {i+1} =====")

    A, B = generate_outputs(prompt)

    choice = choose_output()
    preferred = human_feedback(A, B)

    reward = get_reward(choice, preferred)

    update_memory(choice, reward)

    print(f"\nAgent chose: {choice}")
    print(f"Human preferred: {preferred}")
    print(f"Reward: {reward}")
    print(f"Scores: {memory}")