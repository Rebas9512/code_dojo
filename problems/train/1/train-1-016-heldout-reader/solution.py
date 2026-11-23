import torch
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence


class SelectedRows(Dataset):
    def __init__(self, rows, ids):
        self.rows = rows
        self.ids = ids

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index):
        return self.rows[self.ids[index]]


def collate(rows):
    tensors = [torch.tensor(row, dtype=torch.long) for row in rows]
    return pad_sequence(tensors, batch_first=True, padding_value=-1)


def training_reader(rows, order, held, width):
    subset = SelectedRows(rows, order[held:])
    return DataLoader(subset, batch_size=width, collate_fn=collate)
