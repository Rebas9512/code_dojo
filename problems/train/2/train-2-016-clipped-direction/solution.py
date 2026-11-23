import torch
p = torch.tensor([0., 0.], requires_grad=True)
p.grad = torch.tensor([-6., 8.])
torch.nn.utils.clip_grad_norm_([p], 5.)
print([round(x, 2) for x in p.grad.tolist()])
