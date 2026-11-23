def can_pack(nums: list[int], target: int) -> bool:
    possible = [True] + [False] * target
    for value in nums:
        for total in ____:
            possible[total] = possible[total] or possible[total - value]
    return possible[target]
