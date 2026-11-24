def stone_winner(values: list[int]) -> str:
    n = len(values)
    next_one = next_two = next_three = 0
    for i in range(n - 1, -1, -1):
        gained = values[i]
        best = gained - next_one
        if i + 1 < n:
            gained += values[i + 1]
            best = max(best, gained - next_two)
        if i + 2 < n:
            gained += values[i + 2]
            best = max(best, gained - next_three)
        next_three = next_two
        next_two = next_one
        next_one = best

    if next_one > 0:
        return "Alice"
    if next_one < 0:
        return "Bob"
    return "Tie"
