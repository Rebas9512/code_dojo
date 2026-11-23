import torch
import torch.nn.functional as F
x = torch.ones(2, 3, 4)
wide = F.gelu(x @ torch.ones(4, 8))
print(tuple(wide.shape))
print(tuple((wide @ torch.ones(8, 4)).shape))
