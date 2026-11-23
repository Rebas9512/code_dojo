def last_weight(stones: list[int]) -> int:
    total = sum(stones)
    half = total // 2
    possible = [True] + [False] * half
    for weight in stones:
        for s in range(half, weight - 1, -1):
            possible[s] = possible[s] or possible[s - weight]
    for s in range(half, -1, -1):
        if possible[s]:
            return total - 2 * s
