from collections import deque


def fill_exits(grid: list[list[int]]) -> None:
    queue = deque((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 0)
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((0,1), (0,-1), (1,0), (-1,0)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0])
                    and grid[nr][nc] == 2147483647):
                grid[nr][nc] = grid[r][c] + 1
                queue.append((nr,nc))


def run_case(grid: list[list[int]]) -> list[list[int]]:
    fill_exits(grid)
    return grid
