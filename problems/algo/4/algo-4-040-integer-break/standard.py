def break_product(n: int) -> int:
    best = [0] * (n + 1)
    for total in range(2, n + 1):
        for first in range(1, total):
            rest = total - first
            best[total] = max(best[total], first * rest, first * best[rest])
    return best[n]
