from collections import deque


def can_finish(n: int, prerequisites: list[list[int]]) -> bool:
    after = [[] for _ in range(n)]
    degree = [0] * n
    for course, before in prerequisites:
        after[before].append(course)
        degree[course] += 1
    queue = deque(i for i in range(n) if degree[i] == 0)
    completed = 0
    while queue:
        current = queue.popleft()
        completed += 1
        for course in after[current]:
            degree[course] -= 1
            if degree[course] == 0:
                queue.append(course)
    return completed == n
