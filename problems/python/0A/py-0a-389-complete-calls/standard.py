def nodes(n: int) -> int:
    if n < 2:
        return 1
    return 1 + nodes(n - 1) + nodes(n - 2)
