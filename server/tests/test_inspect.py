"""看数据作答通过题库、提交、课程、助教和附加题的正常入口。"""
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.ai import extra
from app.ai.provider import FakeProvider
from app.db import Store
from app.inspect_data import InspectExercise, data_block
from app.problems import ProblemBank

FIXTURES = Path(__file__).parent / "fixtures/problems"
CHOICE = "data-0-001-book-key"
SHORT = "data-0-002-shelf"


@pytest.fixture
def api(tmp_path, monkeypatch):
    import app.main as main
    monkeypatch.setattr(main, "bank", ProblemBank(FIXTURES))
    monkeypatch.setattr(main, "store", Store(tmp_path / "db.sqlite"))
    monkeypatch.setattr(main.judge, "run", Mock(side_effect=AssertionError("inspect 不需要 Docker")))
    return TestClient(main.app)


def test_load_and_lesson(api):
    root = api.get("/api/tracks").json()[0]
    assert (root["id"], root["language"], root["runtime"], root["total"]) == ("data", "none", "none", 2)
    detail = api.get(f"/api/problems/{CHOICE}").json()
    assert detail["answer"] == {"type": "choice", "options": ["书名 title", "图书编号 book_id"]}
    assert detail["data"][0]["content"].endswith('B2,夜航,""\n')
    assert detail["data"][1]["columns"][0]["primary_key"]
    assert "file" not in detail["data"][0] and "explain" not in detail
    assert api.get(f"/api/problems/{SHORT}").json()["answer"] == {"type": "short"}
    section, = api.get(f"/api/problems/{CHOICE}/lesson").json()["sections"]
    step = section["steps"][1]
    assert section["new"] and step["type"] == "example" and "B2,夜航" in step["data"]["content"]


@pytest.mark.parametrize(("pid", "wrong", "right", "mid"), [(SHORT, " ６ ", "　ａ６ ", "DM04"), (CHOICE, 0, 1, "DM05")])
def test_grade_and_progress(api, pid, wrong, right, mid):
    base = f"/api/problems/{pid}"
    bad = api.post(base + "/run", json={"answer": wrong}).json()
    assert bad["verdict"] == "wrong_answer" and bad["misconception"]["id"] == mid
    assert all(bad["misconception"][k] for k in ("name", "line"))
    assert api.get("/api/tracks").json()[0]["attempted"] == 0
    import app.main as main
    assert main.store.latest_result(pid)["misconception"]["id"] == mid
    assert api.get(base + "/submissions").json() == []
    assert api.post(base + "/submit", json={"answer": wrong}).json()["verdict"] == "wrong_answer"
    assert api.get("/api/tracks").json()[0]["attempted"] == 1
    good = api.post(base + "/submit", json={"answer": right}).json()
    assert good["verdict"] == "accepted" and "misconception" not in good
    assert good["explain"] == bad["explain"] and good["explain"].strip()
    assert [s["verdict"] for s in api.get(base + "/submissions").json()] == ["accepted", "wrong_answer"]
    assert api.get("/api/tracks").json()[0]["solved"] == 1


@pytest.mark.parametrize("block", [
    {"kind": "csv", "content": 'a,b\n"unfinished'},
    {"kind": "table", "content": "a,b\n1,2,3"},
    {"kind": "json", "content": '{"x": NaN}'},
    {"kind": "schema", "content": "columns: [1]"},
    {"kind": "values", "content": "{}"},
    {"kind": "text", "content": "x"},
    {"kind": "table", "file": "../track.yaml"},
    {"kind": "table", "file": "absent.csv"},
    {"kind": "table", "file": "a.csv", "content": "a"},
])
def test_invalid_blocks(block):
    with pytest.raises(ValueError):
        data_block(block, FIXTURES / "data")


@pytest.mark.parametrize("invalid", [
    {"type": "choice", "options": ["甲", "乙"], "correct": 2},
    {"type": "choice", "options": ["甲", "乙"], "correct": True},
    {"type": "short", "accept": []}, {"type": "short", "accept": [" "]},
    {"type": "short", "accept": ["Ａ", "a"]},
])
def test_extra_validation_and_retry(api, invalid):
    import app.main as main
    parent = main.bank.get(CHOICE)
    spec = {"title": "找编号", "mode": "inspect", "statement": "编号是什么？", "explain": "读第一列。",
            "data": [{"kind": "csv", "content": "id\nABC"}], "answer": {"type": "short", "accept": ["ABC"]}}
    fake = FakeProvider([spec | {"answer": invalid}, spec | {"data": [{"kind": "json", "content": "["}]}, spec])
    result, notes = extra.generate(fake, main.judge, parent, request="", skill_names={}, existing=[])
    assert result == spec and len(notes) == 2 and len(fake.calls) == 3
    assert "book_id" in fake.calls[0]["prompt"] and "正确答案" in fake.calls[0]["system"]
    row = main.store.create_extra(CHOICE, "")
    main.store.finish_extra(row["row_id"], result, notes)
    path = "/api/problems/" + row["id"]
    assert api.get(path).json()["answer"] == {"type": "short"}
    assert api.post(path + "/submit", json={"answer": " ａＢｃ "}).json()["verdict"] == "accepted"
    with pytest.raises(ValueError, match="内联"):
        InspectExercise.load(spec | {"data": [{"kind": "table", "file": "books.csv"}]})


@pytest.mark.parametrize(("pid", "answer", "expected"), [(CHOICE, "0", "书名 title"), (SHORT, "A", "学生当前的短答案：A")])
def test_tutor_context_and_edit_target(api, monkeypatch, pid, answer, expected):
    import app.main as main
    edit = {"old": answer, "new": "B", "why": "看清编号"}
    fake = FakeProvider([{"reply": "再看一眼编号。", "edits": [edit]}])
    monkeypatch.setattr(main, "ai", fake)
    r = api.post(f"/api/problems/{pid}/chat", json={"message": "讲讲思路", "answer": answer}).json()
    prompt = fake.calls[0]["prompt"]
    assert expected in prompt and "正确答案（只供判断，不要透露）" in prompt and "B2" in prompt
    assert r["assistant"]["edits"] == ([] if pid == CHOICE else [edit])


def test_extra_api_uses_inspect_branch(api, monkeypatch):
    import app.main as main
    from test_extras import wait_ready

    spec = {"mode": "inspect", "title": "看书名", "statement": "第二本书叫什么？", "explain": "沿第二条记录读书名。",
            "data": [{"kind": "table", "content": "id,name\n1,夜航\n2,远山"}],
            "answer": {"type": "choice", "options": ["夜航", "远山"], "correct": 1}}
    monkeypatch.setattr(main, "ai", FakeProvider([spec]))
    r = api.post(f"/api/problems/{SHORT}/extras", json={"request": "换成单选"})
    assert r.status_code == 200 and r.json()["status"] == "generating"
    ready = wait_ready(api, SHORT, r.json()["seq"])
    assert ready["status"] == "ready"
    base = "/api/problems/" + ready["id"]
    assert api.get(base).json()["answer"] == {"type": "choice", "options": ["夜航", "远山"]}
    assert api.post(base + "/submit", json={"answer": 1}).json()["verdict"] == "accepted"
    assert api.get("/api/tracks").json()[0]["solved"] == 0
