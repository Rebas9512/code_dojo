from math import exp


def candidate_probs(scores: list[float]) -> list[float]:
    peak = max(scores)
    weights = [exp(score - peak) for score in scores]
    total = sum(weights)
    return [weight / total for weight in weights]
