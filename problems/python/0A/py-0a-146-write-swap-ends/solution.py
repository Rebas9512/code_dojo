def swap_ends(nums: list[int]) -> list[int]:
    if len(nums) >= 2:
        nums[0], nums[-1] = nums[-1], nums[0]
    return nums
