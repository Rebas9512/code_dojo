def reverse_part(nums: list[int], left: int, right: int) -> None:
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def rotate_right(nums: list[int], k: int) -> None:
    if not nums:
        return
    n = len(nums)
    shift = k % n
    if shift == 0:
        return
    reverse_part(nums, 0, n - 1)
    reverse_part(nums, 0, shift - 1)
    reverse_part(nums, shift, n - 1)


def run_case(nums: list[int], k: int) -> list[int]:
    rotate_right(nums, k)
    return nums
