def max_loot(nums: list[int]) -> int:
    two = one = 0
    for amount in nums:
        two, one = one, max(one, two + amount)
    return one
