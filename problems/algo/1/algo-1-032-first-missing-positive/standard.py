def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n:
            target = nums[i] - 1
            if nums[target] == nums[i]:
                break
            nums[i], nums[target] = nums[target], nums[i]
    for i, value in enumerate(nums):
        if value != i + 1:
            return i + 1
    return n + 1
