from torch.utils.data import Dataset


class Readings(Dataset):
    def __init__(self, values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

r = Readings([6, 2, 9, 5])
print(len(r), r[3])
