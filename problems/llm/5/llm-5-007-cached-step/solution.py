import torch


def cached_step(model, ids, start, cache):
    x, q, k, v = model.project(ids, start)
    if cache is not None:
        old_k, old_v = cache
        k = torch.cat([old_k, k], dim=2)
        v = torch.cat([old_v, v], dim=2)
    scores = q @ k.transpose(-2, -1) / q.shape[-1] ** 0.5
    query_pos = start + torch.arange(ids.shape[1])
    future = torch.arange(k.shape[2])[None, :] > query_pos[:, None]
    weights = torch.softmax(scores.masked_fill(future, float("-inf")), dim=-1)
    return model.finish(x, weights @ v), (k, v)
