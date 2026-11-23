import torch
torch.manual_seed(0)
layer = torch.nn.Dropout(1.)
x = torch.tensor([1., 3.])
print(layer(x).tolist())
layer.eval()
print(layer(x).tolist())
