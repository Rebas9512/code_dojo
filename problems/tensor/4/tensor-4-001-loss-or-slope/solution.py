import torch
x = torch.tensor([2., -3.], requires_grad=True)
loss = torch.sum(x * x)
print(tuple(x.shape), tuple(loss.shape))
loss.backward()
print(x.grad.tolist())
