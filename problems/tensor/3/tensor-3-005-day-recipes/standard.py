import torch


def day_recipes(a, b):
    return torch.einsum("bij,bjk->bik", a, b)
