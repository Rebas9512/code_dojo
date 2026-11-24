def gradient(design, labels, weights, l2):
    residual = sigmoid(design @ weights) - labels
    grad = design.T @ residual / len(labels)
    grad[:-1] += l2 * weights[:-1]
    return grad
