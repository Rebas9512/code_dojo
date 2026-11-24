def loss_history(x: float, target: float, rate: float, steps: int) -> list[float]:
    gap = x - target
    losses = [gap ** 2]
    for _ in range(steps):
        x = x - rate * (2 * gap)
        gap = x - target
        losses.append(gap ** 2)
    return losses
