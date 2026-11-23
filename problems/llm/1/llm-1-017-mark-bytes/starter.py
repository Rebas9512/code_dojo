def mark_bytes(text):
    result = []
    for i, part in enumerate(text.split("<end>")):
        if i:
            ...
        result.extend(part.encode("utf-8"))
    return result
