def learning_rate(step, steps, warmup, peak, floor):
    if step <= warmup:
        return peak * step / warmup
    progress = (step - warmup) / (steps - warmup)
    return floor + (peak - floor) * (1 + math.cos(math.pi * progress)) / 2
