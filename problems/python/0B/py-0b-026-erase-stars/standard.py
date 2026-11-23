def erase_stars(text: str) -> str:
    kept = []
    for ch in text:
        if ch == "*":
            kept.pop()
        else:
            kept.append(ch)
    return "".join(kept)
