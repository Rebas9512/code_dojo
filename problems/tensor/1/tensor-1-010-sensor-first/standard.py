import torch


def sensor_first(cube):
    x = torch.tensor(cube)
    return x.permute(2, 0, 1).reshape(x.shape[2], -1)
