def fit(n):
    first, *_, last = load_data(n)
    return (last[1] - first[1]) / (last[0] - first[0])
