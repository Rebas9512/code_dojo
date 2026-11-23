def clip_negatives(nums: list[int]) -> list[int]:
    for i in range(len(nums)):
        if nums[i] < 0:
            nums[i] = 0
    return nums
