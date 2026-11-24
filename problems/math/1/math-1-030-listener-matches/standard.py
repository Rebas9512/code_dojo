def listener_matches(tastes: list[list[int]]) -> list[list[int]]:
    scores = []
    for listener in tastes:
        matches = []
        for other in tastes:
            matches.append(sum(listener[k] * other[k] for k in range(len(listener))))
        scores.append(matches)
    return scores
