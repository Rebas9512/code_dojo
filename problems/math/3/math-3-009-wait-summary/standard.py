def wait_summary(values: list[float]) -> list[float]:
    count = len(values)
    mean = sum(values) / count
    variance = sum((value - mean) ** 2 for value in values) / count
    return [mean, variance, variance**0.5]
