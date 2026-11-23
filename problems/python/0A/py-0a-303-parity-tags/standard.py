def parity_tags(nums: list[int]) -> list[str]:
    return ["even" if n % 2 == 0 else "odd" for n in nums]
