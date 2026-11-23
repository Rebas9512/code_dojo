def compact(nums: list[int], target: int) -> int:
    write = 0
    for value in nums:
        if ____:
            nums[write] = value
            write += 1
    return write


def run_case(nums: list[int], target: int) -> list:
    size = compact(nums, target)
    return [size, nums[:size]]
