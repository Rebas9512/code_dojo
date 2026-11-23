def balance_dials(x: float, y: float, rate: float, steps: int) -> list[float]:
    for i in range(steps):
        gx = 2*(x-y)
        gy = -gx
        x = x - rate*gx
        y = y - rate*gy
    return [x, y]
