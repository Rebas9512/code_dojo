def odd_squares(nums: list[int]) -> list[int]:
    return [x * x for x in nums if x % 2 != 0]
