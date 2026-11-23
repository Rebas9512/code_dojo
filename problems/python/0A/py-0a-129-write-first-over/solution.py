def first_over(limit: int) -> int:
    total = 0
    last = 0
    for i in range(1, limit + 2):
        total += i
        if total > limit:
            last = i
            break
    return last
