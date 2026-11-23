def unique_prefix(nums: list[int]) -> int:
    pass


def run_case(nums: list[int]) -> list:
    size = unique_prefix(nums)
    return [size, nums[:size]]
