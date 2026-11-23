def unique_prefix(nums: list[int]) -> int:
    write = 0
    for value in nums:
        if write == 0 or value != nums[write - 1]:
            nums[write] = value
            write += 1
    return write


def run_case(nums: list[int]) -> list:
    size = unique_prefix(nums)
    return [size, nums[:size]]
