def min_end(n: int, x: int) -> int:
    remaining = n - 1
    value = x
    place = 1
    while remaining:
        if (x & place) == 0:
            if remaining & 1:
                value |= place
            remaining >>= 1
        place <<= 1
    return value
