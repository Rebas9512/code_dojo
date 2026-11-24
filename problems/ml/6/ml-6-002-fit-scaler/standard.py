def fit_scaler(train):
    center = np.mean(train, axis=0)
    spread = np.std(train, axis=0)
    return center, np.where(spread == 0, 1.0, spread)
