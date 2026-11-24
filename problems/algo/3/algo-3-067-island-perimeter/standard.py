def perimeter(grid: list[list[int]]) -> int:
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 1:
                total += 4
                if r > 0 and grid[r - 1][c]:
                    total -= 2
                if c > 0 and row[c - 1]:
                    total -= 2
    return total
