def matches(pattern: str, text: str) -> bool:
    words = text.split()
    pairs = set(zip(pattern, words))
    same_length = len(pattern) == len(words)
    one_word_per_symbol = len(pairs) == len(set(pattern))
    one_symbol_per_word = len(pairs) == len(set(words))
    return same_length and one_word_per_symbol and one_symbol_per_word
