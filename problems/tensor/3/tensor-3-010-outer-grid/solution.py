import torch
a = torch.tensor([2, -1])
b = torch.tensor([3, 0, 4])
y = torch.einsum("i,j->ij", a, b)
reference = a[:, None] * b[None, :]
assert torch.equal(y, reference)
print(tuple(y.shape))
print(y.tolist())
