def feature_scores(rows: list[list[int]], weights: list[int]) -> list[int]:
    out = []
    for row in rows:
        out.append(sum(row[i] * weights[i] for i in range(len(row))))
    return out
