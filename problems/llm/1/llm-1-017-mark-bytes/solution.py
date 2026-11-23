def mark_bytes(text):
    result = []
    for i, part in enumerate(text.split("<end>")):
        if i:
            result.append(1000)
        result.extend(part.encode("utf-8"))
    return result
