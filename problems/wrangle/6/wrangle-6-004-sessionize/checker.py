EVENTS = ['event_id', 'user_id', 'action', 'happened_at']
OUTPUT = ['event_id', 'user_id', 'action', 'happened_at', 'session_id']


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
    actual = fn(frame(args[0], EVENTS))
    for col in ['session_id']:
        assert pd.api.types.is_numeric_dtype(actual[col]), f"{col} 应为数值列"
    return same_table(actual, frame(expected, OUTPUT))
