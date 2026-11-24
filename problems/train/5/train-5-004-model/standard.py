def build_model(hidden_size):
    import torch.nn as nn

    return nn.Sequential(
        nn.Linear(64, hidden_size),
        nn.ReLU(),
        nn.Linear(hidden_size, 10),
    )
