def fill(grid, r, c, land, marked):
    if grid[r][c] != land:
        return 0
    rows, cols = len(grid), len(grid[0])
    grid[r][c] = marked
    stack = [(r, c)]
    area = 0
    while stack:
        r, c = stack.pop()
        area += 1
        for dr, dc in ((-1,0), (1,0), (0,-1), (0,1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == land:
                grid[nr][nc] = marked
                stack.append((nr, nc))
    return area

def capture_regions(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        fill(grid, r, 0, 'O', '+')
        fill(grid, r, cols-1, 'O', '+')
    for c in range(cols):
        fill(grid, 0, c, 'O', '+')
        fill(grid, rows-1, c, 'O', '+')
    for row in grid:
        for c, cell in enumerate(row):
            row[c] = 'O' if cell == '+' else 'X'


def run_case(grid: list[list[str]]) -> list[list[str]]:
    capture_regions(grid)
    return grid
