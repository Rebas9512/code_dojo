def vector_length(delta: list[float]) -> float:
    squared = sum(x * x for x in delta)
    return squared ** 0.5
