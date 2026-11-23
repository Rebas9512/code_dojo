import torch
from io import BytesIO


def save_weights(model):
    buf = BytesIO()
    torch.save(model.state_dict(), buf)
    ____  # 在此补全
    return buf
