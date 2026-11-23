def ordered_sums(nums: list[int], target: int) -> int:
    ways = [1] + [0] * target
    for total in range(1, target + 1):
        for step in nums:
            if step <= total:
                ways[total] += ways[total - step]
    return ways[target]
