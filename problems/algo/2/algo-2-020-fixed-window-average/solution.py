def max_average(nums: list[int], k: int) -> float:
    total = sum(nums[i] for i in range(k))
    best = total
    for end in range(k, len(nums)):
        total += nums[end] - nums[end - k]
        best = max(best, total)
    return best / k
