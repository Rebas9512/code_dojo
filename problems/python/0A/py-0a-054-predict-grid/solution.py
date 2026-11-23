grid = [[1, 2, 3],
        [4, 5, 6]]
print(len(grid))
print(len(grid[0]))
print(grid[1][0])
grid[0][2] = 30
print(grid[0])
for row in grid:
    print(sum(row))
