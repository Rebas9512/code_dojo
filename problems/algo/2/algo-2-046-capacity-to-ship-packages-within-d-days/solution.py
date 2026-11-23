def groups_needed(values: list[int], limit: int) -> int:
    groups = 1
    load = 0
    for weight in values:
        if load + weight > limit:
            groups += 1
            load = 0
        load += weight
    return groups


def ship_capacity(weights: list[int], days: int) -> int:
    lo, hi = max(weights), sum(weights) + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if groups_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
