def first_positions(nums: list[int], queries: list[int]) -> list[int]:
    positions = {}
    for i, value in enumerate(nums):
        if value not in positions:
            positions[value] = i
    return [positions.get(value, -1) for value in queries]
