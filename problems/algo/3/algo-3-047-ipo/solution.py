import heapq


def grow_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    projects = sorted(zip(capital, profits))
    ready = []
    index = 0
    for _ in range(k):
        while index < len(projects) and projects[index][0] <= w:
            heapq.heappush(ready, -projects[index][1])
            index += 1
        if not ready:
            break
        w -= heapq.heappop(ready)
    return w
