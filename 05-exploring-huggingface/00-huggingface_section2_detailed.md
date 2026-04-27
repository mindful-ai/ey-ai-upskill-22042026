# 📘 Section 2 — Setup & First Steps (Detailed Workshop Handout)

---

# 🧩 2.1 Installation & Environment Setup

## 🎯 Goal
Set up a fully functional environment to run Hugging Face models locally using CPU or GPU, and connect to the Hugging Face Hub.

---

## 🪜 Step 1 — Install Required Libraries

### Using pip (Recommended)
```bash
pip install transformers datasets accelerate
```

### What gets installed?
- transformers → model APIs
- datasets → data handling
- accelerate → scaling & hardware abstraction

---

## 🪜 Step 2 — Verify Installation

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
print(classifier("Setup successful!"))
```

### ✅ Expected Behavior
- Downloads a pretrained model
- Runs inference
- Outputs sentiment

---

## 🪜 Step 3 — CPU vs GPU Setup

### 🔹 CPU (Default)
- No setup required
- Suitable for small workloads

### 🔹 GPU (Recommended for speed)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Verify GPU:
```python
import torch
print(torch.cuda.is_available())
```

---

## 🪜 Step 4 — Device Selection

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis", device=0)  # GPU
classifier = pipeline("sentiment-analysis", device=-1) # CPU
```

---

## 🪜 Step 5 — Hugging Face Authentication

### Why?
- Access private models
- Push models
- Use APIs

```bash
huggingface-cli login
huggingface-cli whoami
```

---

# 🧩 2.2 First Model Inference

## 🎯 Goal
Use pretrained models via Pipeline API

---

## 🪜 Step 1 — Import Pipeline
```python
from transformers import pipeline
```

---

## 🪜 Step 2 — Text Classification
```python
classifier = pipeline("sentiment-analysis")
print(classifier("I love Hugging Face!"))
```

### Explanation
- Automatically loads model + tokenizer
- Performs inference

---

## 🪜 Step 3 — Named Entity Recognition (NER)
```python
ner = pipeline("ner", aggregation_strategy="simple")
print(ner("Elon Musk founded SpaceX in California"))
```

### Explanation
Identifies:
- Person
- Organization
- Location

---

## 🪜 Step 4 — Question Answering
```python
from transformers import pipeline

qa = pipeline(
    task="text-generation",
    model="google/flan-t5-base"
    # model="distilgpt2"
)

context = "Hugging Face builds AI tools."
question = "What does Hugging Face build?"

prompt = f"Answer the question: {question} Context: {context}"

result = qa(
    prompt,
    max_new_tokens=30,
    do_sample=False
)

print(result[0]["generated_text"])
```

---

# 🧩 2.3 Understanding Pipeline Internals

## 🎯 Goal
Understand what happens inside a pipeline

---

## 🔄 Flow
Input → Tokenizer → Tokens → Model → Logits → Output

---

## 🪜 Step 1 — Tokenization

### Definition
Tokenization converts text into numbers (tokens)

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
print(tokenizer("Hugging Face is amazing!"))
```

---

## 🪜 Step 2 — Model Loading

### What happens?
- Downloads model from Hub (first time)
- Stores in cache

Cache location:
```
~/.cache/huggingface/
```

---

## 🪜 Step 3 — Model Inference

- Tokens → embeddings
- Passed through neural network
- Produces logits (raw scores)

---

## 🪜 Step 4 — Post-processing

- Converts logits → labels
- Makes output human-readable

---

## 🪜 Step 5 — Device Placement

### CPU
```python
pipeline("sentiment-analysis", device=-1)
```

### GPU
```python
pipeline("sentiment-analysis", device=0)
```

---

# 🧪 Practice Tasks

## Task 1
Try different pipelines:
- ner
- text-generation
- translation

## Task 2
Print tokens and inspect outputs

## Task 3
Compare CPU vs GPU speed

---

# 🚀 Mini Challenge — Smart QA Tool

## Objective
Build a CLI-based question answering system

---

## ✅ Solution

```python
from transformers import pipeline

qa = pipeline("question-answering")

while True:
    context = input("\nEnter context (or type 'exit'): ")
    if context.lower() == "exit":
        break

    question = input("Enter question: ")

    result = qa(question=question, context=context)

    print("\nAnswer:", result['answer'])
    print("Confidence:", result['score'])
```

---

# ✅ Outcome

By completing this section, learners can:
- Install Hugging Face ecosystem
- Run pretrained models
- Understand pipeline internals
- Build simple NLP applications
