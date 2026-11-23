def first_echo(text: str) -> str:
    seen = set()
    for ch in text:
        if ch in seen:
            return ch
        seen.add(ch)
    return ""
