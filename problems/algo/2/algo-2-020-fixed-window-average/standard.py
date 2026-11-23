def max_average(nums: list[int], k: int) -> float:
    window_sum = sum(nums[index] for index in range(k))
    best_sum = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best_sum = max(best_sum, window_sum)
    return best_sum / k
