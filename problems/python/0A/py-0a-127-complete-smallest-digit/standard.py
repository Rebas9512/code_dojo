def smallest_digit(n: int) -> int:
    best = n % 10
    while n >= 10:
        n //= 10
        digit = n % 10
        if digit < best:
            best = digit
    return best
