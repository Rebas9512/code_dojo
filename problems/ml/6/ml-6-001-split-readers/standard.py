def load_split(path, seed):
    table = pd.read_csv(path, keep_default_na=False)
    numeric = np.asarray(table[NUMERIC_COLUMNS], dtype=float)
    cities = np.asarray(table["city"], dtype=str)
    labels = np.asarray(table["churned"], dtype=int)

    rng = np.random.default_rng(seed)
    groups = []
    for label in (0, 1):
        rows = rng.permutation(np.flatnonzero(labels == label))
        holdout = len(rows) // 5
        groups.append(np.split(rows, [len(rows) - 2 * holdout, len(rows) - holdout]))

    train, valid, test = [rng.permutation(np.concatenate(group)) for group in zip(*groups)]
    return numeric, cities, labels, train, valid, test
