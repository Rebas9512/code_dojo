def climb(n: int) -> int:
    previous = current = 1
    for step in range(2, n + 1):
        previous, current = current, previous + current
    return current
