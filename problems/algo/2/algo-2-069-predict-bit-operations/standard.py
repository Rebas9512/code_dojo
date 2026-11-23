def inspect_bits(a: int, b: int, i: int) -> list[int]:
    return [a & b, a | b, a ^ b, a << i, a >> i, (a >> i) & 1]
