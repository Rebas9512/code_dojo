import torch
p = torch.tensor(-4., requires_grad=True)
p.grad = torch.tensor(0.)
opt = torch.optim.SGD([p], lr=0.5, weight_decay=0.25)
opt.step()
print(p.item())
