
import time

def exact_match(pred, gt):
    return int(pred.strip().lower() == gt.strip().lower())

def similarity(pred, gt):
    p = set(pred.lower().split())
    g = set(gt.lower().split())
    return len(p & g) / max(len(g),1)

def measure_latency(func, *args):
    start = time.time()
    result = func(*args)
    latency = time.time() - start
    return result, latency
