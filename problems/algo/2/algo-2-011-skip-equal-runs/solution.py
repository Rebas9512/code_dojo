def distinct_values(nums: list[int]) -> list[int]:
    ordered = sorted(nums)
    result = []
    for i, value in enumerate(ordered):
        if i == 0 or ordered[i - 1] != value:
            result.append(value)
    return result
