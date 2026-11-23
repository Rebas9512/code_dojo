def min_total(rows: list[list[int]]) -> int:
    best = rows[-1].copy()
    for row in reversed(rows[:-1]):
        for j, value in enumerate(row):
            best[j] = value + min(best[j], best[j + 1])
    return best[0]
