def has_duplicate(badges: list[int]) -> bool:
    seen = set()
    for badge in badges:
        if badge in seen:
            return True
        seen.add(badge)
    return False


def run_case(n: int, tail: list[int]) -> bool:
    badges = list(range(n))
    badges.extend(tail)
    return has_duplicate(badges)
