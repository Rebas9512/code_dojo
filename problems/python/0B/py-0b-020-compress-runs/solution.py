def compress(chars: list[str]) -> int:
    read = write = 0
    while read < len(chars):
        start = read
        letter = chars[read]
        while read < len(chars) and chars[read] == letter:
            read += 1
        chars[write] = letter
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write


def run_case(chars: list[str]) -> list:
    size = compress(chars)
    return [size, chars[:size]]
