def add_bypass(a: list[list[int]]) -> list[list[int]]:
    out = []
    for r in range(len(a)):
        out.append([a[r][c] + (1 if r == c else 0) for c in range(len(a))])
    return out
