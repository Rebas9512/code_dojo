def sign_count(nums: list[int], target: int) -> int:
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    positive = (total + target) // 2
    ways = [1] + [0] * positive
    for value in nums:
        for s in range(positive, value - 1, -1):
            ways[s] += ways[s - value]
    return ways[-1]
