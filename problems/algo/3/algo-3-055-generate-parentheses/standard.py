def parentheses(n: int) -> list[str]:
    answers = []

    def visit(opened, closed, word):
        if closed == n:
            answers.append(word)
            return
        if opened < n:
            visit(opened + 1, closed, word + '(')
        if closed < opened:
            visit(opened, closed + 1, word + ')')

    visit(0, 0, '')
    return answers
