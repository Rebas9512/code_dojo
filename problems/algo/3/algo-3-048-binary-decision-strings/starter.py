def bit_strings(n: int) -> list[str]:
    answers, path = [], []
    def visit():
        if len(path) == n:
            answers.append(''.join(path))
            return
        for digit in '01':
            path.append(digit)
            visit()
            ____  # 撤销刚才放进去的一位
    visit()
    return answers
