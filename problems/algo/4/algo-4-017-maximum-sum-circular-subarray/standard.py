def max_circular(nums: list[int]) -> int:
    high = low = largest = smallest = total = nums[0]
    for i in range(1, len(nums)):
        value = nums[i]
        high = max(value, high + value)
        low = min(value, low + value)
        largest = max(largest, high)
        smallest = min(smallest, low)
        total += value
    if largest < 0:
        return largest
    return max(largest, total - smallest)
