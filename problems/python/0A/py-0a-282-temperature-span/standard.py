def extremes(values: list[int]) -> tuple[int, int]:
    low = high = values[0]
    for value in values:
        low = min(low, value)
        high = max(high, value)
    return low, high
