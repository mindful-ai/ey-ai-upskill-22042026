
import json
from evals.metrics import exact_match

def dummy_model(prompt, question):
    return "A metabolic disorder" if "diabetes" in question else "Blood pressure"

def run_evaluation():
    with open("datasets/sample_dataset.json") as f:
        data = json.load(f)

    score = 0
    for item in data:
        pred = dummy_model("", item["question"])
        score += exact_match(pred, item["answer"])

    print("Accuracy:", score / len(data))
