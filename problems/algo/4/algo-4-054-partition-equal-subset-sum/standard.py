def equal_groups(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    possible = [True] + [False] * target
    for value in nums:
        for total in range(target, value - 1, -1):
            possible[total] = possible[total] or possible[total - value]
    return possible[target]
