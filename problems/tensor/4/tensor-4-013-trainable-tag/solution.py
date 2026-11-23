import torch
import torch.nn as nn
x = torch.tensor([1., 2.])
p = nn.Parameter(x)
print(tuple(p.shape))
print(x.requires_grad, p.requires_grad)
print(isinstance(p, nn.Parameter))
