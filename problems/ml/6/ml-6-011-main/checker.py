import csv
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory


def check_function(args, expected, fn):
    start, count, seed, folds, steps, candidates, thresholds = args
    with (DATA_DIR / "features.csv").open(encoding="utf-8", newline="") as source:
        header, *rows = csv.reader(source)
    with TemporaryDirectory(dir=".") as name:
        directory = Path(name)
        with (directory / "features.csv").open("w", encoding="utf-8", newline="") as sample:
            writer = csv.writer(sample)
            writer.writerow(header)
            writer.writerows(rows[start:start + count])

        fn.__globals__.update(DATA_DIR=directory, SEED=seed, FOLDS=folds, STEPS=steps,
                              CANDIDATES=candidates, THRESHOLDS=thresholds)
        output = StringIO()
        with redirect_stdout(output):
            fn()

    lines = [line for line in output.getvalue().splitlines() if line.strip()]
    assert len(lines) >= 2, "先打印一行训练或评估摘要，再打印 JSON"
    actual = json.loads(lines[-1])
    np.testing.assert_array_equal(actual["confusion"], expected["confusion"])
    for key in ("precision", "recall", "f1", "auc", "rate", "l2", "threshold"):
        assert type(actual[key]) in (float, int), f"{key} 应为 JSON 数值"
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-8, err_msg=key)
    return True
