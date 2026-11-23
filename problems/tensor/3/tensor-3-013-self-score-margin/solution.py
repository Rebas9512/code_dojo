import torch


def margins(x):
    scores = torch.einsum("bid,bjd->bij", x, x)
    own = torch.einsum("bii->bi", scores)
    return scores - own.unsqueeze(2)
