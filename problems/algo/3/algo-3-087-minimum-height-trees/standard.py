from collections import deque


def shortest_roots(n: int, edges: list[list[int]]) -> list[int]:
    if n == 1:
        return [0]
    adjacent = [[] for _ in range(n)]
    degree = [0] * n
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
        degree[a] += 1
        degree[b] += 1
    leaves = deque(i for i in range(n) if degree[i] == 1)
    remaining = n
    while remaining > 2:
        width = len(leaves)
        remaining -= width
        for _ in range(width):
            leaf = leaves.popleft()
            for near in adjacent[leaf]:
                degree[near] -= 1
                if degree[near] == 1:
                    leaves.append(near)
    return list(leaves)
