def snapshot(layer):
    return {name: value.clone() for name, value in layer.state_dict().items()}
