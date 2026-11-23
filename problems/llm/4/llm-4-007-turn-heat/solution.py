import torch
z = torch.tensor([-1., 1.])
cold = torch.softmax(z / 0.5, -1)
warm = torch.softmax(z / 2, -1)
print(bool(cold[1] > warm[1]))
