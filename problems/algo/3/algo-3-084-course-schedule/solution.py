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
            if degree[course] == 0:
                queue.append(course)
    return order if len(order) == n else []

def can_finish(n: int, prerequisites: list[list[int]]) -> bool:
    return len(schedule(n, prerequisites)) == n
