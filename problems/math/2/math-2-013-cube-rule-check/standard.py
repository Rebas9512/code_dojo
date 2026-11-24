def check_cube(x: float, h: float) -> list[float]:
    measured = ((x + h) ** 3 - x**3) / h
    return [3 * x**2, measured]
