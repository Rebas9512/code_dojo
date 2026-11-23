def stone_winner(values: list[int]) -> str:
    n = len(values)
    lead = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        gained = 0
        best = None
        for j in range(i, min(i + 3, n)):
            gained += values[j]
            margin = gained - lead[j + 1]
            if best is None or margin > best:
                best = margin
        lead[i] = best
    if lead[0] > 0:
        return "Alice"
    if lead[0] < 0:
        return "Bob"
    return "Tie"
