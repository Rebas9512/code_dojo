import heapq


def cover(groups: list[list[int]]) -> list[int]:
    heap = [(row[0], i, 0) for i, row in enumerate(groups)]
    heapq.heapify(heap)
    high = max(row[0] for row in groups)
    best = [heap[0][0], high]
    while True:
        low, i, j = heapq.heappop(heap)
        if high - low < best[1] - best[0]:
            best = [low, high]
        if j + 1 == len(groups[i]):
            return best
        value = groups[i][j + 1]
        high = max(high, value)
        heapq.heappush(heap, (value, i, j + 1))
