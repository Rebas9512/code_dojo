from math import log


def log_change(factors: list[float]) -> float:
    total = 0.0
    for factor in factors:
        total += log(factor)
    return total
