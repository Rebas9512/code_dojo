import torch
from torch.utils.data import DataLoader
def draw(seed):
    g = torch.Generator().manual_seed(seed)
    loader = DataLoader(range(8), batch_size=4, shuffle=True, generator=g)
    return [row.tolist() for row in loader]
print(draw(12) == draw(12))
print(len(draw(12)))
