def column_sums(grid: list[list[int]]) -> list[int]:
    cols = len(grid[0])
    sums = [0] * cols
    for i in range(len(grid)):
        for j in range(cols):
            sums[j] += grid[i][j]
    return sums
