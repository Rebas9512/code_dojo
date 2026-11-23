"""对原始数组、张量和表做比较，并返回可显示的第一处差异。"""

from numbers import Real

import numpy as np


def as_array(value):
    if hasattr(value, "detach"):
        tensor = value.detach().cpu()
        if str(tensor.dtype) == "torch.bfloat16":
            tensor = tensor.float()
        return tensor.numpy()
    return np.asarray(value)


def allclose(expected, actual, *, rtol=1e-5, atol=1e-8):
    """返回 None 表示通过，否则返回中文差异。"""
    try:
        want, got = as_array(expected), as_array(actual)
    except (TypeError, ValueError, RuntimeError) as exc:
        return f"无法转换为规则数值数组：{exc}"
    if want.shape != got.shape:
        return f"形状不同：期望 {want.shape}，实际 {got.shape}"
    kinds = {"i": "整数", "u": "整数", "f": "浮点", "b": "布尔"}
    kind = kinds.get(want.dtype.kind)
    if kind is None or kinds.get(got.dtype.kind) != kind:
        return f"dtype 类别不同或不支持：期望 {want.dtype}，实际 {got.dtype}"
    if kind == "布尔" or rtol == atol == 0:
        close = np.equal(got, want)
    else:
        close = np.isclose(got, want, rtol=rtol, atol=atol)
    if np.all(close):
        return None
    index = tuple(int(n) for n in np.argwhere(~close)[0])
    return f"位置 {index} 超出容差：期望 {want[index].item()}，实际 {got[index].item()}"


def frame(expected, actual, *, rtol=1e-5, atol=1e-8, ignore_row_order=False, ignore_index=False,
          check_column_names=True):
    import pandas as pd

    if isinstance(expected, dict):
        if "columns" in expected:
            expected = pd.DataFrame(expected["data"], columns=expected["columns"], index=expected.get("index"))
        else:
            expected = pd.Series(expected["data"], name=expected.get("name"), index=expected.get("index"))
    if isinstance(expected, pd.Series):
        if not isinstance(actual, pd.Series):
            return f"期望 Series，实际 {type(actual).__name__}"
        if check_column_names and actual.name != expected.name:
            return f"Series 名称不同：期望 {expected.name!r}，实际 {actual.name!r}"
        expected, actual = expected.to_frame(name=0), actual.to_frame(name=0)
    if not isinstance(actual, pd.DataFrame):
        return f"期望 DataFrame，实际 {type(actual).__name__}"
    if expected.shape != actual.shape:
        return f"形状不同：期望 {expected.shape}，实际 {actual.shape}"
    if check_column_names:
        for pos, (left, right) in enumerate(zip(expected.columns, actual.columns)):
            if left != right:
                return f"第 {pos + 1} 列列名不同：期望 {left!r}，实际 {right!r}"

    def equal(a, b):
        if pd.api.types.is_scalar(a) and pd.api.types.is_scalar(b):
            if pd.isna(a) or pd.isna(b):
                return pd.isna(a) and pd.isna(b)
            if isinstance(a, (bool, np.bool_)) or isinstance(b, (bool, np.bool_)):
                return type(a) in (bool, np.bool_) and type(b) in (bool, np.bool_) and a == b
            if isinstance(a, Real) and isinstance(b, Real):
                return bool(np.isclose(b, a, rtol=rtol, atol=atol))
        return np.array_equal(a, b)

    want = list(expected.itertuples(index=False, name=None))
    got = list(actual.itertuples(index=False, name=None))

    def difference(i, j):
        if not ignore_index and not expected.index[i:i + 1].equals(actual.index[j:j + 1]):
            return f"第 {i + 1} 行索引不同：期望 {expected.index[i]!r}，实际 {actual.index[j]!r}"
        for k, (a, b) in enumerate(zip(want[i], got[j])):
            if not equal(a, b):
                return f"期望第 {i + 1} 行、实际第 {j + 1} 行的第 {k + 1} 列不同：期望 {a!r}，实际 {b!r}"
        return None

    for i in range(len(want)):
        error = difference(i, i)
        if error:
            if not ignore_row_order:
                return error
            break
    else:
        return None

    # 常见的分组、排序题仅仅行序不同，先用排序避免两两比较整张表。
    def row_order(rows, index):
        return sorted(range(len(rows)), key=lambda i: rows[i] if ignore_index else (index[i], *rows[i]))

    try:
        pairs = zip(row_order(want, expected.index), row_order(got, actual.index))
        if all(difference(i, j) is None for i, j in pairs):
            return None
    except (TypeError, ValueError):
        pass  # 混合类型或缺失值可能无法排序，下面仍能配对。

    # 容差可能让一行有多个候选，需要一一配对，并保留重复行的次数。
    owner = {}
    candidates = [[j for j in range(len(got)) if difference(i, j) is None] for i in range(len(want))]

    def match(i, visited):
        for j in candidates[i]:
            if j not in visited:
                visited.add(j)
                if j not in owner or match(owner[j], visited):
                    owner[j] = i
                    return True
        return False

    for i in range(len(want)):
        if not match(i, set()):
            j = next(j for j in range(len(got)) if j not in owner)
            return f"第 {i + 1} 行没有可配对的行。{difference(i, j)}"
    return None


def compare_result(mode, expected, value, options):
    if mode == "allclose":
        error = allclose(expected, value, rtol=options.get("rtol", 1e-5), atol=options.get("atol", 1e-8))
        try:
            actual = as_array(value).tolist()
        except (TypeError, ValueError, RuntimeError):
            actual = repr(value)
    else:
        import pandas as pd

        error = frame(expected, value, **options)
        if isinstance(value, pd.Series):
            actual = {"name": value.name, "index": list(value.index), "data": value.tolist()}
        elif isinstance(value, pd.DataFrame):
            actual = value.to_dict(orient="split")
        else:
            actual = repr(value)
    return actual, error
