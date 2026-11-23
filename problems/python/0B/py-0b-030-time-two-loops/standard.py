import time


def time_two_loops(nums: list[int]) -> list[int]:
    start = time.perf_counter()
    total = 0
    for value in nums:
        total += value
    middle = time.perf_counter()
    equal_pairs = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                equal_pairs += 1
    end = time.perf_counter()
    print("sum seconds", middle - start, "pair seconds", end - middle)
    return [total, equal_pairs]
