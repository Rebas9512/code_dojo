def count_parameters(layer):
    count = 0
    for parameter in layer.parameters():
        count += parameter.numel()
    return count
