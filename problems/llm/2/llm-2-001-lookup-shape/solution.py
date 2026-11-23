import torch
layer = torch.nn.Embedding.from_pretrained(torch.zeros(8, 5))
ids = torch.tensor([[1, 1, 0], [2, 0, 4]])
print(tuple(layer(ids).shape))
