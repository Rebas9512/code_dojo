def count_from(n: int) -> list[int]:
    if n == 0:
        return []
    [n] + count_from(n - 1)
