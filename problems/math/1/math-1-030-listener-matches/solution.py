def listener_matches(tastes: list[list[int]]) -> list[list[int]]:
    columns = [[row[k] for row in tastes] for k in range(len(tastes[0]))]
    scores = []
    for row in tastes:
        matches = []
        for j in range(len(tastes)):
            matches.append(sum(row[k] * columns[k][j] for k in range(len(row))))
        scores.append(matches)
    return scores
