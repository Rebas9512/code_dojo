def read_level(n: int) -> int | None:
    if n >= 0:
        return n


def display(n: int) -> str:
    level = read_level(n)
    if level is None:
        return "?"
    return str(level)
