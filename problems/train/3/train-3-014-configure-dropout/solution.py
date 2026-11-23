import torch


def dropout_layer(p, training):
    layer = torch.nn.Dropout(p)
    layer.train(training)
    return layer
