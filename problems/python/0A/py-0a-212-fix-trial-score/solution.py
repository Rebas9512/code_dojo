def trial(scores: list[int], bonus: int) -> list[list[int]]:
    adjusted = scores.copy()
    for i in range(len(adjusted)):
        adjusted[i] += bonus
    return [scores, adjusted]
