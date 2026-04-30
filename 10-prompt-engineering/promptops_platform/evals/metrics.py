
def exact_match(pred, gt):
    return int(pred.strip().lower() == gt.strip().lower())

def simple_similarity(pred, gt):
    return len(set(pred.split()) & set(gt.split())) / max(len(gt.split()),1)
