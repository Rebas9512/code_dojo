def weighted_grade(scores: list[float], weights: list[float]) -> float:
    total = 0.0
    for i in range(len(scores)):
        total += scores[i] * weights[i]
    return total
