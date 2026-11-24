def update_best(best, wait, loss):
    if loss < best:
        return [loss, 0]
    return [best, wait + 1]
