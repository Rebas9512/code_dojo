def only_here(records: list[int], others: list[int]) -> list[int]:
    excluded = set(others)
    unique = []
    for badge in records:
        if badge not in excluded:
            unique.append(badge)
            excluded.add(badge)
    return unique


def different_badges(a: list[int], b: list[int]) -> list[list[int]]:
    return [only_here(a, b), only_here(b, a)]
