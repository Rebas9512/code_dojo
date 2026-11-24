import math


def common_pattern(a: str, b: str) -> str:
    if a + b != b + a:
        return ""
    return a[: math.gcd(len(a), len(b))]
