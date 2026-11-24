from collections import deque


def rot_time(grid: list[list[int]]) -> int:
    queue = deque()
    fresh = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 2:
                queue.append((r, c, 0))
            elif cell == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, minutes = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, minutes + 1))
    return -1 if fresh else minutes
