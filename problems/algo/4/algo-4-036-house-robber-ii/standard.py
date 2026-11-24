def circle_loot(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    def line(start, stop):
        two = one = 0
        for i in range(start, stop):
            two, one = one, max(one, two + nums[i])
        return one

    return max(line(0, len(nums) - 1), line(1, len(nums)))
