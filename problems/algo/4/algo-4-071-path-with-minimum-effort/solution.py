import heapq


def minimum_effort(heights: list[list[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost != best[r][c]:
            continue
        if (r, c) == (rows - 1, cols - 1):
            return cost
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                edge = abs(heights[r][c] - heights[nr][nc])
                candidate = max(cost, edge)
                if candidate < best[nr][nc]:
                    best[nr][nc] = candidate
                    heapq.heappush(heap, (candidate, nr, nc))
