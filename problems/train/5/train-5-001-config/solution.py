@dataclass
class Config:
    seed: int = 42
    epochs: int = 40
    batch_size: int = 64
    hidden_size: int = 96
    lr: float = 0.006
    weight_decay: float = 0.01
    step_size: int = 12
    gamma: float = 0.5
    max_norm: float = 1.0
    patience: int = 10

    def set_seed(self):
        import random
        from numpy.random import seed as numpy_seed
        import torch

        random.seed(self.seed)
        numpy_seed(self.seed)
        torch.manual_seed(self.seed)
