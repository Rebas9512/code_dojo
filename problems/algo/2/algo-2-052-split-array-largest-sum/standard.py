def segments_needed(values: list[int], limit: int) -> int:
    segments = 1
    segment_sum = 0
    for value in values:
        if segment_sum + value > limit:
            segments += 1
            segment_sum = 0
        segment_sum += value
    return segments


def split_min_largest(nums: list[int], k: int) -> int:
    lo, hi = max(nums), sum(nums) + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if segments_needed(nums, mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
