def flight_cost(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    price = [float("inf")] * n
    price[src] = 0
    for _ in range(k + 1):
        updated = price[:]
        for u, v, fare in flights:
            updated[v] = min(updated[v], price[u] + fare)
        price = updated
    return -1 if price[dst] == float("inf") else price[dst]
