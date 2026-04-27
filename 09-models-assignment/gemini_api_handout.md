# 🚀 Gemini API Practice Handout (2026)

## 🧠 Overview
This handout introduces students to using Google Gemini API for building simple AI applications.

You will learn:
- How to get an API key
- How to install required libraries
- How to generate text
- How to build a simple chatbot

---

## ✅ Step 1: Get API Key

1. Visit: https://aistudio.google.com/app/apikey  
2. Generate API Key  
3. Save it securely  

---

## ✅ Step 2: Install Library

```bash
pip install google-generativeai
```

---

## ✅ Step 3: Basic Example

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Explain transformers simply")

print(response.text)
```

---

## 💬 Step 4: Build a Chatbot

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

def chat():
    print("Gemini Chatbot (type 'exit' to quit)")

    chat_session = model.start_chat(history=[])

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = chat_session.send_message(user_input)
        print("AI:", response.text)

chat()
```

---

## 🔥 Recommended Models

- gemini-1.5-flash (fast + default)
- gemini-1.5-pro (higher quality)
- gemini-2.0-flash (latest fast model)

---

## ⚠️ Common Errors

### API Key Error
- Ensure API key is correct

### Model Name Error
- Use exact model names

### Rate Limits
- Retry after some time

---

## 🎯 Practice Exercises

1. Modify chatbot to:
   - Act as a physics teacher
   - Act as a coding assistant

2. Add:
   - Chat history saving
   - Different system prompts

3. Experiment with:
   - Different models
   - Temperature settings

---

## 🚀 Next Steps

- Build a web app using FastAPI
- Add streaming responses
- Combine multiple AI providers

---

Happy Learning! 🎓
