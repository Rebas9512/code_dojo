from collections import deque


def shortest_route(grid: list[list[int]], start: list[int], end: list[int]) -> int:
    queue = deque([(start[0], start[1], 0)])
    seen = {tuple(start)}
    while queue:
        r, c, distance = queue.popleft()
        if [r, c] == end:
            return distance
        for dr, dc in ((0,1), (0,-1), (1,0), (-1,0)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0])
                    and grid[nr][nc] == 0 and (nr,nc) not in seen):
                seen.add((nr,nc))
                queue.append((nr, nc, ____))  # 相邻格子的步数
    return -1
