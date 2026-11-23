def two_sum(nums: list[int], target: int) -> list[int]:
    positions = {}
    for i, value in enumerate(nums):
        other = target - value
        if other in positions:
            return [positions[other], i]
        positions[value] = i
