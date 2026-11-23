"""数据科学提交、课程及附加题均走真正的 CPU 沙箱。"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.ai.extra import generate
from app.ai.provider import FakeProvider
from app.problems import build_extra

ROOT = Path(__file__).parent / "fixtures/problems/dsfix/1"
PROBLEMS = sorted(path.name for path in ROOT.iterdir())


@pytest.fixture
def ds(judging):
    from app.main import app, judge

    if judge.backends["ds"] == "docker" and not judge.image_present("ds"):
        pytest.skip(f"判题镜像 {judge.ds_image} 不存在，先 docker build")
    return TestClient(app)


def submit(client, n, code=None, *, answer=None, examples=False):
    pid = PROBLEMS[n - 1]
    payload = {"answer": answer} if answer is not None else {"code": code}
    response = client.post(f"/api/problems/{pid}/{'run' if examples else 'submit'}", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


@pytest.mark.parametrize("n", range(1, 8))
def test_reference(ds, n):
    code = (ROOT / PROBLEMS[n - 1] / "solution.py").read_text(encoding="utf-8")
    result = submit(ds, n, code, answer="torch.Size([2, 3])\ntorch.Size([3, 2])" if n == 7 else None)
    assert result["verdict"] == "accepted", result
    assert result["passed"] == result["total"] == (1 if n == 7 else 5)


@pytest.mark.parametrize(("n", "code", "message"), [
    (1, "def double(values): return [2 * v for v in values]", "推导式"),
    (1, "def double(values):\n    while values: pass", "循环"),
    (1, "def double(values):\n    for v in values: pass", "循环"),
    (1, "from sklearn.metrics import accuracy_score", "不能导入 sklearn"),
    (6, "import torch.nn.functional as F\ndef attention(q,k,v): return F.scaled_dot_product_attention(q,k,v)",
     "torch.nn.functional.scaled_dot_product_attention"),
    (6, "from torch import nn as n\ndef attention(q,k,v): return n.MultiheadAttention(4,1)", "torch.nn.MultiheadAttention"),
    (6, "def attention(q,k,v): return attend(q,k,v)\nfrom torch.nn.functional import scaled_dot_product_attention as attend",
     "torch.nn.functional.scaled_dot_product_attention"),
])
def test_constraints_before_execution(ds, n, code, message):
    result = submit(ds, n, code, examples=True)
    assert result["verdict"] == "constraint_error" and message in result["error"] and "第 " in result["error"]
    assert result["cases"] == []


@pytest.mark.parametrize(("n", "code", "messages"), [
    (1, "import numpy as np\ndef double(values): return np.asarray(values, dtype=float) * 2", ["dtype", "int", "float"]),
    (1, "def double(values): return values", ["位置 (0,)", "期望 4", "实际 2"]),
    (2, 'import pandas as pd\ndef totals(rows): return pd.DataFrame([["甲",6],["乙",2]], columns=["组","总数"])',
     ["第 1 行", "第 2 列", "期望 7", "实际 6"]),
    (4, "def backward(x, upstream): return x * 0", ["梯度", "超出容差"]),
])
def test_wrong_values(ds, n, code, messages):
    result = submit(ds, n, code, examples=True)
    assert result["verdict"] == "wrong_answer", result
    assert all(m in result["cases"][0]["error"] for m in messages), result


def test_shape_wrong_example(ds):
    from app.main import bank

    problem = bank.get(PROBLEMS[2])
    result = submit(ds, 3, problem.meta.wrong_examples[0]["code"], examples=True)
    assert result["verdict"] == "wrong_answer"
    assert result["cases"][0]["error"] == "形状不同：期望 (3, 2)，实际 (2, 3)"


def test_importing_attention_does_not_call_it(ds):
    solution = (ROOT / PROBLEMS[5] / "solution.py").read_text(encoding="utf-8")
    result = submit(ds, 6, "from torch.nn.functional import *\n" + solution, examples=True)
    assert result["verdict"] == "accepted", result


@pytest.mark.parametrize(("old", "new", "message"), [
    (None, None, "第 2 步没有在 backward 之前清梯度"),
    ("model.eval()", "pass", "model.eval()"),
    (", torch.no_grad()", "", "torch.no_grad()"),
    ("x, y = data.train", "x, y = data.valid", "训练阶段访问了验证集"),
    ("x, y = data.train", "with data.evaluating(): x, y = data.valid\n        x = x[:]", "使用了验证集的张量"),
    ("loss.backward()", "loss.backward()\n        optimizer.zero_grad()", "在 backward 之后清了梯度"),
    ("model(data.valid[0])", "pass", "完成一次评估"),
])
def test_training_diagnosis(ds, old, new, message):
    directory = ROOT / PROBLEMS[4]
    code = (directory / ("solution.py" if old else "starter.py")).read_text(encoding="utf-8")
    if old:
        code = code.replace(old, new)
    result = submit(ds, 5, code, examples=True)
    assert result["verdict"] == "wrong_answer" and message in result["cases"][0]["error"], result


def test_helpers_in_ds_playground(ds):
    code = """
from dojo_grad import numeric_grad, check_grad
from dojo_compare import allclose, frame
from dojo_train import assert_trajectory, assert_overfit, assert_loss_decreased
import numpy as np
import pandas as pd
import torch

x = torch.tensor([1., 2.], dtype=torch.float64)
assert torch.allclose(numeric_grad(lambda t: t.square().sum(), x, 1e-5), 2*x)
assert list(x) == [1., 2.]
assert check_grad(lambda x,y: (y,x), lambda x,y: (x*y).sum(), [x, x])
assert allclose(4, 4) is None
assert "dtype" in allclose(True, 1)
assert "形状" in allclose([[4., 5.]], [4., 5.])
assert allclose([1.0, 0.0], [1.05, 0.001], rtol=.1, atol=.002) is None
assert "位置 (1,)" in allclose([1.0, 0.0], [1.05, 0.001], rtol=.1)
expected = pd.Series([1.0, 2.0], index=[5, 7], name="分")
actual = pd.Series([2.0, 1.000001], index=[7, 5], name="分")
assert frame(expected, actual, ignore_row_order=True) is None
assert "索引" in frame(expected, actual)
assert "名称" in frame(expected, actual.rename("成绩"))
assert frame(expected, actual.rename("成绩"), ignore_row_order=True, check_column_names=False) is None
assert frame(expected, actual.reset_index(drop=True), ignore_row_order=True, ignore_index=True) is None
assert "列名" in frame(expected.to_frame(), actual.rename("成绩").to_frame())
assert frame(pd.Series([None]), pd.Series([np.nan])) is None
assert frame(pd.Series([0,0,3]), pd.Series([0,3,3]), ignore_row_order=True, ignore_index=True)
assert frame(pd.Series([1., 0.]), pd.Series([0.5, 1.5]), ignore_row_order=True, ignore_index=True, atol=.6) is None
for f, args, why in [(assert_trajectory, ([1., .2], [1., .1]), "位置 (1,)"),
                     (assert_overfit, ([1., .2],), "尚未拟合"),
                     (assert_loss_decreased, ([1.] * 20,), "下降不足")]:
    try:
        f(*args)
    except AssertionError as exc:
        assert why in str(exc)
    else:
        raise AssertionError(why)
print("通过")
"""
    response = ds.post("/api/playground/run", json={"problem_id": PROBLEMS[0], "code": code}).json()
    assert response["status"] == "ok" and response["stdout"].strip() == "通过", response


def test_ds_extra_validation_and_run(ds):
    from app.main import bank, judge, judge_problem, RunRequest

    parent = bank.get(PROBLEMS[0])
    code = parent.read("solution.py")
    fake = FakeProvider([dict(title="另一份数组翻倍", statement="返回数组的两倍。", mode="function", entry="double",
                              signature="def double(values):", compare="allclose", starter="", solution=code,
                              tests_json=json.dumps(parent.tests), wrong_solutions=["def double(values): return values"])])
    spec, notes = generate(fake, judge, parent, request="", skill_names={}, existing=[])
    extra = build_extra(parent, 12345, 1, spec)
    assert notes == [] and len(fake.calls) == 1 and extra.meta.constraints.no_loops
    assert judge_problem(extra, RunRequest(code=code), "examples")["verdict"] == "accepted"


def test_class_method_allclose(ds):
    from app.main import judge

    result = judge.run(runtime="ds", mode="class", entry="Vector", compare="allclose",
                       code="import numpy as np\nclass Vector:\n    def values(self): return np.array([1,2])",
                       cases=[{"ops": ["Vector", "values"], "args": [[], []], "expected": [None, [1, 3]]}])
    assert result["verdict"] == "wrong_answer"
    assert "方法调用 values" in result["cases"][0]["error"] and "位置 (1,)" in result["cases"][0]["error"]
