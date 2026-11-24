def min_total(rows: list[list[int]]) -> int:
    best = rows[-1].copy()
    for i in range(len(rows) - 2, -1, -1):
        for j, value in enumerate(rows[i]):
            best[j] = value + min(best[j], best[j + 1])
    return best[0]
