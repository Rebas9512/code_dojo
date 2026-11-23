from collections import deque


def dock(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    seen = set()
    for r, row in enumerate(grid):
        if "@" in row:
            start = (r, row.index("@"))
            queue.append((*start, 0))
            seen.add(start)
    while queue:
        r, c, steps = queue.popleft()
        if grid[r][c] == "+":
            return steps
        for i, j in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= i < rows and 0 <= j < cols and grid[i][j] != "#" and (i, j) not in seen:
                seen.add((i, j))
                queue.append((i, j, steps + 1))
    return -1
