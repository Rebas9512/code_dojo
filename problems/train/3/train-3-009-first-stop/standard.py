def stop_epoch(losses, patience):
    best = float("inf")
    wait = 0
    for epoch, loss in enumerate(losses, 1):
        if loss < best:
            best, wait = loss, 0
        else:
            wait += 1
            if wait >= patience:
                return epoch
    return 0
