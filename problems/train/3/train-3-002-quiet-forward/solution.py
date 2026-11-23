import torch


def measure(model, x):
    model.eval()
    with torch.no_grad():
        return model(x)
