def filter_evens(nums: list[int]) -> list[int]:
    result = []
    for x in nums:
        if x % 2 == 0:
            result.append(x)
    return result
