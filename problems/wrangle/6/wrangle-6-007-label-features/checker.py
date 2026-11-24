USERS = ['user_id', 'city', 'joined_on']
ACTIVITY = ['user_id', 'sessions_30d', 'active_days_30d', 'events_30d']
PURCHASES = ['user_id', 'days_since_last_order', 'orders_30d', 'spend_30d', 'avg_basket']
ORDERS = ['payment_id', 'user_id', 'paid_at', 'amount']
OUTPUT = ['user_id', 'city', 'signup_days', 'sessions_30d', 'active_days_30d', 'events_30d', 'orders_30d', 'spend_30d', 'avg_basket', 'days_since_last_order', 'churned']


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
    users = frame(args[0], USERS)
    activity = frame(args[1], ACTIVITY).astype({col: float for col in ACTIVITY[1:]})
    purchases = frame(args[2], PURCHASES).astype({col: float for col in PURCHASES[1:]})
    for table in (users, activity, purchases):
        table["user_id"] = table["user_id"].astype("Int64")
    actual = fn(users, activity, purchases, frame(args[3], ORDERS), pd.Timestamp(args[4], tz="UTC"))
    for col in OUTPUT:
        if col == "city":
            continue
        assert pd.api.types.is_numeric_dtype(actual[col]), f"{col} 应为数值列"
    assert not pd.api.types.is_bool_dtype(actual["churned"]), "请把标签写成数值 0 或 1"
    return same_table(actual, frame(expected, OUTPUT))
