def signs(nums: list[int]) -> list[bool]:
    return [all(x > 0 for x in nums), any(x < 0 for x in nums)]
