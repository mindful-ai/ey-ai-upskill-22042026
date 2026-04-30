
# Mock LLM-as-judge

def judge(pred, gt):
    if pred.lower() == gt.lower():
        return 5
    if gt.lower() in pred.lower():
        return 4
    return 2
