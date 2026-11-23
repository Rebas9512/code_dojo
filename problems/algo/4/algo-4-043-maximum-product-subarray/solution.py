def max_product(nums: list[int]) -> int:
    low = high = best = nums[0]
    for value in nums[1:]:
        a, b = low * value, high * value
        low = min(value, a, b)
        high = max(value, a, b)
        best = max(best, high)
    return best
