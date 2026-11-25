"""用临时库检查长期笔记、开关和聊天写回事务。"""

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import date, timedelta
from threading import Event

import pytest
from fastapi.testclient import TestClient

from app import events, main
from app.ai import memory
from app.ai.provider import AIError, FakeProvider
from app.db import Store


def note(name, **fields):
    return {"name": name, "note": {"type": "feedback", "description": "一次讲一步", "scope": None,
                                   "as_of": "2026-11-24", "body": "学生说步骤太多会忘，等他试过再继续。"} | fields}


def save(store, *ops):
    store.add_chat("原题", "assistant", "好。", snapshot=store.memory_snapshot(), memory=list(ops))


def test_existing_database_and_settings_api(client, monkeypatch, tmp_path):
    path = tmp_path / "old.db"
    old = Store(path)
    old.set_limit(7)
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE memory_notes")
    store = Store(path)
    monkeypatch.setattr(main, "store", store)
    assert store.daily_limit() == 7 and store.journal.machine == old.journal.machine
    url = "/api/memory/settings"
    assert client.get(url).json() == {"enabled": True}
    assert not any(e["payload"]["row"].get("key") == "memory_enabled" for e in store.pending_events())
    save(store, note("one-step"))
    assert client.put(url, json={"enabled": False}).json() == {"enabled": False}
    assert client.get(url).json() == {"enabled": False} and store.memory_snapshot() is None
    assert client.put(url, json={"enabled": True}).json() == {"enabled": True}
    assert store.memory_snapshot().notes[0]["name"] == "one-step"
    client.put(url, json={"enabled": False}).raise_for_status()
    assert client.post("/api/memory/clear", json={}).json() == {"ok": True}
    assert not Store(path).memory_enabled()
    client.put(url, json={"enabled": True}).raise_for_status()
    assert store.memory_snapshot().notes == []
    assert list(store.memory_snapshot().versions) == ["one-step"]
    tombstone = [e["payload"] for e in store.pending_events() if e["type"] == "memory_notes"][-1]
    assert tombstone == {"entity": '["one-step"]', "removed": False, "row": {
        "name": "one-step", "type": None, "description": None, "scope": None, "as_of": None, "body": None, "deleted": 1}}


@pytest.mark.parametrize("field,limit", [("name", 32), ("description", 40), ("body", 160)])
def test_lengths_only_skip_overlong_operation(tmp_path, field, limit):
    store = Store(tmp_path / "db")
    items = [note("字" * n) if field == "name" else note(str(n), **{field: "字" * n})
             for n in (limit + 1, limit)]
    save(store, *items)
    row, = store.memory_snapshot().notes
    assert row[field] == "字" * limit and len(store.chat("原题")) == 1


@pytest.mark.parametrize("change", ["clear", "switch", "sync_switch"])
def test_inflight_new_name_after_clear_or_switch(tmp_path, change):
    store = Store(tmp_path / "db")
    snapshot = store.memory_snapshot()
    if change == "clear":
        store.clear_memory()
    else:
        source = Store(tmp_path / "other/db") if change == "sync_switch" else store
        source.set_memory_enabled(False)
        source.set_memory_enabled(True)
        if change == "sync_switch":
            store.import_events(source.pending_events())
    store.add_chat("原题", "assistant", "旧答复", snapshot=snapshot, memory=[note("old")])
    save(store, note("fresh"))
    assert [n["name"] for n in store.memory_snapshot().notes] == ["fresh"]
    assert [m["content"] for m in store.chat("原题")] == ["旧答复", "好。"]


def test_per_name_version_includes_deleted_rows_and_sync(tmp_path):
    store = Store(tmp_path / "a/db")
    other = Store(tmp_path / "b/db")
    save(store, note("old"), note("revive"))
    save(store, {"name": "revive", "note": None})
    snapshot = store.memory_snapshot()
    other.import_events(store.pending_events())
    save(other, {"name": "old", "note": None}, note("new", body="另一台写的"))
    store.import_events(other.pending_events())
    store.add_chat("原题", "assistant", "继续", snapshot=snapshot, memory=[note("old"), note("revive")])
    store.add_chat("原题", "assistant", "继续", snapshot=snapshot, memory=[note("new"), note("fresh")])
    assert {r["name"]: r["body"] for r in store.memory_snapshot().notes} == {
        "revive": note("revive")["note"]["body"], "fresh": note("fresh")["note"]["body"], "new": "另一台写的"}


def test_same_name_order_and_atomic_reply(tmp_path):
    store = Store(tmp_path / "db")
    save(store, note("one-step"), {"name": "one-step", "note": None})
    assert store.memory_snapshot().notes == []
    records = store.pending_events()
    assert [e["payload"]["row"]["deleted"] for e in records if e["type"] == "memory_notes"] == [0, 1]
    with sqlite3.connect(store.path) as conn:
        conn.execute("""CREATE TRIGGER reject_note BEFORE INSERT ON memory_notes
                        BEGIN SELECT RAISE(ABORT, '写入失败'); END""")
    with pytest.raises(sqlite3.IntegrityError, match="写入失败"):
        save(store, note("error"))
    assert len(store.chat("原题")) == 1 and store.pending_events() == records


BOOK = "data-0-001-book-key"
SHELF = "data-0-002-shelf"


@pytest.fixture
def review_site(monkeypatch, tmp_path):
    store = Store(tmp_path / "study.db")
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(main, "_review_thread", None)
    yield TestClient(main.app), store
    if main._review_thread:
        main._review_thread.join(5)
        assert not main._review_thread.is_alive()


def wait_review():
    main._review_thread.join(5)
    assert not main._review_thread.is_alive()


def review_meta(store, key):
    with sqlite3.connect(store.path) as conn:
        return events.meta(conn, "memory_review_" + key)


def next_day(monkeypatch):
    class Tomorrow(date):
        @classmethod
        def today(cls):
            return date.today() + timedelta(days=1)

    monkeypatch.setattr(main, "date", Tomorrow)
    return Tomorrow.today()


def test_map_only_reviews_new_local_help_when_agent_available(review_site, fake_agents, monkeypatch, tmp_path):
    client, store = review_site
    store.record_help(BOOK, solution=False, author=1)
    with sqlite3.connect(store.path) as conn:
        conn.execute("DELETE FROM sync_meta WHERE key='memory_review_cursor'")
    store = Store(store.path)  # 模拟已有交卷和求助记录的机器首次升级
    monkeypatch.setattr(main, "store", store)
    other = Store(tmp_path / "other/code_dojo.db")
    other.record_help(SHELF, solution=True)
    store.import_events(other.pending_events())
    assert store.import_legacy(other.path.parent) > 0
    client.post(f"/api/problems/{BOOK}/run", json={"answer": 0}).raise_for_status()
    fake = FakeProvider([{"memory": []}])
    with monkeypatch.context() as patch:
        patch.setattr(main, "available_agents", lambda _: [{"id": "claude"}])
        patch.setattr(main, "providers", {"claude": fake})
        client.get("/api/tracks").raise_for_status()
        assert not fake.calls and not review_meta(store, "day")

    monkeypatch.setattr(main.bank.get(BOOK).meta, "hints", ["找编号"])
    client.post(f"/api/problems/{BOOK}/hints/1", json={}).raise_for_status()
    client.get("/api/tracks").raise_for_status()  # 实际配置为 off
    assert not review_meta(store, "day") and main._review_thread is None
    with monkeypatch.context() as patch:
        missing = str(tmp_path / "未安装的助教")
        patch.setattr(main, "settings", replace(main.settings, ai_provider="claude", claude_bin=missing, codex_bin=missing))
        client.get("/api/tracks").raise_for_status()
        assert not review_meta(store, "day") and main._review_thread is None
    store.set_memory_enabled(False)
    fake_agents(codex=fake)
    store.record_help(BOOK, solution=False)
    client.get("/api/tracks").raise_for_status()
    assert not fake.calls and not review_meta(store, "day")
    store.set_memory_enabled(True)
    client.get("/api/tracks").raise_for_status()
    assert not fake.calls and not review_meta(store, "day")
    client.post(f"/api/problems/{BOOK}/hints/1", json={}).raise_for_status()
    client.get("/api/tracks").raise_for_status()
    wait_review()
    call, = fake.calls
    evidence = call["prompt"].split("本机练习证据\n")[1].splitlines()
    assert len(evidence) == 1 and all(s in evidence[0] for s in (BOOK, "求助 提示", "data.column-key"))
    assert call["effort"] == "low"
    assert review_meta(store, "cursor") == [e for e in store.pending_events() if e["type"] == "study_help"][-1]["timestamp"]
    store.record_help(SHELF, solution=True)
    client.get("/api/tracks").raise_for_status()
    assert len(fake.calls) == 1 and review_meta(store, "day") == date.today().isoformat()


def test_four_submits_backlog_and_summary(review_site, monkeypatch, fake_agents):
    from app import db
    client, store = review_site
    fake = FakeProvider([{"memory": []}, {"memory": []}])
    fake_agents(claude=fake)
    for name, kind, scope in [("skill", "progress", "data.column-key"), ("track", "progress", "data"),
                              ("other", "progress", "python"), ("learner", "learner", "data.column-key")]:
        save(store, note(name, type=kind, scope=scope, body=name + "的正文"))
    for _ in range(25):
        store.record_help(SHELF, solution=False, author=1)
    monkeypatch.setattr(db, "now", lambda: "2026-11-19T12:00:00+00:00")
    for answer in (0, 0, 1):
        client.post(f"/api/problems/{BOOK}/submit", json={"answer": answer}).raise_for_status()
    assert not fake.calls
    client.post(f"/api/problems/{SHELF}/submit", json={"answer": "私人的原始答案", "ai_lines": 7}).raise_for_status()
    wait_review()
    client.get("/api/tracks").raise_for_status()
    first, = fake.calls
    lines = first["prompt"].split("本机练习证据\n")[1].splitlines()
    assert len(lines) == 24 and all("求助 提示" in line and SHELF in line for line in lines)
    assert "skill的正文" in first["prompt"] and "track的正文" in first["prompt"]
    assert "other 一次讲一步" in first["prompt"] and "learner 一次讲一步" in first["prompt"]
    assert "other的正文" not in first["prompt"] and "learner的正文" not in first["prompt"]
    tomorrow = next_day(monkeypatch)
    client.get("/api/tracks").raise_for_status()
    wait_review()
    second = fake.calls[1]["prompt"]
    lines = second.split("本机练习证据\n")[1].splitlines()
    assert len(lines) == 5
    assert all(BOOK in line and "2026-11-19 wrong_answer 独立 DM05" in line for line in lines[:2])
    assert "accepted 独立" in lines[2] and "求助 提示" in lines[3] and "wrong_answer 提示 AI改码" in lines[4]
    assert "私人的原始答案" not in second and "DM04" not in second
    assert max(map(len, lines)) <= 100 and len("\n".join(lines)) <= 2400
    assert store.claim_memory_review((tomorrow + timedelta(days=1)).isoformat(), after_submit=False) is None


def test_failure_retries_same_batch_after_restart(review_site, monkeypatch, fake_agents):
    client, store = review_site
    store.record_help(BOOK, solution=True)
    before = review_meta(store, "cursor")

    def fail(system, prompt):
        raise AIError("本次失败")

    fake = FakeProvider(fail)
    fake_agents(codex=fake)
    client.get("/api/tracks").raise_for_status()
    wait_review()
    assert review_meta(store, "cursor") == before and "求助 题解" in fake.calls[0]["prompt"]
    restarted = Store(store.path)
    assert restarted.claim_memory_review(date.today().isoformat(), after_submit=False) is None
    monkeypatch.setattr(main, "store", restarted)
    next_day(monkeypatch)
    fake.responses = [{"memory": []}]
    client.get("/api/tracks").raise_for_status()
    wait_review()
    assert len(fake.calls) == 2 and fake.calls[0]["prompt"] == fake.calls[1]["prompt"]
    assert review_meta(restarted, "cursor") > before


@pytest.mark.parametrize("during", ["chat", "clear", "other_connection_clear", "switch", "sync_switch"])
def test_review_in_flight(review_site, fake_agents, during, tmp_path, monkeypatch):
    client, store = review_site
    entered, release = Event(), Event()
    progress = note("same", type="progress", scope="data.column-key", as_of=date.today().isoformat())
    save(store, progress)
    store.record_help(BOOK, solution=False)

    def reply(system, prompt):
        entered.set()
        assert release.wait(10)
        return {"memory": [progress, note("separate", type="progress")]}

    fake = FakeProvider(reply)
    fake_agents(codex=fake)
    if during == "chat":
        for answer in (0, 0, 1, 1):
            client.post(f"/api/problems/{BOOK}/submit", json={"answer": answer}).raise_for_status()
    else:
        client.get("/api/tracks").raise_for_status()
    try:
        assert entered.wait(5)
        if during == "chat":
            save(store, note("same", body="聊天先写回"))
        elif during == "clear":
            client.post("/api/memory/clear", json={}).raise_for_status()
        elif during == "other_connection_clear":
            Store(store.path).clear_memory()
        else:
            source = Store(tmp_path / "other/db") if during == "sync_switch" else store
            source.set_memory_enabled(False)
            store.record_help(BOOK, solution=True)
            source.set_memory_enabled(True)
            if source is not store:
                store.import_events(source.pending_events())
        cursor = review_meta(store, "cursor")
        store.record_help(SHELF, solution=False, author=1)
        tomorrow = next_day(monkeypatch)
        client.get("/api/tracks").raise_for_status()  # 即便跨了午夜，也要等在途任务结束
        assert len(fake.calls) == 1
    finally:
        release.set()
        wait_review()
    bodies = {n["name"]: n["body"] for n in store.memory_snapshot().notes}
    if during == "chat":
        assert bodies == {"same": "聊天先写回", "separate": progress["note"]["body"]}
    else:
        assert bodies == ({} if during.endswith("clear") else {"same": progress["note"]["body"]})
        assert review_meta(store, "cursor") == cursor
    batch = store.claim_memory_review(tomorrow.isoformat(), after_submit=False)
    event, = batch.evidence
    assert event.problem_id == SHELF and event.outcome == "求助 提示"


def test_review_progress_types_dates_and_atomic_cursor(tmp_path):
    store = Store(tmp_path / "db")
    save(store, note("preference"), note("recent", type="progress", as_of="2099-01-01"))
    save(store, note("solved", type="progress", as_of="2020-03-02"), note("ongoing", type="progress", as_of="2020-03-02"))
    store.record_help(BOOK, solution=False)
    batch = store.claim_memory_review("2026-11-24", after_submit=False)
    cursor = review_meta(store, "cursor")
    with sqlite3.connect(store.path) as conn:
        conn.execute("""CREATE TRIGGER reject_cursor BEFORE INSERT ON sync_meta WHEN NEW.key='memory_review_cursor'
                        BEGIN SELECT RAISE(ABORT,'游标写入失败'); END""")
    with pytest.raises(sqlite3.IntegrityError, match="游标写入失败"):
        store.finish_memory_review(batch, [note("rolled-back", type="progress")])
    assert review_meta(store, "cursor") == cursor
    with sqlite3.connect(store.path) as conn:
        conn.execute("DROP TRIGGER reject_cursor")
    store.finish_memory_review(batch, [note("new-learner", type="learner"), note("preference", type="progress")])
    assert review_meta(store, "cursor") == batch.through
    for day, operations in enumerate([
        [{"name": "preference", "note": None}, note("recent", type="progress")],
        [{"name": "recent", "note": None}, {"name": "solved", "note": None}],
        [note("ongoing", type="progress", body="下次换一组数据再试", as_of=date.today().isoformat())],
    ], 25):
        store.record_help(BOOK, solution=False)
        batch = store.claim_memory_review(f"2026-11-{day}", after_submit=False)
        store.finish_memory_review(batch, operations)
    notes = {n["name"]: n for n in store.memory_snapshot().notes}
    assert notes.keys() == {"preference", "recent", "ongoing"}
    assert notes["preference"]["type"] == "feedback" and notes["recent"]["as_of"] == "2099-01-01"
    assert notes["ongoing"]["body"] == "下次换一组数据再试"


def test_review_maps_deleted_extra_and_wins_before_chat(review_site, fake_agents):
    client, store = review_site
    extra = store.create_extra(BOOK, "练一下前置技能", "py.var-arith")
    store.record_help(extra["id"], solution=False, author=1)
    store.delete_extra(BOOK, extra["seq"])
    chat = store.memory_snapshot()
    fake = FakeProvider([{"memory": [note("focus", type="progress", body="回顾先写回", scope="py.var-arith")]}])
    fake_agents(codex=fake)
    client.get("/api/tracks").raise_for_status()
    wait_review()
    line = fake.calls[0]["prompt"].split("本机练习证据\n")[1]
    assert BOOK in line and "py.var-arith" in line and "data.column-key" not in line and "x-" not in line
    store.add_chat(BOOK, "assistant", "继续。", snapshot=chat, memory=[note("focus"), note("preference")])
    assert {n["name"]: n["body"] for n in store.memory_snapshot().notes} == {
        "focus": "回顾先写回", "preference": note("preference")["note"]["body"]}


def test_concurrent_claim_and_full_batch_budget(tmp_path):
    store = Store(tmp_path / "db")
    other = Store(store.path)
    pid = "algo-4-078-find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree"
    for _ in range(24):
        store.record_help(pid, solution=False)
    with ThreadPoolExecutor(max_workers=2) as pool:
        batches = list(pool.map(lambda db: db.claim_memory_review("2026-11-24", after_submit=False), (store, other)))
    batch, = [batch for batch in batches if batch]
    skills = ["algo.minimum-spanning-tree", "algo.disjoint-set", "algo.graph-traversal", "algo.sorting"]
    for event in batch.evidence:
        event.track, event.skills = "algo", skills
    batch.snapshot.notes = [note(str(i), type="progress", scope=skills[0], body="观" * 160)["note"] | {"name": str(i)}
                            for i in range(16)]
    prompt = memory.review_prompt(batch, {})
    context, evidence = prompt.split("\n本机练习证据\n")
    index, bodies = context.split("\n相关正文")
    assert index.count("一次讲一步") == 16 and 0 < len("\n相关正文" + bodies) <= 1000
    lines = evidence.splitlines()
    assert len(lines) == 24 and max(map(len, lines)) <= 100 and len(evidence) <= 2400
    assert all("algo-4-078" in line and skills[0] in line and set(line.split()[5:]) <= set(skills) for line in lines)
