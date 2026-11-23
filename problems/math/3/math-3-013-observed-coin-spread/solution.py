def coin_spread(flips: list[int]) -> list[float]:
    p = sum(flips)/len(flips)
    variance = sum((x-p)**2 for x in flips)/len(flips)
    return [p, variance]
