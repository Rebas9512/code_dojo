from torch.utils.data import Dataset


class Pairs(Dataset):
    def __init__(self, values, labels):
        self.values = values
        self.labels = labels

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index], self.labels[index]


def make_dataset(values, labels):
    return Pairs(values, labels)
