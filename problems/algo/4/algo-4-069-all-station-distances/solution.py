import heapq


def distances(n: int, edges: list[list[int]], start: int) -> list[int]:
    graph = [[] for _ in range(n)]
    for u, v, weight in edges:
        graph[u].append((v, weight))
    dist = [float("inf")] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cost, node = heapq.heappop(heap)
        if cost != dist[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return [-1 if value == float("inf") else value for value in dist]
