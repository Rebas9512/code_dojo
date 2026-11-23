from collections import deque


def jumps(x: int, y: int) -> int:
    x, y = abs(x), abs(y)
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    while queue:
        r, c, depth = queue.popleft()
        if (r, c) == (x, y):
            return depth
        for dr, dc in moves:
            a, b = r + dr, c + dc
            if -2 <= a <= x + 2 and -2 <= b <= y + 2 and (a, b) not in seen:
                seen.add((a, b))
                queue.append((a, b, depth + 1))
    return -1
