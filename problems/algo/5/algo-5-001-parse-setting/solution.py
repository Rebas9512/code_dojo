def read_setting(line: str, fallback: int) -> int:
    try:
        key, value = line.split("=")
        if key.strip():
            return int(value)
    except ValueError:
        return fallback
    return fallback
