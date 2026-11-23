def interleave(a: str, b: str) -> str:
    parts = []
    size = min(len(a), len(b))
    for i in range(size):
        parts.append(a[i])
        parts.append(b[i])
    return ''.join(parts) + a[size:] + b[size:]
