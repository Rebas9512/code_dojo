def compact(nums: list[int]) -> int:
    pass


def run_case(nums: list[int]) -> list:
    k = compact(nums)
    return [k, nums[:k]]
