def total(scores: list[int]) -> int:
    return sum(scores)


def passed(scores: list[int], cutoff: int) -> int:
    count = 0
    for score in scores:
        if score >= cutoff:
            count += 1
    return count


def highest(scores: list[int]) -> int | None:
    if scores:
        return max(scores)


def summary(scores: list[int], cutoff: int = 60) -> list[int | None]:
    return [total(scores), passed(scores, cutoff), highest(scores)]
