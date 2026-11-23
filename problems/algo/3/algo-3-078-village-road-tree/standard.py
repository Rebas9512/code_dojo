def road_tree(n: int, roads: list[list[int]]) -> bool:
    if len(roads) != n - 1:
        return False
    neighbors = [[] for _ in range(n)]
    for a, b in roads:
        neighbors[a].append(b)
        neighbors[b].append(a)

    seen = {0}
    stack = [0]
    while stack:
        village = stack.pop()
        for other in neighbors[village]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == n
