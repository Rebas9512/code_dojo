"""以独立 bare 测试仓库往返真实 Git；所有文件和提交均在 pytest 临时目录。"""

import json
import sqlite3
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app import db
from app.db import Store
from app.sync import ProgressSync, git


def submit(store, pid="题", **kw):
    return store.add_submission(**(dict(problem_id=pid, track="data", kind="submit", code="解答",
                                        elapsed_ms=3210, result={"verdict": "accepted", "passed": 1, "total": 1},
                                        hints_used=0, counted=True) | kw))


@pytest.fixture
def machines(tmp_path):
    remote = tmp_path / "远端.git"
    subprocess.run(["git", "init", "--bare", str(remote)], cwd=tmp_path, check=True, capture_output=True)
    return [ProgressSync(Store(tmp_path / name / "code_dojo.db"), str(remote)) for name in ("甲", "乙")]


def exchange(sync):
    state = sync.sync()
    assert state["error"] == ""
    assert state["last_sync"] and state["pending"] == 0
    return state


def test_two_machines_and_repeated_import(machines, monkeypatch):
    a, b = machines
    yesterday = date.today() - timedelta(days=1)
    with monkeypatch.context() as clock:
        clock.setattr(db, "now", lambda: yesterday.isoformat() + "T12:00:00+00:00")
        submit(a.store, ai_lines=2, hints_used=1)
    a.store.set_limit(7)
    msg = a.store.add_chat("题", "assistant", "试试这里", [{"old": "甲", "new": "乙"}], ["重试"])
    exchange(a)
    exchange(b)
    assert b.store.study_rows() == a.store.study_rows()
    assert b.store.submissions("题")[0]["code"] == "解答"
    assert b.store.latest_result("题") == {"verdict": "accepted", "passed": 1, "total": 1}
    assert a.store.review_rows() == b.store.review_rows()
    assert a.store.chat("题") == b.store.chat("题")
    assert b.store.daily_limit() == 7
    due = b.store.review_rows()[0]["due"]
    submit(b.store, kind="review", review_source="题", review_due=due)
    b.store.mark_applied("题", msg["id"])
    submit(a.store, "甲做的")
    submit(b.store, "乙做的")
    with ThreadPoolExecutor(2) as pool:
        list(pool.map(exchange, machines))
    exchange(a)
    exchange(b)
    for store in (a.store, b.store):
        assert len(store.study_rows()) == 4
        assert store.chat("题")[0]["applied"]
        assert store.submissions("题")[0]["kind"] == "review"
        assert any(r["result"] == "passed" and r["last_reviewed"] for r in store.review_rows())
    a.store.clear_chat("题")
    exchange(a)
    exchange(b)
    assert b.store.chat("题") == []
    assert len(a.store.study_rows()) == len(b.store.study_rows()) == 4
    files = list(a.root.glob("*/*.jsonl"))
    assert {f.parent.name for f in files} == {a.store.journal.machine, b.store.journal.machine}
    for f in files:
        rows = [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines()]
        assert len({r["id"] for r in rows}) == len(rows)
        assert all(r["machine"] == f.parent.name and r["timestamp"][:7] == f.stem for r in rows)


def test_offline_extras_collide_and_remain_playable(machines, monkeypatch):
    from app import main
    a, b = machines
    parent = "data-0-001-book-key"
    for sync, title in zip(machines, ["甲题", "乙题"]):
        extra = sync.store.create_extra(parent, "再来一道")
        assert extra["id"] == "x-1"
        spec = {"title": title, "statement": "写出编号", "mode": "inspect", "explain": "读取第一列。",
                "data": [{"kind": "csv", "content": "编号\nA1"}],
                "answer": {"type": "short", "accept": ["A1"]}}
        sync.store.finish_extra(1, spec, ["已验证"])
        submit(sync.store, "x-1", code=title)
        sync.store.record_help("x-1", solution=True)
    exchange(a)
    exchange(b)
    exchange(a)
    for sync in machines:
        extras = sync.store.extras(parent)
        assert len(extras) == 2
        assert {e["seq"] for e in extras} == {1, 2}
        for e in extras:
            assert e["spec"]["answer"]["accept"] == ["A1"]
            assert e["spec"]["title"] == sync.store.submissions(e["id"])[0]["code"]
            assert any(r["rewrite_target"] == e["id"] for r in sync.store.review_rows())
    imported = next(e for e in b.store.extras(parent) if e["title"] == "甲题")
    monkeypatch.setattr(main, "store", b.store)
    monkeypatch.setattr(main, "progress_sync", b)
    client = TestClient(main.app)
    url = f"/api/problems/{imported['id']}"
    assert client.get(url).json()["title"] == "甲题"
    assert client.post(url + "/submit", json={"answer": "A1"}).json()["verdict"] == "accepted"
    a.store.delete_extra(parent, 1)
    exchange(a)
    exchange(b)
    assert [e["title"] for e in b.store.extras(parent)] == ["乙题"]


def test_failure_offline_then_retry(machines):
    a, _ = machines
    store = a.store
    submit(store)
    assert len(list((store.path.parent / "events").glob("*/*.jsonl"))) == 1
    assert not ProgressSync(store, "").sync()["enabled"]
    unavailable = ProgressSync(store, str(store.path.parent / "不存在"))
    state = unavailable.sync()
    assert state["error"] and state["pending"] and not state["last_sync"]
    exchange(a)
    assert store.sync_status()[0] == 0
    assert Store(store.path).journal.machine == store.journal.machine


def test_conflicting_month_keeps_both_lines(machines, tmp_path):
    a, _ = machines
    submit(a.store, "前")
    exchange(a)
    # 人为制造同一机器目录、同一月份的追加冲突。
    clone = tmp_path / "另一份克隆"
    git(tmp_path, "clone", "--", a.repo, str(clone))
    file, = clone.glob("*/*.jsonl")
    row = json.loads(file.read_text(encoding="utf-8").splitlines()[0])
    from uuid import uuid4
    row.update(id=str(uuid4()), type="settings", payload={
        "entity": '["daily_limit"]', "row": {"key": "daily_limit", "value": 11}, "removed": False})
    with file.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    git(clone, "add", "--", a.store.journal.machine)
    git(clone, "commit", "-m", "测试中同时追加的事件")
    git(clone, "push")
    submit(a.store, "后")
    exchange(a)
    assert a.store.daily_limit() == 11
    assert len(a.store.study_rows()) == 2
    assert len((a.root / file.relative_to(clone)).read_text(encoding="utf-8").splitlines()) == 5


def test_legacy_read_only_snapshot_twice(machines, tmp_path):
    a, b = machines
    old = tmp_path / "旧库/code_dojo.db"
    old.parent.mkdir()
    with sqlite3.connect(old) as conn:
        conn.execute("""CREATE TABLE submissions (id INTEGER PRIMARY KEY,problem_id TEXT,track TEXT,kind TEXT,
            code TEXT,verdict TEXT,passed INTEGER,total INTEGER,elapsed_ms INTEGER,hints_used INTEGER,
            result_json TEXT,created_at TEXT)""")
        conn.execute("""INSERT INTO submissions VALUES (9,'旧题','data','submit','旧解','accepted',1,1,321,0,
            '{"verdict":"accepted"}','2020-01-02T12:00:00+00:00')""")
    original = old.read_bytes()
    submit(a.store, "旧题", code="今次未过", result={"verdict": "wrong_answer"})
    assert a.store.import_legacy(old.parent) == 1
    assert a.store.import_legacy(old.parent) == 0
    assert old.read_bytes() == original
    a.store.initialize_reviews({"旧题"})
    assert a.store.review_rows()[0]["due"] == "2020-01-03"
    assert a.store.review_rows()[0]["result"] == "new"
    exchange(a)
    exchange(b)
    assert b.store.import_legacy(old.parent) == 0
    assert [r["code"] for r in b.store.submissions("旧题")] == ["今次未过", "旧解"]


def test_sync_routes_and_accepted_trigger(tmp_path, monkeypatch):
    from app import main
    sync = ProgressSync(Store(tmp_path / "code_dojo.db"), "")
    with monkeypatch.context() as m:
        m.setattr(main, "store", sync.store)
        m.setattr(main, "progress_sync", sync)
        m.setattr(sync, "request", Mock())
        client = TestClient(main.app)
        assert client.get("/api/sync").json()["enabled"] is False
        url = "/api/problems/data-0-001-book-key/submit"
        client.post(url, json={"answer": 0}).raise_for_status()
        sync.request.assert_not_called()
        client.post(url, json={"answer": 1}).raise_for_status()
        sync.request.assert_called_once()
        assert client.post("/api/sync", json={}).json()["pending"] > 0


def test_monthly_export_retries_after_partial_write(tmp_path, monkeypatch):
    from app import events
    store = Store(tmp_path / "code_dojo.db")
    with monkeypatch.context() as broken:
        broken.setattr(events.os, "fsync", Mock(side_effect=OSError("磁盘暂不可用")))
        submit(store)
    records = store.pending_events()
    file, = (tmp_path / "events").glob("*/*.jsonl")
    lines = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == len(records) == 2
    assert {e["id"] for e in lines} == {e["id"] for e in records}
    assert len(store.submissions("题")) == 1
    file.write_bytes(file.read_bytes()[:15])
    Store(store.path)
    assert [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()] == lines


def test_timer_and_exit_flush(machines, monkeypatch):
    import time
    from app import sync as service
    a, b = machines
    assert service.INTERVAL == 600
    monkeypatch.setattr(service, "INTERVAL", .05)
    a.start()
    try:
        a.store.set_limit(6)
        deadline = time.monotonic() + 15
        while a.status()["pending"] and time.monotonic() < deadline:
            time.sleep(.05)
        exchange(b)
        assert b.store.daily_limit() == 6
        a.store.set_limit(8)
    finally:
        a.close()
    exchange(b)
    assert b.store.daily_limit() == 8


def test_offline_deletion_survives_late_edits(machines):
    a, b = machines
    message = a.store.add_chat("题", "assistant", "修改", [{"old": "旧", "new": "新"}])
    extra = a.store.create_extra("题", "再来一道")
    exchange(a)
    exchange(b)
    b.store.clear_chat("题")
    b.store.delete_extra("题", 1)
    a.store.mark_applied("题", message["id"])
    a.store.finish_extra(extra["row_id"], {"title": "新变式"}, [])
    exchange(a)
    exchange(b)
    exchange(a)
    for sync in machines:
        assert sync.store.chat("题") == []
        assert sync.store.extras("题") == []
