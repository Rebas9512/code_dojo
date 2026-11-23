def max_subarray(nums: list[int]) -> int:
    ending = best = nums[0]
    for value in nums[1:]:
        ending = max(value, ending + value)
        best = max(best, ending)
    return best
