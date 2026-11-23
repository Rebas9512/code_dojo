def first_over(limit: int) -> int:
    total = 0
    for number in range(1, limit + 2):
        total += number
        if total > limit:
            break
    return number
