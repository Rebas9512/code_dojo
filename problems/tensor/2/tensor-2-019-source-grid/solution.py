import torch
i = torch.arange(3)
r = i[:, None]
print(tuple(r.shape))
print((r == i).tolist())
