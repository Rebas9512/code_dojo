def mark_island(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    grid[r][c] = '0'
    stack = [(r, c)]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                grid[nr][nc] = '0'
                stack.append((nr, nc))


def count_islands(grid: list[list[str]]) -> int:
    islands = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '1':
                islands += 1
                mark_island(grid, r, c)
    return islands
