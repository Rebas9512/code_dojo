def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for index, weight in enumerate(nums):
        needed = target - weight
        if needed in seen:
            return [seen[needed], index]
        seen[weight] = index
