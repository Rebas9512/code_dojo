import heapq
from collections import Counter


def reorganize(s: str) -> str:
    heap = [(-count, char) for char, count in Counter(s).items()]
    heapq.heapify(heap)
    result = []
    waiting = (0, '')
    while heap:
        count, char = heapq.heappop(heap)
        result.append(char)
        if waiting[0] < 0:
            heapq.heappush(heap, waiting)
        waiting = (count + 1, char)
    return ''.join(result) if len(result) == len(s) else ''
