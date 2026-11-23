def range_totals(nums: list[int], queries: list[list[int]]) -> list[int]:
    pre = [0]
    for value in nums:
        pre.append(pre[-1] + value)
    totals = []
    for left, right in queries:
        totals.append(pre[right + 1] - pre[left])
    return totals
