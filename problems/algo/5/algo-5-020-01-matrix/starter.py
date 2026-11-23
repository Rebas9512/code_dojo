from collections import deque


def nearest_zero(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in mat]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 1:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for i, j in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= i < rows and 0 <= j < cols and dist[i][j] == -1:
                dist[i][j] = dist[r][c] + 1
                queue.append((i, j))
    return dist
