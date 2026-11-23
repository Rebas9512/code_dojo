import heapq


def swim_time(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost != best[r][c]:
            continue
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                candidate = max(cost, grid[nr][nc])
                if candidate < best[nr][nc]:
                    best[nr][nc] = candidate
                    heapq.heappush(heap, (candidate, nr, nc))
