import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.Linear(3, 2)
x = torch.zeros((4, 3))
print(tuple(layer.weight.shape), tuple(layer.bias.shape))
print(tuple(nn.functional.linear(x, layer.weight, layer.bias).shape))
