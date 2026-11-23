def shift_char(ch: str, step: int) -> str:
    offset = (ord(ch) - ord("a") + step) % 26
    return chr(ord("a") + offset)


def shift_label(text: str, step: int) -> str:
    result = ""
    for ch in text:
        result += shift_char(ch, step)
    return result
