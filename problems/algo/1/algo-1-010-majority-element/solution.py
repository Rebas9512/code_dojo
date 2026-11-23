from collections import Counter


def majority_element(nums: list[int]) -> int:
    counts = Counter(nums)
    for value, count in counts.items():
        if count > len(nums) // 2:
            return value
