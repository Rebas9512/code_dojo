import torch
p = torch.tensor(0., requires_grad=True)
opt = torch.optim.SGD([p], lr=1., momentum=0.5)
for g in [2., 0.]:
    p.grad = torch.tensor(g)
    opt.step()
print(p.item())
