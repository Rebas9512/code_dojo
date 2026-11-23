def max_circular(nums: list[int]) -> int:
    high = low = largest = smallest = total = nums[0]
    for value in nums[1:]:
        high = max(value, high + value)
        low = min(value, low + value)
        largest = max(largest, high)
        smallest = min(smallest, low)
        total += value
    return max(largest, total - smallest)
