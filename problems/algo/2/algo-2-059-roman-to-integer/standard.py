def roman_value(text: str) -> int:
    worth = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, char in enumerate(text):
        value = worth[char]
        if i + 1 < len(text) and value < worth[text[i + 1]]:
            total -= value
        else:
            total += value
    return total
