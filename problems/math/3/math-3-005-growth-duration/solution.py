from math import log


def elapsed_time(start: float, end: float, k: float) -> float:
    return log(end / start) / k
