def codec(letters, value, mode):
    if mode == "decode":
        return "".join(letters[i] for i in value)
    lookup = {c: i for i, c in enumerate(letters)}
    return [lookup[c] for c in value]
