from math import exp


def shifted_weights(scores: list[float]) -> list[float]:
    peak = max(scores)
    return [exp(s - peak) for s in scores]
