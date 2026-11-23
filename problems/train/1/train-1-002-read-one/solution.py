from torch.utils.data import Dataset


class Readings(Dataset):
    def __init__(self, values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]


def reading_at(values, index):
    return Readings(values)[index]
