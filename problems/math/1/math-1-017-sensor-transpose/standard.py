def by_sensor(log: list[list[int]]) -> list[list[int]]:
    result = []
    for col in range(len(log[0])):
        result.append([row[col] for row in log])
    return result
