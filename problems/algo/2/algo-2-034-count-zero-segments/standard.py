def zero_segments(nums: list[int]) -> int:
    counts = {0: 1}
    prefix = answer = 0
    for value in nums:
        prefix += value
        previous = counts.get(prefix, 0)
        answer += previous
        counts[prefix] = previous + 1
    return answer
