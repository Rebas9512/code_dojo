def min_jumps(nums: list[int]) -> int:
    end = reach = jumps = 0
    for i in range(len(nums) - 1):
        reach = max(reach, i + nums[i])
        if i == end:
            jumps += 1
            end = reach
    return jumps
