import heapq


def top_values(values: list[int], k: int) -> list[int]:
    kept = []
    for value in values:
        heapq.heappush(kept, value)
        if len(kept) >= k:
            heapq.heappop(kept)
    return kept
