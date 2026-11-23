def sequence_starts(nums: list[int]) -> list[int]:
    values = set(nums)
    return [x for x in values if x + 1 not in values]
