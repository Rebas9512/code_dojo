from math import exp


def candidate_probs(scores: list[float]) -> list[float]:
    peak = max(scores)
    weights = [exp(s - peak) for s in scores]
    total = sum(weights)
    return [w/total for w in weights]
