import torch
model = torch.nn.Identity()
model.eval()
with torch.no_grad():
    print(model.training, torch.is_grad_enabled())
print(model.training, torch.is_grad_enabled())
