import heapq


def closest(points: list[list[int]], k: int) -> list[list[int]]:
    kept = []
    for x, y in points:
        heapq.heappush(kept, (-(x*x + y*y), x, y))
        if len(kept) > k:
            heapq.heappop(kept)
    return [[x, y] for _, x, y in kept]
