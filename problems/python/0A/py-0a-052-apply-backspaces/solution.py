def apply_backspaces(s: str) -> str:
    typed = []
    for ch in s:
        if ch == "#":
            if len(typed) > 0:
                typed.pop()
        else:
            typed.append(ch)
    return "".join(typed)
