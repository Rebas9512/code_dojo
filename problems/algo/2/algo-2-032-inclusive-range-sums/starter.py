def range_sums(nums: list[int], queries: list[list[int]]) -> list[int]:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return [____ for left, right in queries]
