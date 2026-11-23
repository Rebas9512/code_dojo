def first_repeat(nums: list[int]) -> int | None:
    seen = set()
    for value in nums:
        if value in seen:
            return value
        seen.add(value)
    return None
