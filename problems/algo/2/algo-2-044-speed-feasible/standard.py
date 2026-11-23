def feasible(piles: list[int], speed: int, h: int) -> bool:
    return sum((pile + speed - 1) // speed for pile in piles) <= h
