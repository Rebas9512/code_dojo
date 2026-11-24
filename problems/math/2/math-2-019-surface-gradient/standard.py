def surface_gradient(x: float, y: float, h: float) -> list[float]:
    x_squared = x**2
    base = x_squared + x * y
    next_x = x + h
    right = next_x**2 + next_x * y
    up = x_squared + x * (y + h)
    return [(right - base) / h, (up - base) / h]
