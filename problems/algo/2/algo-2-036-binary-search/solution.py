def lower_bound(nums: list[int], x: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search(nums: list[int], target: int) -> int:
    pos = lower_bound(nums, target)
    if pos < len(nums) and nums[pos] == target:
        return pos
    return -1
