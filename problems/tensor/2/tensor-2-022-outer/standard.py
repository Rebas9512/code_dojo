import torch


def outer(a, b):
    return a[:, None] * b[None, :]
