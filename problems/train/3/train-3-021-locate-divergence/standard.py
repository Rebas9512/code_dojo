def first_divergence(train, valid):
    for i in range(1, len(train)):
        if train[i] < train[i - 1] and valid[i] > valid[i - 1]:
            return i + 1
    return 0
