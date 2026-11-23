def routes(n: int) -> int:
    if n <= 1:
        return 1
    return routes(n - 1) + routes(n - 2)
