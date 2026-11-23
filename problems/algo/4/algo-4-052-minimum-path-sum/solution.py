def min_path(grid: list[list[int]]) -> int:
    cost = [float("inf")] * len(grid[0])
    cost[0] = 0
    for row in grid:
        for c, value in enumerate(row):
            if c > 0:
                cost[c] = min(cost[c], cost[c - 1])
            cost[c] += value
    return cost[-1]
