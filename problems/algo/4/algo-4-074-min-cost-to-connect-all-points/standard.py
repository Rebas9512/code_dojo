def connect_points(points: list[list[int]]) -> int:
    n = len(points)
    joined = [False] * n
    price = [float("inf")] * n
    price[0] = 0
    total = 0
    for _ in range(n):
        node = min((i for i in range(n) if not joined[i]), key=lambda i: price[i])
        joined[node] = True
        total += price[node]
        x, y = points[node]
        for i, (a, b) in enumerate(points):
            if not joined[i]:
                price[i] = min(price[i], abs(x - a) + abs(y - b))
    return total
