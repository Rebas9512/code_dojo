import torch


def restore(layer, saved):
    layer.load_state_dict(saved)
