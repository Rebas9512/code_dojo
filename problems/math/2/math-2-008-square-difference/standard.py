def square_rate(x: float, h: float) -> float:
    gain = (x + h) ** 2 - x**2
    return gain / h
