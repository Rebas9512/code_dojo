def population_variance(values: list[float]) -> float:
    count = len(values)
    mean = sum(values) / count
    return sum((value - mean) ** 2 for value in values) / count
