import torch
ids = torch.randperm(7, generator=torch.Generator().manual_seed(3)).tolist()
valid, train = ids[:2], ids[2:]
print(len(train), len(valid))
print(len(set(train).intersection(valid)))
