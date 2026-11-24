def joint_step(x: float, y: float, rate: float) -> list[float]:
    slope = 2 * (x + y)
    change = rate * slope
    return [x - change, y - change]
