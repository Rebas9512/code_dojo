import torch
x = torch.tensor([[4, 9, 6], [8, 1, 7]])
top = torch.topk(x, 2, dim=1)
print(tuple(top.values.shape))
print(torch.argmax(x, dim=1).tolist())
