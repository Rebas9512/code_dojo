def surface_gradient(x: float, y: float, h: float) -> list[float]:
    base = x*x + x*y
    right = (x+h)**2 + (x+h)*y
    up = x*x + x*(y+h)
    return [(right-base)/h, (up-base)/h]
