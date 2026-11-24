"""两个三部分项目，独立题库、判题数据与同步事件。"""

import io
import json
import sys
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.db import Store
from app.problems import ProblemBank
from app.project_run import evaluate_metrics, python_run, sql_plan
from app.sql_judge import dataset, run_node, sql_cases


@pytest.fixture
def bank(monkeypatch, tmp_path):
    bank = ProblemBank(Path(__file__).parent / "fixtures/projects")
    bank.refresh()
    assert not bank.errors
    monkeypatch.setattr(main, "bank", bank)
    monkeypatch.setattr(main, "store", Store(tmp_path / "local/progress.db"))
    return bank


def test_python_injection(bank, judging):
    project = bank.projects["line-fit"]
    part = project.parts[1]
    code = """def fit(n):
    Path("checkpoint").write_text("ready")
    return len(load_data(n)) + 10
"""
    def grade(source):
        return judging.run(code=source, mode="function", cases=[{"args": [3], "expected": 13}], **part.judge_options())
    assert grade(code)["verdict"] == "accepted"
    assert grade(project.solutions[part.id])["verdict"] == "wrong_answer"
    assert grade("pass")["verdict"] == "runtime_error"
    report = project.parts[-1]
    assert judging.run(code=project.solutions[report.id], mode="function", cases=report.cases("all"),
                       **report.judge_options())["verdict"] == "accepted"



def test_class_part_with_checker(bank, judging):
    project = bank.projects["line-fit"]
    options = dict(mode="class", entry="Line", compare="checker", cases=[{"ops": ["Line", "slope"],
                   "args": [[], [3]], "expected": [None, 2]}], reference=project.reference,
                   data=project.directory / "data", runtime="ds",
                   checker="def check(args, expected, actual): return actual == expected and fit(3) == actual[-1]")
    code = "class Line:\n    def slope(self, n): return fit(n)"
    assert judging.run(code=code, **options)["verdict"] == "accepted"
    assert judging.run(code=code.replace("return fit(n)", "return 0"), **options)["verdict"] == "wrong_answer"


def test_sql_injection(bank, tmp_path):
    project = bank.projects["sales-report"]
    final = project.parts[-1]
    sql = project.solutions
    expected_prefix = [sql[p.id] for p in project.parts[:-1]]
    plan = sql_cases(final, tmp_path, all_cases=True)
    for case, total in zip(plan["datasets"], [30, 70], strict=True):
        assert case["setup"][-2:] == expected_prefix
        assert case["expected"]["checks"][0]["rows"] == [[total]]
    assert not any("CREATE VIEW" in step for step in dataset(project.parts[0], "db:sales"))
    job = sql_plan(project)
    assert job["expected"]["checks"][0]["rows"] == [[30]]
    assert job["timeoutMs"] == 12000
    assert job["expected"]["checks"][1]["outcome"] == "ok"


def test_sql_cte_parts(bank, tmp_path):
    project = bank.projects["sales-report"]
    first, second, final = project.parts
    for part, name, code in [(first, "positive_sales", "SELECT amount FROM sales WHERE amount > 0"),
                             (second, "sale_total", "SELECT SUM(amount) AS total FROM positive_sales")]:
        part.meta.cte = name
        project.solutions[part.id] = code
    project.sections = ["WITH positive_sales AS (\n", "\n), sale_total AS (\n", "\n)\n", "\n"]
    setup = dataset(second, "db:sales")
    expected, = run_node(mode="script", cte=second.meta.cte, checks=[c.model_dump() for c in second.meta.checks],
                         datasets=[setup], solution=project.solutions[second.id])
    assert expected["checks"][0]["rows"] == [[30]]
    assert sql_cases(final, tmp_path, all_cases=False)["datasets"][0]["expected"]["checks"][0]["rows"] == [[30]]
    assert sql_plan(project)["expected"]["checks"][0]["rows"] == [[30]]


def test_assemble_export_and_sync(judging, bank, tmp_path, monkeypatch):
    project = bank.projects["line-fit"]
    client = TestClient(main.app, headers={"Content-Type": "application/json"})
    base = "/api/projects/line-fit"
    first, second, third = project.parts
    def submit(p, code, kind="submit"):
        return client.post(f"/api/problems/{p.id}/{kind}", json={"code": code}).json()["verdict"]
    assert client.post(base + "/run", json={}).status_code == 409
    stage = client.get("/api/tracks").json()[0]["stages"][0]
    assert stage["kind"] == "project" and stage["units"][0]["project"] == "line-fit"
    versions = ["# 第一版\n", "# 第二版\n"]
    for header in versions:
        assert submit(first, header + project.solutions[first.id]) == "accepted"
    assert submit(first, "pass") != "accepted"
    assert submit(first, "# 样例\n" + project.solutions[first.id], "run") == "accepted"
    data = client.get(base).json()
    assert data["parts"][0]["status"] == "solved" and data["parts"][1]["status"] is None
    assert versions[1] in data["code"] and versions[0] not in data["code"] and "# 样例" not in data["code"]
    assert 'raise NotImplementedError("第 2 部分还没完成")' in data["code"]
    for p in (second, third):
        assert project.solutions[p.id].strip() not in data["code"]
        assert submit(p, project.solutions[p.id]) == "accepted"
    exported = client.get(base + "/export/py").text
    assert exported == client.get(base).json()["code"]
    assert exported.replace(versions[1], "") == project.reference
    nb = client.get(base + "/export/ipynb").json()
    assert (nb["nbformat"], nb["nbformat_minor"]) == (4, 4)
    assert [c["cell_type"] for c in nb["cells"]] == ["code", *["markdown", "code"] * 3, "code"]
    assert nb["cells"][-1]["source"].endswith("main()")
    with zipfile.ZipFile(io.BytesIO(client.get(base + "/data").content)) as data:
        assert data.namelist() == ["data/points.csv"]
        data.extractall(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", sys.argv.copy())
    ns = {}
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == [] and cell["execution_count"] is None
            exec(cell["source"], ns)
    response = client.post(base + "/run", json={})
    events = [json.loads(line) for line in response.text.splitlines()]
    assert events[0] == {"line": "fitted"} and events[-1]["result"]["metrics"] == {"slope": 2}
    assert client.get(base).json()["completed"]
    main.store.complete_project("line-fit")
    pending = main.store.pending_events()
    assert sum(e["type"] == "project_completions" for e in pending) == 1
    remote = Store(tmp_path / "remote/progress.db")
    remote.import_events(pending)
    assert remote.import_events(pending) == 0 and remote.project_completed("line-fit")
    assert project.assemble(remote.project_answers(project.meta.parts)) == exported


@pytest.mark.parametrize(("code", "verdict"), [
    ('print(\'{"slope": 1}\')', "wrong_answer"),
    ('print(\'{"slope": 2}\')\nraise ValueError("failed")', "runtime_error"),
    ('print("started")\nwhile True: pass', "timeout"),
])
def test_full_run_verdict(bank, judging, code, verdict):
    project = bank.projects["line-fit"]
    project.meta.run.timeout = 1
    events = list(python_run(judging, project, code))
    assert events[-1]["result"]["verdict"] == verdict
    assert events[0].get("line")


def test_training_script_can_restore_its_own_class(bank, judging):
    project = bank.projects["line-fit"]
    code = """import pickle
import threading

class Fit:
    slope = 2

assert threading.current_thread() is threading.main_thread()
with open("model.bin", "wb") as f:
    pickle.dump(Fit(), f)
with open("model.bin", "rb") as f:
    model = pickle.load(f)
import json
print(json.dumps({"slope": model.slope}))
raise SystemExit(0)
"""
    result = list(python_run(judging, project, code))[-1]["result"]
    assert result == {"verdict": "accepted", "metrics": {"slope": 2}}


@pytest.mark.parametrize("output", ["training", "[]", "{}", '{"slope":true}', '{"slope":"2"}', '{"slope":NaN}'])
def test_invalid_metrics(output):
    assert evaluate_metrics(output, {"slope": {">=": 2}})["verdict"] == "wrong_answer"


def test_sql_completion_requires_every_check(bank):
    client = TestClient(main.app, headers={"Content-Type": "application/json"})
    project = bank.projects["sales-report"]
    for part in project.parts:
        main.store.add_submission(problem_id=part.id, kind="submit", track="sales", code=project.solutions[part.id],
                                  result={"verdict": "accepted"}, elapsed_ms=1, hints_used=0)
    base = "/api/projects/sales-report"
    plan = client.post(base + "/run", json={}).json()
    assert plan["sql"] == client.get(base + "/export/sql").text == project.reference
    assert client.post(base + "/sql-result", json={"passed": [True, False]}).json()["verdict"] == "wrong_answer"
    assert not client.get(base).json()["completed"]
    assert client.post(base + "/sql-result", json={"passed": [True, True]}).json()["verdict"] == "accepted"
    assert client.get(base).json()["completed"]
