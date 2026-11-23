def placement_swaps(nums: list[int]) -> int:
    swaps = 0
    for i in range(len(nums)):
        while nums[i] != i + 1:
            target = nums[i] - 1
            nums[i], nums[target] = nums[target], nums[i]
            swaps += 1
    return swaps
