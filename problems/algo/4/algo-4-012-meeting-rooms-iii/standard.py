import heapq


def busiest_room(n: int, meetings: list[list[int]]) -> int:
    free = list(range(n))
    busy = []
    counts = [0] * n
    for start, end in sorted(meetings):
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if free:
            room = heapq.heappop(free)
            finish = end
        else:
            available, room = heapq.heappop(busy)
            finish = available + end - start
        heapq.heappush(busy, (finish, room))
        counts[room] += 1
    return counts.index(max(counts))
