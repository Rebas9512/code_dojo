def column_sums(grid: list[list[int]]) -> list[int]:
    cols = len(grid[0])
    sums = [0] * cols
    for row in grid:
        for col in range(cols):
            sums[col] += row[col]
    return sums
