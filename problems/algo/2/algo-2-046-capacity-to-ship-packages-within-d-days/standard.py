def days_needed(weights: list[int], capacity: int) -> int:
    days = 1
    load = 0
    for weight in weights:
        if load + weight > capacity:
            days += 1
            load = 0
        load += weight
    return days


def ship_capacity(weights: list[int], days: int) -> int:
    lo, hi = max(weights), sum(weights) + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
