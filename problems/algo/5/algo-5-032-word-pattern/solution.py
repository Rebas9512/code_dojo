def matches(pattern: str, text: str) -> bool:
    words = text.split()
    return len(pattern) == len(words) and len(set(pattern)) == len(set(words)) == len(
        set(zip(pattern, words))
    )
