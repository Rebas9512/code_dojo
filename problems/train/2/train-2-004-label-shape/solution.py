import torch
scores = torch.tensor([[0., 1., 2.], [0., 1., 2.]])
labels = torch.tensor([2, 1])
loss = torch.nn.CrossEntropyLoss()(scores, labels)
print(tuple(labels.shape), tuple(loss.shape))
