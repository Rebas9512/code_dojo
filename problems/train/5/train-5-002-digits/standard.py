class DigitsDataset(Dataset):
    def __init__(self, path):
        import numpy as np
        import torch

        rows = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.int64, ndmin=2)
        self.pixels = torch.tensor(rows[:, :-1], dtype=torch.float32) / 16
        self.labels = torch.tensor(rows[:, -1], dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return self.pixels[index], self.labels[index]
