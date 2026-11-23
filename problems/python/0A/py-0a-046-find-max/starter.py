def find_max(nums: list[int]) -> int:
    best = 0
    for x in nums:
        if x > best:
            best = x
    return best
