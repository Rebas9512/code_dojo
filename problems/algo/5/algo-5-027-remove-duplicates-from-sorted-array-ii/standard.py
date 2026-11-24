def compact(nums: list[int]) -> int:
    size = 0
    for value in nums:
        if size < 2 or value != nums[size - 2]:
            nums[size] = value
            size += 1
    return size


def run_case(nums: list[int]) -> list:
    k = compact(nums)
    return [k, nums[:k]]
