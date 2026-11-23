def remove_element(nums: list[int], val: int) -> int:
    size = 0
    for value in nums:
        if value != val:
            nums[size] = value
            size += 1
    return size


def run_case(nums: list[int], val: int) -> list:
    size = remove_element(nums, val)
    return [size, nums[:size]]
