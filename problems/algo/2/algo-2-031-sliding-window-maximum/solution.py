from collections import deque


def window_max(nums: list[int], k: int) -> list[int]:
    candidates = deque()
    result = []
    for right, value in enumerate(nums):
        if candidates and candidates[0] <= right - k:
            candidates.popleft()
        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(right)
        if right + 1 >= k:
            result.append(nums[candidates[0]])
    return result
