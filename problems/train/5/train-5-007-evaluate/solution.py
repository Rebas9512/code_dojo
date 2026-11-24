def evaluate(model, loader):
    import torch

    model.eval()
    correct = 0
    sample_count = 0
    with torch.no_grad():
        for features, labels in loader:
            predicted = torch.max(model(features), dim=1).indices
            correct += torch.sum(predicted == labels).item()
            sample_count += len(labels)
    return correct / sample_count
