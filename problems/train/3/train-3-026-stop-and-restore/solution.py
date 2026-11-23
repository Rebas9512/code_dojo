import torch
from io import BytesIO


def select_checkpoint(model, epochs, patience):
    best = float("inf")
    wait = 0
    best_epoch = 0
    snapshot = BytesIO()
    for epoch, valid_loss in enumerate(epochs, 1):
        if valid_loss < best:
            best = valid_loss
            best_epoch = epoch
            wait = 0
            snapshot = BytesIO()
            torch.save(model.state_dict(), snapshot)
        else:
            wait += 1
            if wait >= patience:
                break
    snapshot.seek(0)
    model.load_state_dict(torch.load(snapshot, weights_only=True))
    return best_epoch
