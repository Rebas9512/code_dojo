def keypad(digits: str) -> list[str]:
    groups = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
    if not digits:
        return []
    answers = []
    def fill(i, prefix):
        if i == len(digits):
            answers.append(prefix)
            return
        for ch in groups[int(digits[i]) - 2]:
            fill(i + 1, prefix + ch)
    fill(0, '')
    return answers
