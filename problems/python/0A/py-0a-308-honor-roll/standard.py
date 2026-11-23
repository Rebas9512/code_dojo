def ranking(names: list[str], scores: list[int]) -> list[tuple[int, str, int]]:
    rows = sorted(zip(names, scores), key=lambda pair: (-pair[1], pair[0]))
    return [(rank, name, score) for rank, (name, score) in enumerate(rows, 1)]
