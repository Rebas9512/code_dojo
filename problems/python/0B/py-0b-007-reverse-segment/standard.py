def reverse_part(nums: list[int], left: int, right: int) -> None:
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def run_case(nums: list[int], left: int, right: int) -> list[int]:
    reverse_part(nums, left, right)
    return nums
