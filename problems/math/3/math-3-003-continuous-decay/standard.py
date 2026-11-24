from math import exp


def remaining_mass(mass: float, k: float, times: list[float]) -> list[float]:
    return [mass * exp(-k * t) for t in times]
