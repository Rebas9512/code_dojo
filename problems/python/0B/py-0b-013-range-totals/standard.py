def range_totals(nums: list[int], queries: list[list[int]]) -> list[int]:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    totals = []
    for left, right in queries:
        totals.append(prefix[right + 1] - prefix[left])
    return totals
