import heapq


def pop_largest(values: list[int]) -> list[int]:
    heap = []
    for value in values:
        heapq.heappush(heap, -value)
    return [-heapq.heappop(heap) for _ in range(len(heap))]
