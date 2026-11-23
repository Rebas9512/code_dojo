def find_duplicate(nums: list[int]) -> int:
    slow = nums[0]
    fast = nums[nums[0]]
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]
    probe = 0
    while probe != slow:
        probe = nums[probe]
        slow = nums[slow]
    return probe
