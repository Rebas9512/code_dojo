import torch
from torch.nn.utils.rnn import pad_sequence


def collate(rows, pad):
    seqs = [torch.tensor(row, dtype=torch.long) for row in rows]
    return pad_sequence(seqs, batch_first=True, padding_value=pad)
