
import json
from evals.metrics import exact_match, similarity, measure_latency
from evals.model import model_call
from evals.judge import judge

def evaluate_prompt(prompt, dataset):
    results = []
    for item in dataset:
        pred, latency = measure_latency(model_call, prompt, item["question"])
        gt = item["answer"]

        results.append({
            "question": item["question"],
            "prediction": pred,
            "ground_truth": gt,
            "exact_match": exact_match(pred, gt),
            "similarity": similarity(pred, gt),
            "judge_score": judge(pred, gt),
            "latency": latency
        })
    return results

def summarize(results):
    n = len(results)
    return {
        "accuracy": sum(r["exact_match"] for r in results)/n,
        "similarity": sum(r["similarity"] for r in results)/n,
        "judge_score": sum(r["judge_score"] for r in results)/n,
        "avg_latency": sum(r["latency"] for r in results)/n
    }

def run_all():
    with open("datasets/dataset.json") as f:
        dataset = json.load(f)

    with open("prompts/prompts.json") as f:
        prompts = json.load(f)

    for name, prompt in prompts.items():
        print(f"\nEvaluating {name}...")
        results = evaluate_prompt(prompt, dataset)
        summary = summarize(results)
        print(summary)
