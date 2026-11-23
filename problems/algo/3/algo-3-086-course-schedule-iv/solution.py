from collections import deque


def prerequisites_of(n: int, edges: list[list[int]], queries: list[list[int]]) -> list[bool]:
    after = [[] for _ in range(n)]
    degree = [0] * n
    ancestors = [set() for _ in range(n)]
    for a, b in edges:
        after[a].append(b)
        degree[b] += 1
    ready = deque(i for i in range(n) if degree[i] == 0)
    while ready:
        a = ready.popleft()
        for b in after[a]:
            ancestors[b].update(ancestors[a])
            ancestors[b].add(a)
            degree[b] -= 1
            if degree[b] == 0:
                ready.append(b)
    return [a in ancestors[b] for a, b in queries]
