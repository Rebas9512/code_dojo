import heapq
from collections import Counter, deque


def shortest_time(tasks: list[str], n: int) -> int:
    ready = [-count for count in Counter(tasks).values()]
    heapq.heapify(ready)
    cooling = deque()
    time = 0
    while ready or cooling:
        if not ready:
            time = max(time, cooling[0][0])
        while cooling and cooling[0][0] <= time:
            _, count = cooling.popleft()
            heapq.heappush(ready, count)
        count = heapq.heappop(ready) + 1
        if count < 0:
            cooling.append((time + n + 1, count))
        time += 1
    return time
