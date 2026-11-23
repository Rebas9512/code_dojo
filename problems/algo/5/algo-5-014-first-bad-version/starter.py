def first_bad(n: int, is_bad) -> int:
    pass


def run_case(n: int, first: int) -> int:
    def is_bad(version):
        return version >= first

    return first_bad(n, is_bad)
