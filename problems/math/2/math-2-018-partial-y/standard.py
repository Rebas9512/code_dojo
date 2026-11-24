def partial_y(x: float, y: float, h: float) -> float:
    base = x * y + y**2
    new_y = y + h
    after = x * new_y + new_y**2
    return (after - base) / h
