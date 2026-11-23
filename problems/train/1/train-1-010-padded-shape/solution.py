import torch
from torch.nn.utils.rnn import pad_sequence
rows = [torch.tensor([1, 0]), torch.tensor([3]), torch.tensor([2, 4, 6, 8])]
print(tuple(pad_sequence(rows, batch_first=True).shape))
