def feature_scores(rows: list[list[int]], weights: list[int]) -> list[int]:
    scores = []
    for row in rows:
        scores.append(sum(row[i] * weights[i] for i in range(len(row))))
    return scores
