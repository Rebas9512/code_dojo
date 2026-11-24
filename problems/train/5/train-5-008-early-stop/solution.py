class EarlyStopping:
    def __init__(self, patience, checkpoint):
        self.patience = patience
        self.checkpoint = checkpoint
        self.best_accuracy = -1.0
        self.wait = 0

    def observe(self, epoch, accuracy, model, optimizer):
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy
            self.wait = 0
            self.checkpoint.save(model, optimizer, epoch)
        else:
            self.wait += 1
        return self.wait >= self.patience

    def restore(self, model, optimizer):
        return self.checkpoint.load(model, optimizer)
