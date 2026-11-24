def train_model(design, labels, rate, l2, steps):
    weights = np.zeros(design.shape[1])
    for _ in range(steps):
        weights -= rate * gradient(design, labels, weights, l2)
    return weights
