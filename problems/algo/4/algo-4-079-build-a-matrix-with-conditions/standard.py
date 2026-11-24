def place_numbers(k: int, above: list[list[int]], left: list[list[int]]) -> list[list[int]]:
    def order(pairs):
        graph = [[] for _ in range(k + 1)]
        degree = [0] * (k + 1)
        for a, b in pairs:
            graph[a].append(b)
            degree[b] += 1
        ready = [v for v in range(1, k + 1) if degree[v] == 0]
        result = []
        while ready:
            v = ready.pop()
            result.append(v)
            for w in graph[v]:
                degree[w] -= 1
                if degree[w] == 0:
                    ready.append(w)
        return result

    rows, cols = order(above), order(left)
    if len(rows) != k or len(cols) != k:
        return []
    column = {value: i for i, value in enumerate(cols)}
    matrix = [[0] * k for _ in range(k)]
    for r, value in enumerate(rows):
        matrix[r][column[value]] = value
    return matrix
