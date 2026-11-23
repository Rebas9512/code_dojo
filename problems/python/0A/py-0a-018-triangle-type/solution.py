def triangle_type(a: int, b: int, c: int) -> str:
    if a + b <= c or a + c <= b or b + c <= a:
        return "不是三角形"
    if a == b and b == c:
        return "等边"
    if a == b or b == c or a == c:
        return "等腰"
    return "普通"
