def smallest_digit(n: int) -> int:
    best = n % 10
    while n > 0:
        digit = n % 10
        if ____:
            best = digit
        n = n // 10
    return best
