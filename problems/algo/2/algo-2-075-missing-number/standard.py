def missing_number(nums: list[int]) -> int:
    missing = len(nums)
    for i, value in enumerate(nums):
        missing ^= i ^ value
    return missing
