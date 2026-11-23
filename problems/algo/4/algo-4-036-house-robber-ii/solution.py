def circle_loot(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    def line(values):
        two = one = 0
        for value in values:
            two, one = one, max(one, two + value)
        return one

    return max(line(nums[:-1]), line(nums[1:]))
