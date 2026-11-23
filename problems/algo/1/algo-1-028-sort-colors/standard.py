def sort_colors(nums: list[int]) -> None:
    counts = [0, 0, 0]
    for color in nums:
        counts[color] += 1
    index = 0
    for color in range(3):
        for _ in range(counts[color]):
            nums[index] = color
            index += 1


def run_case(nums: list[int]) -> list[int]:
    sort_colors(nums)
    return nums
