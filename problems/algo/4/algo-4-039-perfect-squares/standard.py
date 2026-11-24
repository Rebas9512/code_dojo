def least_squares(n: int) -> int:
    squares = []
    base = 1
    while base * base <= n:
        squares.append(base * base)
        base += 1
    best = list(range(n + 1))
    for total in range(1, n + 1):
        for square in squares:
            if square > total:
                break
            best[total] = min(best[total], 1 + best[total - square])
    return best[n]
