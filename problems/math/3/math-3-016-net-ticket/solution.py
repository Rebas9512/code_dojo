def expected_net(values: list[float], probs: list[float], cost: float) -> float:
    gross = sum(values[i]*probs[i] for i in range(len(values)))
    return gross - cost
