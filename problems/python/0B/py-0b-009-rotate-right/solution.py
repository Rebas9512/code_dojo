def reverse_part(nums: list[int], left: int, right: int) -> None:
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def rotate_right(nums: list[int], k: int) -> None:
    if not nums:
        return
    shift = k % len(nums)
    reverse_part(nums, 0, len(nums) - 1)
    reverse_part(nums, 0, shift - 1)
    reverse_part(nums, shift, len(nums) - 1)


def run_case(nums: list[int], k: int) -> list[int]:
    rotate_right(nums, k)
    return nums
