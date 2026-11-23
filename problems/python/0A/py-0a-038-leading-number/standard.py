def leading_number(s: str) -> str:
    result = ""
    for ch in s:
        if not ch.isdigit():
            break
        result += ch
    return result
