import torch


def compare_modes(layer, x, seed):
    torch.manual_seed(seed)
    layer.train()
    training = layer(x)
    layer.eval()
    with torch.no_grad():
        validation = layer(x)
    return training, validation
