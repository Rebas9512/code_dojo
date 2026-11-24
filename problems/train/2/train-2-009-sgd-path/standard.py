def momentum_path(start, grads, rate, memory):
    position = start
    velocity = 0.0
    history = []
    for gradient in grads:
        velocity = memory * velocity + gradient
        position -= rate * velocity
        history.append(position)
    return history
