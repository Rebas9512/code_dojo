def max_subarray(nums: list[int]) -> int:
    ending = best = nums[0]
    for i in range(1, len(nums)):
        value = nums[i]
        ending = max(value, ending + value)
        best = max(best, ending)
    return best
