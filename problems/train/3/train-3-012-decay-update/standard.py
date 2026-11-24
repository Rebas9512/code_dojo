def decay_step(weights, grads, rate, decay):
    return [w - rate * (g + decay * w) for w, g in zip(weights, grads)]
