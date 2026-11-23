def groups_needed(values: list[int], limit: int) -> int:
    groups = 1
    load = 0
    for weight in values:
        if load + weight > limit:
            groups += 1
            load = 0
        load += weight
    return groups


def split_min_largest(nums: list[int], k: int) -> int:
    lo, hi = max(nums), sum(nums) + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if groups_needed(nums, mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
