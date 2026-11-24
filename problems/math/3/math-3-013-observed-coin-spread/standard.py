def coin_spread(flips: list[int]) -> list[float]:
    p = sum(flips) / len(flips)
    return [p, p * (1 - p)]
