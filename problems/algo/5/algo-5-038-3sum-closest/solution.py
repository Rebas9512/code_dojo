def closest(nums: list[int], target: int) -> int:
    nums.sort()
    best = sum(nums[:3])
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if abs(total - target) < abs(best - target):
                best = total
            if total == target:
                return total
            if total < target:
                left += 1
            else:
                right -= 1
    return best
