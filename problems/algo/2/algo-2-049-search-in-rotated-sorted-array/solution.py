def find_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[-1]:
            lo = mid + 1
        else:
            hi = mid
    start = lo
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        actual = (start + mid) % len(nums)
        if nums[actual] < target:
            lo = mid + 1
        else:
            hi = mid
    actual = (start + lo) % len(nums)
    return actual if lo < len(nums) and nums[actual] == target else -1
