def check_link(a: float, b: float, x: float, h: float) -> list[float]:
    u = a * x + b
    slope = 2 * u * a
    next_u = a * (x + h) + b
    measured = (next_u**2 - u**2) / h
    return [slope, measured]
