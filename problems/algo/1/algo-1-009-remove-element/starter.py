def remove_element(nums: list[int], val: int) -> int:
    pass


def run_case(nums: list[int], val: int) -> list:
    size = remove_element(nums, val)
    return [size, nums[:size]]
