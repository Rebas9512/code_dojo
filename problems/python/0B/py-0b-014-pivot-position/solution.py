def pivot_position(nums: list[int]) -> int:
    total = sum(nums)
    left = 0
    for i, value in enumerate(nums):
        right = total - left - value
        if left == right:
            return i
        left += value
    return -1
