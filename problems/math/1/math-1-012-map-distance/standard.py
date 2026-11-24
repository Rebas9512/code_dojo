def map_distance(a: list[float], b: list[float]) -> float:
    total = 0.0
    for i in range(len(a)):
        delta = a[i] - b[i]
        total += delta * delta
    return total**0.5
