import torch


def diff(x):
    return x[1:] - x[:-1]
