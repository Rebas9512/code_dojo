def identity_row(n: int, r: int) -> list[int]:
    return [1 if c == r else 0 for c in range(n)]
