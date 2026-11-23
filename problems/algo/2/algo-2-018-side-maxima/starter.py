def side_maxima(nums: list[int]) -> list[list[int]]:
    left = nums.copy()
    right = nums.copy()
    for i in range(1, len(nums)):
        left[i] = max(left[i - 1], nums[i])
    for i in range(len(nums) - 2, -1, -1):
        right[i] = ____
    return [left, right]
