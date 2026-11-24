def last_length(text: str) -> int:
    i = len(text) - 1
    while text[i] == " ":
        i -= 1
    end = i
    while i >= 0 and text[i] != " ":
        i -= 1
    return end - i
