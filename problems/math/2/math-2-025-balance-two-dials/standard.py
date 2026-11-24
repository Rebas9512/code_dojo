def balance_dials(x: float, y: float, rate: float, steps: int) -> list[float]:
    for _ in range(steps):
        change = rate * (2 * (x - y))
        x -= change
        y += change
    return [x, y]
