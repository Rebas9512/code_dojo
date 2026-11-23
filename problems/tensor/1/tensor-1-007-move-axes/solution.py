import torch
x = torch.arange(24).reshape(2, 3, 4)
print(tuple(x.shape))
y = x.permute(2, 0, 1)
print(tuple(y.shape), y.is_contiguous())
z = y.transpose(0, 1)
print(tuple(z.shape))
