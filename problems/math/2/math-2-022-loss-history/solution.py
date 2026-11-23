def loss_history(x: float, target: float, rate: float, steps: int) -> list[float]:
    losses = [(x-target)**2]
    for i in range(steps):
        slope = 2 * (x-target)
        x = x - rate*slope
        losses.append((x-target)**2)
    return losses
