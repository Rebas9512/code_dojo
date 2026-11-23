def longest_consecutive(nums: list[int]) -> int:
    values = set(nums)
    best = 0
    for start in values:
        if start - 1 in values:
            continue
        end = start
        while end in values:
            end += 1
        best = max(best, end - start)
    return best
