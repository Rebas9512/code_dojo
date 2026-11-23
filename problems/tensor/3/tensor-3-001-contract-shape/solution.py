import torch
a = torch.tensor([[2, 1], [0, 3]])
b = torch.tensor([[4], [5]])
y = torch.einsum("ij,jk->ik", a, b)
reference = a @ b
assert torch.equal(y, reference)
print(tuple(y.shape))
print(y.tolist())
