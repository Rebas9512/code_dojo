from torch.utils.data import DataLoader


def batches(values, width, drop):
    loader = DataLoader(values, batch_size=width, drop_last=drop)
    return [batch.tolist() for batch in loader]
