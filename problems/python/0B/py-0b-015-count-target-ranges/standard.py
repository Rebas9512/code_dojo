def count_target_ranges(nums: list[int], k: int) -> int:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    count = 0
    for left in range(len(nums)):
        for right in range(left, len(nums)):
            if prefix[right + 1] - prefix[left] == k:
                count += 1
    return count
