from collections import deque


def last_child(n: int, k: int) -> int:
    line = deque(range(1, n + 1))
    while len(line) > 1:
        for _ in range(k - 1):
            line.append(line.popleft())
        line.popleft()
    return line[0]
