def identity_board(n: int) -> list[list[int]]:
    rows = []
    for r in range(n):
        rows.append([1 if r == c else 0 for c in range(n)])
    return rows
