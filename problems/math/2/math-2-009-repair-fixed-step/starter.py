def cube_rate(x: float, h: float) -> float:
    step = 1.0
    return ((x + step) ** 3 - x ** 3) / step
