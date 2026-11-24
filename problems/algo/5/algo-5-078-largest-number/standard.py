from functools import cmp_to_key


def largest(nums: list[int]) -> str:
    def compare(a, b):
        first = a + b
        second = b + a
        if first > second:
            return -1
        if first < second:
            return 1
        return 0

    parts = sorted((str(n) for n in nums), key=cmp_to_key(compare))
    return "0" if parts[0] == "0" else "".join(parts)
