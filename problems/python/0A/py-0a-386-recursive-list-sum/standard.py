def sum_from(nums: list[int], i: int = 0) -> int:
    if i == len(nums):
        return 0
    return nums[i] + sum_from(nums, i + 1)
