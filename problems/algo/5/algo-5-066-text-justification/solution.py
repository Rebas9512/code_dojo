def justify(words: list[str], width: int) -> list[str]:
    lines = []
    i = 0
    while i < len(words):
        j = i + 1
        letters = len(words[i])
        while j < len(words) and letters + len(words[j]) + (j - i) <= width:
            letters += len(words[j])
            j += 1
        gaps = j - i - 1
        if not gaps or j == len(words):
            line = " ".join(words[i:j]).ljust(width)
        else:
            base, extra = divmod(width - letters, gaps)
            parts = [words[i]]
            for offset in range(gaps):
                parts.extend([" " * (base + (offset < extra)), words[i + offset + 1]])
            line = "".join(parts)
        lines.append(line)
        i = j
    return lines
