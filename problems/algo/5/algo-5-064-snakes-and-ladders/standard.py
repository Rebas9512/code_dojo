from collections import deque


def throws(board: list[list[int]]) -> int:
    n = len(board)
    queue = deque([(1, 0)])
    seen = {1}
    while queue:
        here, count = queue.popleft()
        if here == n * n:
            return count
        for step in range(here + 1, min(here + 6, n * n) + 1):
            row, col = divmod(step - 1, n)
            if row % 2:
                col = n - 1 - col
            jump = board[n - 1 - row][col]
            dest = step if jump == -1 else jump
            if dest not in seen:
                seen.add(dest)
                queue.append((dest, count + 1))
    return -1
