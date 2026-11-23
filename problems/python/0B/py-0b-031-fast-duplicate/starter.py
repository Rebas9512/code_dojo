def has_duplicate(badges: list[int]) -> bool:
    pass


def run_case(n: int, tail: list[int]) -> bool:
    badges = list(range(n))
    badges.extend(tail)
    return has_duplicate(badges)
