READERS = ['user_id', 'joined_on', 'channel', 'city', 'device']
OUTPUT = ['user_id', 'city', 'joined_on']


def frame(rows, columns):
    table = pd.DataFrame(rows, columns=columns)
    for name in ("joined_on", "happened_at", "paid_at"):
        if name in table:
            table[name] = pd.to_datetime(table[name], utc=True, format="mixed")
    return table


def same_table(actual, expected):
    pd.testing.assert_frame_equal(
        actual.reset_index(drop=True), expected.reset_index(drop=True),
        check_dtype=False, check_exact=False, atol=1e-9, rtol=1e-9,
    )
    return True


def check_function(args, expected, fn):
    actual = fn(frame(args[0], READERS))
    return same_table(actual, frame(expected, OUTPUT))
