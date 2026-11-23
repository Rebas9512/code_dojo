from torch.utils.data import DataLoader
for batch in DataLoader([4, 9, 8, 7], batch_size=3):
    print(tuple(batch.shape))
