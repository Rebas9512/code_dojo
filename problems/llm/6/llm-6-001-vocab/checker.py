def check_function(args, expected, cls):
    (text,), (message,), (ids,) = args
    vocab = cls(text)
    return (list(vocab.chars) == sorted(set(text))
            and vocab.encode(message) == expected[1]
            and vocab.decode(ids) == expected[2]
            and vocab.decode(vocab.encode(text)) == text)
