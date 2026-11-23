def diagonal_total(grid: list[list[int]]) -> int:
    n = len(grid)
    total = 0
    for row in range(n):
        other = n - 1 - row
        total += grid[row][row]
        if other != row:
            total += grid[row][other]
    return total
