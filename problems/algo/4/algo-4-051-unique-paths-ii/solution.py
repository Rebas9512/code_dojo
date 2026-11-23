def open_paths(grid: list[list[int]]) -> int:
    row = [0] * len(grid[0])
    row[0] = 1
    for line in grid:
        for c, blocked in enumerate(line):
            if blocked:
                row[c] = 0
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]
