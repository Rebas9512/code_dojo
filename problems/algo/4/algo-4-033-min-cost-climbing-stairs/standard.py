def min_fee(cost: list[int]) -> int:
    two = one = 0
    for top in range(2, len(cost) + 1):
        two, one = one, min(one + cost[top - 1], two + cost[top - 2])
    return one
