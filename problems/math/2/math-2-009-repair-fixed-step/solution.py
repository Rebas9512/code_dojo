def cube_rate(x: float, h: float) -> float:
    step = h
    return ((x + step) ** 3 - x ** 3) / step
