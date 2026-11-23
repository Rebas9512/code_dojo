import torch
hidden = torch.ones(2, 4, 6)
readout = torch.ones(9, 6)
print(tuple((hidden @ readout.T).shape))
