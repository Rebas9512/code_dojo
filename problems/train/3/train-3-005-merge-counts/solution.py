def combined_accuracy(correct, sizes):
    total = sum(sizes)
    if total == 0:
        return 0.0
    return sum(correct) / total
