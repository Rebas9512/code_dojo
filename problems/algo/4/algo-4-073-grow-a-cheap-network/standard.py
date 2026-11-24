import heapq


def connect_stations(n: int, edges: list[list[int]]) -> int:
    graph = [[] for _ in range(n)]
    for u, v, fee in edges:
        graph[u].append((fee, v))
        graph[v].append((fee, u))
    joined = set()
    heap = [(0, 0)]
    total = 0
    while len(joined) < n:
        fee, node = heapq.heappop(heap)
        if node in joined:
            continue
        joined.add(node)
        total += fee
        for edge_fee, dest in graph[node]:
            if dest not in joined:
                heapq.heappush(heap, (edge_fee, dest))
    return total
