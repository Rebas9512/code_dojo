from torch.utils.data import DataLoader


def sizes(values, width):
    loader = DataLoader(values, batch_size=width)
    return [len(batch) for batch in loader]
