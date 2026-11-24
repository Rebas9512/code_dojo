def train_one_epoch(model, loader, optimizer, loss_fn, max_norm):
    """训练一轮并返回按样本平均的损失。"""
