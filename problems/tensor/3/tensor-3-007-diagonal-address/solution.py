import torch
a = torch.tensor([[2, 5], [-3, 7]])
y = torch.einsum("ii->i", a)
reference = a.diagonal()
assert torch.equal(y, reference)
print(tuple(y.shape))
print(y.tolist())
