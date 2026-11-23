def near_duplicate(nums: list[int], k: int) -> bool:
    recent = set()
    for i, value in enumerate(nums):
        if i > k:
            recent.discard(nums[i - k - 1])
        if value in recent:
            return True
        recent.add(value)
    return False
