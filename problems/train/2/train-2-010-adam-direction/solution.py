import torch
p = torch.tensor([2., 2.], requires_grad=True)
opt = torch.optim.Adam([p], lr=0.25)
p.grad = torch.tensor([2., -8.])
opt.step()
print([round(x, 2) for x in p.tolist()])
