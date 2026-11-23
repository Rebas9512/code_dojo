from collections import deque


def schedule(n: int, prerequisites: list[list[int]]) -> list[int]:
    after = [[] for _ in range(n)]
    degree = [0] * n
    for course, before in prerequisites:
        after[before].append(course)
        degree[course] += 1
    queue = deque(i for i in range(n) if degree[i] == 0)
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for course in after[current]:
            degree[course] -= 1
            if ____:  # 这门课的最后一项依赖刚刚解除
                queue.append(course)
    return order if len(order) == n else []
