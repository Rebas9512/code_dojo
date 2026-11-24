import csv
from pathlib import Path


def check_function(args, expected, fn):
    labels, seed = args
    cities = [["NA", "rome", "unknown"][i % 3] for i in range(len(labels))]
    numeric = [[10 * i + j / 10 for j in range(8)] for i in range(len(labels))]
    path = Path("sample.csv")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "city", *NUMERIC_COLUMNS, "churned"])
        for i, label in enumerate(labels):
            writer.writerow([500 - i, cities[i], *numeric[i], label])

    values, places, target, train, valid, test = fn(path, seed)
    for array in (values, places, target, train, valid, test):
        assert isinstance(array, np.ndarray), "请返回 NumPy 数组，后面会用行号索引"
    np.testing.assert_allclose(values, numeric)
    np.testing.assert_array_equal(places, cities)
    np.testing.assert_array_equal(target, labels)
    assert np.issubdtype(values.dtype, np.floating), "数值特征应为浮点数"
    assert np.issubdtype(target.dtype, np.integer), "标签应为整数"
    for actual, indices in zip((train, valid, test), expected):
        assert np.issubdtype(actual.dtype, np.integer), "行号应为整数"
        np.testing.assert_array_equal(actual, indices)
    return True
