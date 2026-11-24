def epoch_record(epoch, loss, val_accuracy, lr):
    return {"epoch": epoch, "loss": loss, "val_accuracy": val_accuracy, "lr": lr}
