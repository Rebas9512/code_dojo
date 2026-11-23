import heapq


def network_delay(times: list[list[int]], n: int, start: int) -> int:
    graph = [[] for _ in range(n + 1)]
    for u, v, delay in times:
        graph[u].append((v, delay))
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        arrival, node = heapq.heappop(heap)
        if arrival != dist[node]:
            continue
        for dest, delay in graph[node]:
            candidate = arrival + delay
            if candidate < dist.get(dest, float("inf")):
                dist[dest] = candidate
                heapq.heappush(heap, (candidate, dest))
    return max(dist.values()) if len(dist) == n else -1
