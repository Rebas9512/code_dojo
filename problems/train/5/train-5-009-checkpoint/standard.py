class Checkpoint:
    def __init__(self, path):
        self.path = path

    def save(self, model, optimizer, epoch):
        import torch

        torch.save({
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "epoch": epoch,
        }, self.path)

    def load(self, model, optimizer):
        import torch

        state = torch.load(self.path, weights_only=True)
        model.load_state_dict(state["model"])
        optimizer.load_state_dict(state["optimizer"])
        return state["epoch"]
