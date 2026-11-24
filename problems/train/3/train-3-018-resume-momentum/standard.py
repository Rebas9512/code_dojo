import torch


def restore(buf, model, optimizer):
    buf.seek(0)
    state = torch.load(buf, weights_only=True)
    model.load_state_dict(state["model"])
    optimizer.load_state_dict(state["optimizer"])
    return state["epoch"]
