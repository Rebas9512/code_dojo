def forward_loss(design, labels, weights, l2):
    scores = design @ weights
    signed_scores = (1 - 2 * labels) * scores
    cross_entropy = np.mean(np.logaddexp(0, signed_scores))
    penalty = l2 * np.sum(weights[:-1] ** 2) / 2
    return sigmoid(scores), cross_entropy + penalty
