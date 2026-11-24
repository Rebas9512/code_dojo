from io import BytesIO

import torch


def select_checkpoint(model, epochs, patience):
    best_epoch = 1
    best_loss = float("inf")
    for epoch, valid_loss in enumerate(epochs, 1):
        if valid_loss < best_loss:
            best_loss = valid_loss
            best_epoch = epoch
        if epoch == best_epoch:
            snapshot = BytesIO()
            torch.save(model.state_dict(), snapshot)
        if epoch - best_epoch == patience:
            break

    snapshot.seek(0)
    model.load_state_dict(torch.load(snapshot, weights_only=True))
    return best_epoch
