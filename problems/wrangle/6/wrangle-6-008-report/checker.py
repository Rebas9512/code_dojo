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

from contextlib import redirect_stdout
from io import StringIO
import json
import math


def check_function(args, expected, fn):
    output = Path("features.csv")
    output.unlink(missing_ok=True)
    with TemporaryDirectory(dir=".") as folder:
        directory = Path(folder)
        write_inputs(directory, args[:3])
        fn.__globals__["DATA_DIR"] = directory
        fn.__globals__["CUTOFF"] = pd.Timestamp(args[3], tz="UTC")
        log = StringIO()
        with redirect_stdout(log):
            fn()
    assert output.is_file(), "请在当前工作目录写出 features.csv"
    actual = pd.read_csv(output)
    assert not pd.api.types.is_bool_dtype(actual["churned"]), "CSV 中的标签应为数值 0 或 1"
    target = pd.DataFrame(expected, columns=FEATURE_COLUMNS)
    pd.testing.assert_frame_equal(actual, target, check_dtype=False, atol=1e-9, rtol=1e-9)
    metrics = json.loads(log.getvalue().strip().splitlines()[-1])
    summary = {"rows": len(target), "columns_ok": 1,
               "churn_rate": target["churned"].mean(), "spend_30d": target["spend_30d"].sum()}
    for name, value in summary.items():
        assert type(metrics[name]) in (int, float), f"{name} 应为 JSON 数值"
        assert math.isclose(metrics[name], value, abs_tol=1e-9), f"请核对 {name}"
    return True
