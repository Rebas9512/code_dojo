import torch
from io import BytesIO
buf = BytesIO()
weight = torch.tensor([5.])
torch.save({"w": weight}, buf)
weight.add_(2.)
buf.seek(0)
print(torch.load(buf, weights_only=True)["w"].item(), weight.item())
