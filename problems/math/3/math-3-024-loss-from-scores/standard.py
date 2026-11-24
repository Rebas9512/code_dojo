from math import exp, log


def score_loss(scores: list[float], label: int) -> float:
    peak = max(scores)
    total = sum(exp(score - peak) for score in scores)
    return log(total) - (scores[label] - peak)
