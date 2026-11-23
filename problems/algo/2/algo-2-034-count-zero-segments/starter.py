def zero_segments(nums: list[int]) -> int:
    counts = {}
    prefix = answer = 0
    for value in nums:
        prefix += value
        answer += counts.get(prefix, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer
