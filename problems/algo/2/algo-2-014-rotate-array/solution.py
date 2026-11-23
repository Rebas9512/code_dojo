def reverse_part(nums: list[int], left: int, right: int) -> None:
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def rotate(nums: list[int], k: int) -> None:
    k %= len(nums)
    reverse_part(nums, 0, len(nums) - 1)
    reverse_part(nums, 0, k - 1)
    reverse_part(nums, k, len(nums) - 1)


def run_case(nums: list[int], k: int) -> list:
    rotate(nums, k)
    return nums
