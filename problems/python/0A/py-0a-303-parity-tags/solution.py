def parity_tags(nums: list[int]) -> list[str]:
    return ["偶" if n % 2 == 0 else "奇" for n in nums]
