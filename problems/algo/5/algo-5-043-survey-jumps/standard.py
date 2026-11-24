from collections import deque


def jumps(x: int, y: int) -> int:
    target = (abs(x), abs(y))
    moves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1))
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == target:
            return steps
        for dr, dc in moves:
            neighbor = (abs(r + dr), abs(c + dc))
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor[0], neighbor[1], steps + 1))
