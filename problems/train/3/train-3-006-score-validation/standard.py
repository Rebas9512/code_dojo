import torch


def accuracy(model, batches):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for x, y in batches:
            pred = torch.argmax(model(x), dim=1)
            correct += torch.sum(pred == y).item()
            total += len(y)
    return correct / total if total else 0.0
