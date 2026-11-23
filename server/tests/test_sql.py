"""SQL 从题目文件到浏览器上报、附加题验证的完整流程，使用独立题库和真实 PGlite。"""
from dataclasses import replace
from pathlib import Path
import shutil

import pytest
import yaml
from fastapi.testclient import TestClient

from app import sql_judge
from app.ai import extra
from app.ai.provider import FakeProvider
from app.db import Store
from app.problems import ProblemBank, build_extra

PID = "sql-0-001-copies"
URL = f"/api/problems/{PID}"
SOLUTION = "SELECT n AS copies FROM books ORDER BY n"
SCHEMA = "CREATE TABLE books(n int)"
SEED = "INSERT INTO books VALUES (8), (5)"
FIXTURES = Path(__file__).parent / "fixtures/problems"


@pytest.fixture
def site(tmp_path, monkeypatch):
    import app.main as main

    root = tmp_path / "bank"
    shutil.copytree(FIXTURES, root)
    directory = root / "sql/0" / PID
    db = root / "sql/_db/store"
    db.mkdir(parents=True)
    directory.mkdir(parents=True)
    (db / "schema.sql").write_text(SCHEMA, encoding="utf-8")
    (db / "seed.sql").write_text(SEED, encoding="utf-8")
    (directory / "patch.sql").write_text("INSERT INTO books VALUES (13)", encoding="utf-8")
    (directory / "problem.yaml").write_text(yaml.safe_dump(dict(
        id=PID, title="册数", track="sql", stage="0", order=1, format="fix", difficulty=1,
        datasets=["db:store", "db:store + patch.sql"], ordered=True)), encoding="utf-8")
    (directory / "solution.sql").write_text(SOLUTION, encoding="utf-8")
    (directory / "starter.sql").write_text("SELECT 1", encoding="utf-8")
    monkeypatch.setattr(main, "settings", replace(main.settings, data_dir=tmp_path))
    monkeypatch.setattr(main, "bank", ProblemBank(root))
    monkeypatch.setattr(main, "store", Store(tmp_path / "test.db"))
    return TestClient(main.app), main.bank.get(PID), tmp_path


def test_sql_cases_and_cache(site, monkeypatch):
    client, p, directory = site
    sample = client.get(URL + "/sql-cases").json()
    assert sample == {"ordered": True, "tolerance": 1e-6, "datasets": [{
        "hidden": False, "setup": [SCHEMA, SEED], "expected": {"columns": ["copies"], "types": [23], "rows": [[5], [8]]}}]}
    all_cases = client.get(URL + "/sql-cases?scope=all")
    assert SOLUTION not in all_cases.text
    assert all_cases.json()["datasets"][1]["expected"]["rows"] == [[5], [8], [13]]
    assert len(list((directory / "sql-cache").glob("*.json"))) == 2
    with monkeypatch.context() as m:
        m.setattr(sql_judge, "run_node", lambda **kwargs: pytest.fail("重复执行参考解"))
        assert client.get(URL + "/sql-cases?scope=all").json() == all_cases.json()
    (p.path / "patch.sql").write_text("INSERT INTO books VALUES (21)", encoding="utf-8")
    assert client.get(URL + "/sql-cases?scope=all").json()["datasets"][1]["expected"]["rows"][-1] == [21]
    (p.path / "solution.sql").write_text("SELECT MAX(n) AS top FROM books ORDER BY top", encoding="utf-8")
    assert client.get(URL + "/sql-cases").json()["datasets"][0]["expected"]["rows"] == [[8]]
    assert client.get(URL).json()["starter"] == "SELECT 1"


def test_dml_expected_cache_and_record(site, monkeypatch):
    client, p, directory = site
    path = p.path / "problem.yaml"
    check = "SELECT n FROM books ORDER BY n"
    meta = yaml.safe_load(path.read_text(encoding="utf-8")) | {"mode": "dml", "check_query": check}
    path.write_text(yaml.safe_dump(meta), encoding="utf-8")
    solution = "DELETE FROM books WHERE n=5 RETURNING 99"
    (p.path / "solution.sql").write_text(solution, encoding="utf-8")
    plan = client.get(URL + "/sql-cases?scope=all").json()
    assert (plan["mode"], plan["check_query"]) == ("dml", check)
    assert [d["expected"]["rows"] for d in plan["datasets"]] == [[[8]], [[8], [13]]]
    with monkeypatch.context() as m:
        m.setattr(sql_judge, "run_node", lambda **kwargs: pytest.fail("重复执行修改"))
        assert client.get(URL + "/sql-cases?scope=all").json() == plan
    path.write_text(yaml.safe_dump(meta | {"check_query": "SELECT n+1 FROM books ORDER BY n"}), encoding="utf-8")
    assert client.get(URL + "/sql-cases").json()["datasets"][0]["expected"]["rows"] == [[9]]
    expected = plan["datasets"][0]["expected"]
    case = {"status": "passed", "actual": expected, "expected": expected, "affected_rows": 1}
    body = {"code": solution, "sql_result": {"verdict": "accepted", "cases": [case]}}
    assert client.post(URL + "/run", json=body).json()["cases"][0]["affected_rows"] == 1
    assert len(list((directory / "sql-cache").glob("*.json"))) == 3


@pytest.mark.parametrize(("solution", "check", "error"), [
    ("DROP TABLE books", SOLUTION, "只允许一条"),
    ("DELETE FROM books; COMMIT", SOLUTION, "只能运行一条"),
    ("WITH s AS (SELECT 1) SELECT * FROM s", SOLUTION, "只允许一条"),
    ("UPDATE books SET n=n", SOLUTION, "执行前后"),
    ("UPDATE books SET n=4", "SELECT count(*) FROM books ORDER BY 1", "执行前后"),
    ("DELETE FROM books", "DELETE FROM books RETURNING n", "只允许一条 SELECT"),
    ("DELETE FROM books", "SELECT n FROM books", "检查查询缺少 ORDER BY"),
])
def test_dml_rejects_invalid_reference(solution, check, error):
    with pytest.raises(ValueError, match=error):
        sql_judge.run_node(datasets=[[SCHEMA, SEED]], mode="dml", check_query=check,
                           ordered=True, solution=solution)


def test_dml_empty_state_and_hidden_counterexample():
    job = dict(mode="dml", check_query=SOLUTION, ordered=True, solution="DELETE FROM books",
               datasets=[[SCHEMA, SEED], [SCHEMA, "INSERT INTO books VALUES (5)"]])
    tables = sql_judge.run_node(**job, wrong=["DELETE FROM books WHERE n=8"])
    assert [t["rows"] for t in tables] == [[], []]
    with pytest.raises(ValueError, match="隐藏数据集没有抓住"):
        sql_judge.run_node(**job, wrong=["DELETE FROM books WHERE n=5"])
    # 建库时取当前事务编号，两次读表必须看到同一份初始记录。
    with pytest.raises(ValueError, match="执行前后"):
        sql_judge.run_node(**(job | {"solution": "UPDATE books SET n=n",
                                    "datasets": [[SCHEMA, "INSERT INTO books VALUES (txid_current()::int)"]]}))


def test_dml_extra_validates_then_grades_from_fresh_data(site):
    import app.main as main

    client, parent, _ = site
    spec = extra_spec(mode="dml", check_query=SOLUTION, solution="UPDATE books SET n=n+1",
                      wrong_solutions=["UPDATE books SET n=n+2"], starter="UPDATE books SET n=n")
    fake = FakeProvider([spec | {"check_query": None}, spec | {"wrong_solutions": [spec["solution"]]}, spec])
    out, notes = extra.generate(fake, main.judge, parent, request="练习修改语句", skill_names={}, existing=[])
    assert len(notes) == 2 and "check_query" in notes[0] and "隐藏数据集没有抓住" in notes[1]
    row = main.store.create_extra(parent.id, "练习修改语句")
    main.store.finish_extra(row["row_id"], out, notes)
    endpoint = f"/api/problems/{row['id']}"
    assert client.get(endpoint).json()["mode"] == "dml"
    plan = client.get(endpoint + "/sql-cases?scope=all").json()
    assert plan["mode"] == "dml" and plan["check_query"] == SOLUTION
    assert [c["expected"]["rows"] for c in plan["datasets"]] == [[[2], [8]], [[3], [8]], [[4], [8]]]


def test_sql_records_and_tutor(site, monkeypatch):
    import app.main as main

    client, _, _ = site
    expected = {"columns": ["copies"], "types": [23], "rows": [[5], [8]], "rowCount": 2}
    case = {"status": "passed", "actual": expected, "expected": expected, "time_ms": 8}
    body = {"code": SOLUTION, "ai_lines": 1, "sql_result": {"verdict": "accepted", "cases": [case]}}
    assert client.post(URL + "/run", json=body).json()["total"] == 1
    assert client.get(URL).json()["status"] is None
    assert client.post(URL + "/submit", json=body).status_code == 400
    body["sql_result"]["cases"].append(case)
    result = client.post(URL + "/submit", json=body).json()
    assert result["passed"] == result["total"] == 2 and result["cases"][1]["hidden"]
    assert client.get(URL + "/submissions").json()[0]["code"] == SOLUTION
    assert client.get(URL).json()["status"] == "assisted"
    assert client.post(URL + "/submit", json=body | {"ai_lines": 0}).json()["verdict"] == "accepted"
    assert client.get(URL).json()["status"] == "solved"
    bad = case | {"status": "runtime_error", "error": "column missing does not exist\n列不存在"}
    client.post(URL + "/run", json={"code": "SELECT missing", "sql_result": {"verdict": "runtime_error", "cases": [bad]}})
    fake = FakeProvider([{"reply": "看一下列名", "edits": []}])
    monkeypatch.setattr(main, "ai", fake)
    assert client.post(URL + "/chat", json={"code": "SELECT missing", "message": "哪里错了"}).status_code == 200
    prompt = fake.calls[0]["prompt"]
    assert all(text in prompt for text in [SOLUTION, "SELECT missing", "列不存在", '"books"', '"integer"', "[8]"])


def extra_spec(**updates):
    return dict(title="另一张表", statement="按数量排序。", tables=["books"], ordered=True,
                datasets=[f"{SCHEMA}; INSERT INTO books VALUES ({n}),(7)" for n in [1, 2, 3]],
                solution=SOLUTION, wrong_solutions=["SELECT 1"], starter="SELECT 1") | updates


def test_sql_extra_retries_and_can_be_judged(site):
    import app.main as main

    _, parent, directory = site
    fake = FakeProvider([extra_spec(wrong_solutions=[SOLUTION]), extra_spec(starter=SOLUTION), extra_spec()])
    spec, notes = extra.generate(fake, main.judge, parent, request="", skill_names={}, existing=[])
    assert len(fake.calls) == 3
    assert "隐藏数据集没有抓住" in notes[0] and "隐藏数据集没有抓住" in fake.calls[1]["prompt"]
    assert "初始代码在样例上" in notes[1] and SOLUTION in fake.calls[0]["prompt"]
    problem = build_extra(parent, 1, 1, spec)
    assert problem.starter == "SELECT 1" and problem.read("solution.sql") == SOLUTION
    cases = sql_judge.sql_cases(problem, directory, all_cases=True)["datasets"]
    assert [c["expected"]["rows"] for c in cases] == [[[1], [7]], [[2], [7]], [[3], [7]]]


@pytest.mark.parametrize(("solution", "message"), [
    ("SELECT n FROM books /* ORDER BY n */", "ORDER BY"),
    ("SELECT n FROM books WHERE false ORDER BY n", "结果为空"),
    ("SELECT missing FROM books ORDER BY n", "列不存在"),
])
def test_sql_rejects_unusable_reference(solution, message):
    with pytest.raises(ValueError, match=message):
        sql_judge.run_node(datasets=[[SCHEMA, SEED]], solution=solution, ordered=True)


def test_curriculum_comparison_examples(monkeypatch):
    import json
    root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(root / "scripts/curriculum"))
    from verify_sql import norm_result, same_result

    for c in json.loads((root / "web/tests/sql-comparisons.json").read_text(encoding="utf-8")):
        a, b = [norm_result({"rows": c[k], "types": c["types"]}) for k in ("a", "b")]
        assert same_result(a, b, c["ordered"]) == c["equal"], c["name"]


def test_sql_extra_through_chat_and_api(site, monkeypatch):
    import app.main as main
    import time

    client, _, _ = site
    fake = FakeProvider([{"reply": "正在出题", "edits": [], "make_extra": "再练一次"}, extra_spec()])
    monkeypatch.setattr(main, "ai", fake)
    row = client.post(URL + "/chat", json={"message": "再来一道"}).json()["new_extra"]
    endpoint = f"/api/problems/{row['id']}"
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline and client.get(URL + "/extras").json()[0]["status"] == "generating":
        time.sleep(0.1)
    assert client.get(endpoint).json()["starter"] == "SELECT 1"
    cases = client.get(endpoint + "/sql-cases?scope=all").json()["datasets"]
    assert len(cases) == 3 and all(c["hidden"] for c in cases[1:])
    result = {"verdict": "accepted", "cases": [
        {"status": "passed", "expected": c["expected"], "actual": c["expected"]} for c in cases]}
    assert client.post(endpoint + "/submit", json={"sql_result": result, "code": SOLUTION}).json()["total"] == 3


def test_lesson_uses_its_database_and_patch(site):
    client, problem, _ = site
    meta_file = problem.path / "problem.yaml"
    meta = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
    meta["skills"] = {"introduces": "sql.copies"}
    meta_file.write_text(yaml.safe_dump(meta), encoding="utf-8")
    lesson = problem.path.parents[1] / "lessons/sql-0-l01-copies"
    lesson.mkdir(parents=True)
    step = dict(type="example", skill="sql.copies", db="store", code="SELECT max(n) FROM books",
                patch="INSERT INTO books VALUES (42)")
    (lesson / "lesson.yaml").write_text(yaml.safe_dump(dict(
        id=lesson.name, title="册数", track="sql", skills=["sql.copies"], steps=[step])), encoding="utf-8")
    example = client.get(URL + "/lesson").json()["sections"][0]["steps"][0]
    assert example["setup"] == [SCHEMA, SEED, step["patch"]]
    result, = sql_judge.run_node(datasets=[example["setup"]], solution=example["code"])
    assert result["rows"] == [[42]]
    assert client.get(URL + "/sql-cases").json()["datasets"][0]["expected"]["rows"] == [[5], [8]]


MEMBERS = "CREATE TABLE members(email text UNIQUE); INSERT INTO members VALUES ('a')"
CHECKS = [
    {"label": "重复邮箱", "probe": "INSERT INTO members VALUES ('a')", "expect": "error"},
    {"label": "新邮箱", "probe": "INSERT INTO members VALUES ('b')", "expect": "ok"},
    {"label": "会员名单", "query": "SELECT email FROM members ORDER BY email", "ordered": True},
]


def test_script_expected_checks_and_cache(site):
    client, p, _ = site
    path = p.path / "problem.yaml"
    meta = yaml.safe_load(path.read_text()) | {"mode": "script", "checks": CHECKS}
    path.write_text(yaml.safe_dump(meta))
    (p.path / "solution.sql").write_text(MEMBERS)
    plan = client.get(URL + "/sql-cases?scope=all").json()
    assert plan["checks"] == CHECKS and len(plan["datasets"]) == 2
    for dataset in plan["datasets"]:
        duplicate, fresh, members = dataset["expected"]["checks"]
        assert duplicate["outcome"] == "error" and "unique" in duplicate["error"]
        assert fresh == {"outcome": "ok"} and members["rows"] == [["a"]]
    path.write_text(yaml.safe_dump(meta | {"checks": CHECKS[:2]}))
    assert len(client.get(URL + "/sql-cases").json()["datasets"][0]["expected"]["checks"]) == 2


def test_script_validates_reference_and_wrong_scripts():
    job = dict(mode="script", checks=CHECKS, solution=MEMBERS, datasets=[[]])
    assert sql_judge.run_node(**job, wrong=[MEMBERS.replace(" UNIQUE", ""), "CREATE TABLE broken("])
    for sql, reason in [(MEMBERS, "没有抓住"), (MEMBERS.replace(" UNIQUE", ""), "参考解未通过"),
                        (MEMBERS + "; COMMIT", "事务控制语句")]:
        with pytest.raises(ValueError, match=reason):
            sql_judge.run_node(**(job | {"solution": sql}), wrong=[sql])


def test_script_extra_from_empty_database(site):
    _, parent, directory = site
    spec = extra_spec(mode="script", checks=CHECKS, tables=[], datasets=["", "", ""], solution=MEMBERS,
                      wrong_solutions=[MEMBERS.replace(" UNIQUE", "")], starter="SELECT 1")
    fake = FakeProvider([spec])
    out, notes = extra.generate(fake, None, parent, request="", skill_names={}, existing=[])
    assert not notes
    problem = build_extra(parent, 1, 1, out)
    plan = sql_judge.sql_cases(problem, directory, all_cases=True)
    assert plan["mode"] == "script" and plan["datasets"][2]["expected"]["checks"][-1]["rows"] == [["a"]]


def test_script_query_compares_order_per_check():
    job = dict(mode="script", datasets=[[]],
               solution="CREATE TABLE t(n int); INSERT INTO t VALUES (1),(2)",
               checks=[{"label": "名单", "query": "SELECT n FROM t", "ordered": False}])
    reversed_rows = "CREATE TABLE t(n int); INSERT INTO t VALUES (2),(1)"
    with pytest.raises(ValueError, match="没有抓住"):
        sql_judge.run_node(**job, wrong=[reversed_rows])
    wrong_query = [{"label": "名单", "query": "SELECT missing FROM t"}]
    with pytest.raises(ValueError, match="名单.*missing"):
        sql_judge.run_node(**(job | {"checks": wrong_query}))


def test_script_reference_rejects_unexpected_probe_acceptance():
    with pytest.raises(ValueError, match="重复邮箱.*未通过检查"):
        sql_judge.run_node(mode="script", checks=CHECKS, solution=MEMBERS.replace(" UNIQUE", ""), datasets=[[]])
