import heapq


def last_weight(stones: list[int]) -> int:
    heap = [-weight for weight in stones]
    heapq.heapify(heap)
    while len(heap) >= 2:
        heaviest = -heapq.heappop(heap)
        next_heaviest = -heapq.heappop(heap)
        if heaviest != next_heaviest:
            heapq.heappush(heap, -(heaviest - next_heaviest))
    return -heap[0] if heap else 0
