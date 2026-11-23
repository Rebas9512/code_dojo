def rotated_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[-1]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
