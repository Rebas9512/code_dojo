def distance_after(x: float, y: float, a: float, b: float, rate: float) -> float:
    x = x - rate*2*(x-a)
    y = y - rate*2*(y-b)
    return ((x-a)**2 + (y-b)**2)**0.5
