"""用临时旧库、真实 API 和可控的交卷日期验证复习的完整生命周期。"""
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.ai.provider import FakeProvider
from app.db import Store
from app.problems import ProblemBank

FIXTURES = Path(__file__).parent / "fixtures/problems"
A, B = "data-0-001-book-key", "data-0-002-shelf"
ADD = "py-0a-001-add"


def stamp(days):
    return (datetime.now().astimezone() + timedelta(days=days)).isoformat()


@pytest.fixture
def site(tmp_path, monkeypatch):
    import app.main as main
    store = Store(tmp_path / "study.db")
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(main, "bank", ProblemBank(FIXTURES))
    return TestClient(main.app), store


def send(client, pid, body):
    return client.post(f"/api/problems/{pid}/submit", json=body)


def test_migrate_old_database_twice(tmp_path):
    path = tmp_path / "old.db"
    # 按旧列建库（连 ai_lines 都还没有），完全在临时目录中构造。
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE submissions (id INTEGER PRIMARY KEY,problem_id TEXT,track TEXT,kind TEXT,
          code TEXT,verdict TEXT,passed INTEGER,total INTEGER,elapsed_ms INTEGER,hints_used INTEGER,
          result_json TEXT,created_at TEXT)""")
        result = {"verdict": "accepted", "cases": [{"expected": "甲" * 2400}]}
        conn.execute("INSERT INTO submissions VALUES (1,?,'data','submit','1','accepted',1,1,900,0,?,?)",
                     (A, json.dumps(result), stamp(-3)))
        conn.execute("INSERT INTO submissions VALUES (2,?,'python','submit','','compile_error',0,1,900,0,?,?)",
                     (ADD, json.dumps({"verdict": "compile_error", "error": "第 2 行语法错误"}), stamp(-2)))
    for _ in range(2):
        store = Store(path)
        store.initialize_reviews({A})
        assert store.study_rows()[1]["syntax_error"] == 1
        assert store.latest_result(A)["cases"][0]["expected"].endswith("（共 2400 字符）")
        assert store.review_rows() == [dict(problem_id=A, due=str(date.today()-timedelta(days=2)), step=0, rounds=0, rewrite_target=None,
                                           result="new", last_reviewed=None)]
        assert store.submissions(A)[0]["code"] == "1"


def test_daily_limit_and_concurrent_retry(site, monkeypatch):
    from app import db
    client, store = site
    old = stamp(-1)
    with monkeypatch.context() as clock:
        clock.setattr(db, "now", lambda: old)
        assert send(client, A, {"answer": 1}).json()["verdict"] == "accepted"
        assert send(client, B, {"answer": "A6"}).json()["verdict"] == "accepted"
    assert client.put("/api/today/settings", json={"daily_limit": -1}).status_code == 422
    client.put("/api/today/settings", json={"daily_limit": 1})
    plan = client.get("/api/today").json()
    r, = plan["reviews"]
    assert r["source"] == A and r["step"] == 0
    body = {"review_source": A, "review_due": r["due"], "answer": 0}
    with ThreadPoolExecutor(max_workers=2) as pool:
        codes = list(pool.map(lambda _: send(client, A, body).status_code, range(2)))
    assert sorted(codes) == [200, 409]
    assert client.get("/api/today").json()["reviews"] == []
    assert client.get("/api/tracks/data/skills").json()[0]["state"] == "review"
    assert store.submissions(A)[0]["kind"] == "review"
    assert store.review_rows()[0]["due"] == str(date.today() + timedelta(days=1))
    assert client.get("/api/today").json()["first_rate"] == 1


def test_solution_ai_author_hints_and_rewrite(site, monkeypatch, fake_agents):
    import app.main as main
    from app import db
    client, store = site
    with monkeypatch.context() as clock:
        old = stamp(-1)
        clock.setattr(db, "now", lambda: old)
        reply = client.post(f"/api/problems/{A}/solution", json={}).json()
        assert "图书编号" in reply["solution"]
        assert store.review_rows()[0]["result"] == "rewrite"
        client.post(f"/api/problems/{A}/submit", json={"answer": 1})
        main.bank.problems[B].meta.hints = ["看编号"]
        client.post(f"/api/problems/{B}/hints/1", json={}).raise_for_status()
        fake_agents(claude=FakeProvider([{"reply": "再对照一下编号。", "edits": []}]))
        client.post(f"/api/problems/{B}/chat", json={"message": "给我一点提示"}).raise_for_status()
        assert send(client, B, {"answer": "A6", "hints_used": 1}).status_code == 200
    assert store.submissions(B)[0]["hints_used"] == 2
    assert client.get("/api/tracks/data/skills").json()[0]["counted_solves"] == 0
    due = client.get("/api/today").json()["reviews"]
    assert [r["rewrite"] for r in due] == [True, True]
    body = {"review_source": A, "review_due": due[0]["due"], "answer": 1}
    send(client, A, body).raise_for_status()
    assert store.review_rows()[0]["step"] == 0
    assert store.study_rows()[-1]["solution_seen"] == 0
    assert client.get("/api/tracks/data/skills").json()[0]["counted_solves"] == 1


def test_second_review_changes_target_and_records_source(site, monkeypatch, fake_agents):
    from app import db
    client, store = site
    # 将调度时钟和展示日历一起推进，走普通交卷、原题复习、变式复习三个入口。
    class Day(date):
        offset = -4

        @classmethod
        def today(cls):
            return date.today() + timedelta(days=cls.offset)

    monkeypatch.setattr("app.main.date", Day)
    monkeypatch.setattr(db, "now", lambda: stamp(Day.offset))
    send(client, A, {"answer": 1}).raise_for_status()
    Day.offset = -3
    first, = client.get("/api/today").json()["reviews"]
    send(client, A, dict(review_source=A, review_due=first["due"], answer=1)).raise_for_status()
    Day.offset = 0
    second, = client.get("/api/today").json()["reviews"]
    assert second["id"] == B and second["source"] == A and second["step"] == 1
    ctx = dict(review_source=A, review_due=second["due"])
    assert send(client, A, ctx | {"answer": 1}).status_code == 409
    send(client, B, ctx | {"answer": "A6"}).raise_for_status()
    assert store.study_rows()[-1]["review_source"] == A
    assert store.review_rows()[0]["due"] == str(date.today() + timedelta(days=7))
    assert client.get("/api/tracks").json()[0]["mastered"] == 1
    Day.offset = 7
    fallback, = client.get("/api/today").json()["reviews"]
    assert fallback["generate"] and fallback["source"] == A
    spec = {"title":"练习编号", "mode":"inspect", "statement":"读编号", "explain":"看第一列。",
            "data":[{"kind":"csv", "content":"编号\nABC"}], "answer":{"type":"short", "accept":["ABC"]}}
    progress = dict(type="progress", description="留意编号", body="练习时用两个同名图书作对照。",
                    as_of=str(Day.today()), scope="data.column-key")
    store.add_chat(A, "assistant", "好。", snapshot=store.memory_snapshot(), memory=[{"name": "key", "note": progress}])
    fake = FakeProvider([spec])
    fake_agents(claude=fake)
    import time
    extra = client.post(f"/api/problems/{A}/extras", json={"request":"同套路", "review_source": A, "review_due": fallback["due"]}).json()
    for _ in range(100):
        if store.get_extra(int(extra["id"][2:]))["status"] != "generating":
            break
        time.sleep(.02)
    target, = client.get("/api/today").json()["reviews"]
    assert len(fake.calls) == 1 and progress["body"] not in fake.calls[0]["prompt"]
    assert target["id"] == extra["id"] and target["parent"] == A
    send(client, target["id"], dict(review_source=A, review_due=target["due"], answer="ABC")).raise_for_status()
    assert store.review_rows()[0]["step"] == 3


def test_background_progress_preserves_review_plan_and_mastery(site, monkeypatch, fake_agents):
    from app import db, main
    client, store = site
    yesterday = stamp(-1)
    monkeypatch.setattr(db, "now", lambda: yesterday)
    send(client, A, {"answer": 1}).raise_for_status()
    client.put("/api/today/settings", json={"daily_limit": 1}).raise_for_status()
    plan = client.get("/api/today").json()
    skills = client.get("/api/tracks/data/skills").json()
    reviews = store.review_rows()
    note = dict(type="progress", description="核对编号", scope="data.column-key", as_of=yesterday[:10], body="用书名相同的两行练习。")
    fake = FakeProvider([{"memory": [{"name": "column-key", "note": note}]}])
    fake_agents(claude=fake)
    client.get("/api/tracks").raise_for_status()
    main._review_thread.join(5)
    assert store.memory_snapshot().notes[0]["body"] == note["body"]
    assert store.review_rows() == reviews and client.get("/api/today").json() == plan
    assert client.get("/api/tracks/data/skills").json() == skills and store.extras(A) == []


def test_large_values_judged_before_preview(judging, site):
    import app.main as main
    client, store = site
    p = main.bank.get(ADD)
    value = "书" * 4096
    p.tests = {"examples": [{"args": [value, ""], "expected": value}],
               "hidden": [{"args": [value, "甲"], "expected": value + "甲"}]}
    body = {"code": "def add(a, b): return a + b"}
    accepted = send(client, ADD, body).json()
    assert accepted["verdict"] == "accepted" and accepted["passed"] == 2
    bad = send(client, ADD, {"code": "def add(a,b): return a + ('乙' if b else '')"}).json()
    assert bad["verdict"] == "wrong_answer" and bad["cases"][1]["status"] == "wrong_answer"
    assert store.latest_result(ADD) == {k:v for k,v in bad.items() if k != "submission_id"}
    assert bad["cases"][1]["expected"] == bad["cases"][1]["actual"]
    for c in bad["cases"]:
        for field in ("input", "expected", "actual"):
            assert len(c[field].encode()) < 2048 and ' … （共 ' in c[field]
    assert str(len(value)) in bad["cases"][0]["actual"]


def test_assistance_on_a_variant_rewrites_that_variant(site, monkeypatch):
    from app import db
    client, store = site
    with monkeypatch.context() as clock:
        clock.setattr(db, "now", lambda: stamp(-4))
        send(client, A, {"answer": 1}).raise_for_status()
        clock.setattr(db, "now", lambda: stamp(-3))
        r = store.review_rows()[0]
        send(client, A, dict(answer=1, review_source=A, review_due=r["due"])).raise_for_status()
    item, = client.get("/api/today").json()["reviews"]
    assert item["id"] == B
    send(client, B, dict(answer="A6", ai_lines=1, review_source=A, review_due=item["due"])).raise_for_status()
    retry, = store.review_rows()
    assert retry["rewrite_target"] == B and retry["step"] == 0 and retry["due"] == str(date.today()+timedelta(days=1))
    import app.main as main
    assert main.learning().review_item(retry)["id"] == B


def test_prerequisite_extra_checks_recognizable_skills():
    from app.ai.extra import check_practice_scope
    spec = dict(solution="print(3)", mode="stdio")
    check_practice_scope(spec, "python", {"py.print"})
    with pytest.raises(ValueError, match="py.print"):
        check_practice_scope(spec, "python", {"py.var-arith"})
    with pytest.raises(ValueError, match="sql.where"):
        check_practice_scope({"solution":"SELECT n FROM t WHERE n > 3"}, "sql", {"sql.select-basic"})


def test_session_uses_visible_reviews_and_one_frontier(site, monkeypatch):
    from app import db
    client, store = site
    url = "/api/session-plan"
    assert [p["id"] for p in client.get(url, params={"tab": "sql", "size": 8}).json()] == [A, B]
    old = stamp(-2)
    with monkeypatch.context() as clock:
        clock.setattr(db, "now", lambda: old)
        send(client, A, {"answer": 1}).raise_for_status()
    store.add_submission(problem_id=ADD, track="python", kind="submit", code="",
                         result={"verdict": "wrong_answer"}, elapsed_ms=500, hints_used=0)
    review, = client.get("/api/today").json()["reviews"]
    # 默认接着进度出新题，不把到期复习塞在前面
    assert [p["id"] for p in client.get(url, params={"tab": "sql"}).json()] == [B]
    sql = client.get(url, params={"tab": "sql", "warmup": True}).json()
    assert sql[0] == review and [p["id"] for p in sql[1:]] == [B]
    python = client.get(url, params={"tab": "python", "size": 3, "warmup": True}).json()
    assert python[0] == review and [p["id"] for p in python[1:]] == ["py-0a-004-fill-return"]
