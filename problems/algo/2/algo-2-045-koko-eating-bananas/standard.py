def can_finish(piles: list[int], speed: int, h: int) -> bool:
    return sum((pile + speed - 1) // speed for pile in piles) <= h


def min_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles) + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(piles, mid, h):
            hi = mid
        else:
            lo = mid + 1
    return lo
