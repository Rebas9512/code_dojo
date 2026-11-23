import heapq


def rooms_needed(meetings: list[list[int]]) -> int:
    busy = []
    most = 0
    for start, end in sorted(meetings):
        while busy and busy[0] <= start:
            heapq.heappop(busy)
        heapq.heappush(busy, end)
        most = max(most, len(busy))
    return most
