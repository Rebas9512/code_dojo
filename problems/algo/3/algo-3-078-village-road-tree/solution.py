def components(n: int, edges: list[list[int]]) -> int:
    neighbors = [[] for _ in range(n)]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    seen = set()
    groups = 0
    for start in range(n):
        if start in seen:
            continue
        groups += 1
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for other in neighbors[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    return groups

def road_tree(n: int, roads: list[list[int]]) -> bool:
    return len(roads) == n - 1 and components(n, roads) == 1
