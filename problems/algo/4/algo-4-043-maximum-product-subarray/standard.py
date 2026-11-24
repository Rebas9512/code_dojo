def max_product(nums: list[int]) -> int:
    low = high = best = nums[0]
    for i in range(1, len(nums)):
        value = nums[i]
        from_low = low * value
        from_high = high * value
        low = min(value, from_low, from_high)
        high = max(value, from_low, from_high)
        best = max(best, high)
    return best
