import torch


def limit(params, bound):
    torch.nn.utils.clip_grad_norm_(params, bound)
