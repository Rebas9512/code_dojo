def decode_string(text: str) -> str:
    frames = []
    current = ''
    count = 0
    for char in text:
        if char.isdigit():
            count = count * 10 + int(char)
        elif char == '[':
            frames.append((current, count))
            current = ''
            count = 0
        elif char == ']':
            prefix, times = frames.pop()
            current = prefix + current * times
        else:
            current += char
    return current
