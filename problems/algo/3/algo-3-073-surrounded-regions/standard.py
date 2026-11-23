def mark_safe(grid, r, c):
    if grid[r][c] != 'O':
        return
    rows, cols = len(grid), len(grid[0])
    grid[r][c] = '+'
    stack = [(r, c)]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 'O':
                grid[nr][nc] = '+'
                stack.append((nr, nc))


def capture_regions(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        mark_safe(grid, r, 0)
        mark_safe(grid, r, cols - 1)
    for c in range(cols):
        mark_safe(grid, 0, c)
        mark_safe(grid, rows - 1, c)
    for row in grid:
        for c, cell in enumerate(row):
            row[c] = 'O' if cell == '+' else 'X'


def run_case(grid: list[list[str]]) -> list[list[str]]:
    capture_regions(grid)
    return grid
