def count_after(text: str, target: str, i: int) -> int:
    if i == len(text):
        return 0
    hit = 0
    if text[i] == target:
        hit = 1
    return hit + count_after(text, target, i + 1)
