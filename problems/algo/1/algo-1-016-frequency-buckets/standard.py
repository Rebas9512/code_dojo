from collections import Counter


def frequency_buckets(nums: list[int]) -> list[list[int]]:
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)
    return buckets
