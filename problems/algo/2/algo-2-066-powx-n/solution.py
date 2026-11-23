def power(x: float, n: int) -> float:
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n % 2:
            result *= x
        x *= x
        n //= 2
    return result
