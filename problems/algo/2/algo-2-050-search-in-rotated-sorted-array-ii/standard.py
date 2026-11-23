def has_rotated(nums: list[int], target: int) -> bool:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid]:
            lo += 1
        elif nums[lo] < nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid
            else:
                lo = mid + 1
        elif nums[mid] < target <= nums[hi - 1]:
            lo = mid + 1
        else:
            hi = mid
    return False
