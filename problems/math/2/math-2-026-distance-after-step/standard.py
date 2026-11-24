def distance_after(x: float, y: float, a: float, b: float, rate: float) -> float:
    next_x = x - rate * 2 * (x - a)
    next_y = y - rate * 2 * (y - b)
    return ((next_x - a) ** 2 + (next_y - b) ** 2) ** 0.5
