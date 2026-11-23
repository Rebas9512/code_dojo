from collections import Counter

def frequency_buckets(nums: list[int]) -> list[list[int]]:
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, count in Counter(nums).items():
        buckets[____].append(value)
    return buckets
