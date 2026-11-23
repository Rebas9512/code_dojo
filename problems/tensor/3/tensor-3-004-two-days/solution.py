import torch
a = torch.tensor([[[1, 2]], [[2, 1]]])
b = torch.tensor([[[2], [3]], [[5], [1]]])
y = torch.einsum("bij,bjk->bik", a, b)
reference = torch.bmm(a, b)
assert torch.equal(y, reference)
print(tuple(y.shape))
print(y.tolist())
