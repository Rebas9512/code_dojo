def compress(chars: list[str]) -> int:
    pass


def run_case(chars: list[str]) -> list:
    size = compress(chars)
    return [size, chars[:size]]
