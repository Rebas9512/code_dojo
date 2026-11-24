def build_mlp(width):
    return nn.Sequential(
        nn.Linear(width, 4 * width),
        nn.GELU(),
        nn.Linear(4 * width, width),
    )
