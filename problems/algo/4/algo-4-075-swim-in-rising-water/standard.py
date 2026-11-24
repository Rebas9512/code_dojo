import heapq


def swim_time(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    seen[0][0] = True
    heap = [(grid[0][0], 0, 0)]
    while heap:
        cost, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:
                seen[nr][nc] = True
                heapq.heappush(heap, (max(cost, grid[nr][nc]), nr, nc))
