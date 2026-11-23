def can_pack(nums: list[int], target: int) -> bool:
    possible = [True] + [False] * target
    for value in nums:
        for total in range(target, value - 1, -1):
            possible[total] = possible[total] or possible[total - value]
    return possible[target]
