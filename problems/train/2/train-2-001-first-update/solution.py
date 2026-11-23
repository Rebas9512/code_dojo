import torch
p = torch.tensor(0.0, requires_grad=True)
opt = torch.optim.SGD([p], lr=0.25)
loss = (p - 4) ** 2
opt.zero_grad()
loss.backward()
opt.step()
print(loss.item(), p.item())
