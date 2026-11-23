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

def area_at(grid: list[list[int]], row: int, col: int) -> int:
    return fill(grid, row, col, 1, 0)
