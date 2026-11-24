import csv
from pathlib import Path
from tempfile import TemporaryDirectory


def write_inputs(directory, tables):
    columns = {
        "readers": ["user_id", "joined_on", "channel", "city", "device"],
        "events": ["event_id", "user_id", "action", "happened_at"],
        "payments": ["payment_id", "user_id", "paid_at", "amount"],
    }
    for (name, header), rows in zip(columns.items(), tables, strict=True):
        with (directory / (name + ".csv")).open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

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
    with TemporaryDirectory(dir=".") as folder:
        directory = Path(folder)
        write_inputs(directory, args)
        tables = fn(directory)
    assert isinstance(tables, tuple) and len(tables) == 3, "请依次返回三张表组成的元组"
    schemas = [
        ["user_id", "joined_on", "channel", "city", "device"],
        ["event_id", "user_id", "action", "happened_at"],
        ["payment_id", "user_id", "paid_at", "amount"],
    ]
    for table, rows, columns in zip(tables, expected, schemas, strict=True):
        for col in columns:
            if col.endswith("_id"):
                assert str(table[col].dtype) == "Int64", f"{col} 需要可空整数 Int64"
            if col in ("joined_on", "happened_at", "paid_at"):
                assert str(table[col].dt.tz) == "UTC", f"{col} 需要 UTC 日期时间"
        target = frame(rows, columns)
        for col in columns:
            if col.endswith("_id"):
                target[col] = target[col].astype("Int64")
        for col in ("channel", "city", "device", "action"):
            if col in target:
                target[col] = target[col].astype("string")
                assert pd.api.types.is_string_dtype(table[col].dropna()), f"{col} 应保存文本"
        if "amount" in target:
            target["amount"] = target["amount"].astype("float64")
        same_table(table, target)
    assert pd.api.types.is_float_dtype(tables[2]["amount"]), "amount 应是浮点数"
    return True
