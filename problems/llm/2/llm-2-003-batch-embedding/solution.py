import torch


def embed_batch(weight, ids):
    layer = torch.nn.Embedding.from_pretrained(torch.tensor(weight, dtype=torch.float32))
    return layer(torch.tensor(ids))
