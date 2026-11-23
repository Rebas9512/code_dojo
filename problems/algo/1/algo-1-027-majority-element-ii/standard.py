from collections import Counter


def frequent_thirds(nums: list[int]) -> list[int]:
    counts = Counter(nums)
    return [value for value, count in counts.items() if count * 3 > len(nums)]
