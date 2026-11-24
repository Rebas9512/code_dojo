def design_matrix(numeric, cities, vocabulary):
    one_hot = cities[:, None] == vocabulary
    return np.column_stack((numeric, one_hot, np.ones(len(cities))))
