def expected_payout(values: list[float], probs: list[float]) -> float:
    return sum(values[i]*probs[i] for i in range(len(values)))
