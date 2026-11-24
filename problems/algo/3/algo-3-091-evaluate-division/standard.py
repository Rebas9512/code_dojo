def quotients(
    equations: list[list[str]], values: list[float], queries: list[list[str]]
) -> list[float]:
    graph = {}
    for (a, b), value in zip(equations, values):
        graph.setdefault(a, []).append((b, value))
        graph.setdefault(b, []).append((a, 1 / value))

    def ratio(start, end):
        if start not in graph or end not in graph:
            return -1.0
        stack = [(start, 1.0)]
        seen = {start}
        while stack:
            node, weight = stack.pop()
            if node == end:
                return weight
            for other, factor in graph[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append((other, weight * factor))
        return -1.0

    return [ratio(a, b) for a, b in queries]
