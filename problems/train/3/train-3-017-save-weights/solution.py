import torch
from io import BytesIO


def save_weights(model):
    buf = BytesIO()
    torch.save(model.state_dict(), buf)
    buf.seek(0)
    return buf
