import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.Linear(3, 2)
print(len(list(layer.parameters())))
print(layer.weight.numel() + layer.bias.numel())
print(list(layer.state_dict()))
