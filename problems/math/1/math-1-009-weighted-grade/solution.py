def weighted_grade(scores: list[float], weights: list[float]) -> float:
    parts = [scores[i] * weights[i] for i in range(len(scores))]
    return sum(parts)
