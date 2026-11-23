def count_target_ranges(nums: list[int], k: int) -> int:
    pre = [0]
    for value in nums:
        pre.append(pre[-1] + value)
    count = 0
    for left in range(len(nums)):
        for right in range(left, len(nums)):
            if pre[right + 1] - pre[left] == k:
                count += 1
    return count
