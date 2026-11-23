def joint_step(x: float, y: float, rate: float) -> list[float]:
    g = 2*(x+y)
    x = x - rate*g
    y = y - rate*g
    return [x, y]
