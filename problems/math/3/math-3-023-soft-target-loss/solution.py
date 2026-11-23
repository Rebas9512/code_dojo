from math import log


def vote_loss(target: list[float], predicted: list[float]) -> float:
    loss = 0.0
    for i in range(len(target)):
        if target[i] > 0:
            loss += target[i] * (-log(predicted[i]))
    return loss
