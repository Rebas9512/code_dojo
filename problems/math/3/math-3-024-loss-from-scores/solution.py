from math import exp, log


def score_loss(scores: list[float], label: int) -> float:
    peak = max(scores)
    shifted = [s-peak for s in scores]
    total = sum(exp(s) for s in shifted)
    return log(total) - shifted[label]
