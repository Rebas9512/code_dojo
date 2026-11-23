def unique_prefix(nums: list[int]) -> int:
    write = 1
    for read in range(1, len(nums)):
        value = nums[read]
        if value != nums[write - 1]:
            nums[write] = value
            write += 1
    return write


def run_case(nums: list[int]) -> list:
    size = unique_prefix(nums)
    return [size, nums[:size]]
