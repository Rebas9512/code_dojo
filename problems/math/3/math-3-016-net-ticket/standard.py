def expected_net(values: list[float], probs: list[float], cost: float) -> float:
    payout = sum(values[i] * probs[i] for i in range(len(values)))
    return payout - cost
