import torch
heads = torch.zeros(2, 3, 5, 4)
words = heads.transpose(1, 2)
print(tuple(words.shape))
print(tuple(words.reshape(2, 5, -1).shape))
