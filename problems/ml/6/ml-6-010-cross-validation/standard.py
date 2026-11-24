def select_params(numeric, cities, labels, candidates, k, steps):
    losses = np.zeros(len(candidates))
    rows = np.arange(len(labels))
    for valid in np.array_split(rows, k):
        train = np.ones(len(labels), dtype=bool)
        train[valid] = False
        design = prepare_design(numeric, cities, train)
        for i, (rate, l2) in enumerate(candidates):
            weights = train_model(design[train], labels[train], rate, l2, steps)
            _, loss = forward_loss(design[valid], labels[valid], weights, 0.0)
            losses[i] += loss

    losses /= k
    return candidates[np.argmin(losses)], losses
