import torch
from torch.nn.utils.rnn import pad_sequence


def collate_fn(rows):
    lengths = [len(row) for row in rows]
    seqs = [torch.tensor(row, dtype=torch.long) for row in rows]
    padded = pad_sequence(seqs, batch_first=True, padding_value=0)
    return padded, lengths
