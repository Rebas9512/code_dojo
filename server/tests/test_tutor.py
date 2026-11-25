"""AI 助教（共享编辑框）：用 FakeProvider 代替真 AI，测上下文组装、修改定位、重试和接口。"""

from datetime import date
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.ai import tutor
from app.ai.memory import MemorySnapshot, format_context
from app.ai.provider import FakeProvider
from app.problems import load_problem

FIXTURES = Path(__file__).parent / "fixtures" / "problems" / "python" / "0A"
ADD = FIXTURES / "py-0a-001-add"
PREDICT = FIXTURES / "py-0a-003-predict-loop"
STARTER = "def add(a: int, b: int) -> int:\n    pass\n"


def ask(provider, problem_dir=ADD, **kw):
    args = dict(code=STARTER, answer=None, last_result=None, history=[], message="我卡住了", skill_names={})
    args.update(kw)
    return tutor.ask(provider, load_problem(problem_dir), **args)


def edit(old, new, why="w", target="answer"):
    return {"target": target, "old": old, "new": new, "why": why}


def memory_note(name, kind="feedback", scope=None, as_of="2026-11-24", body="先给一个动作，等学生试完再继续。"):
    return {"name": name, "note": {"type": kind, "scope": scope, "as_of": as_of, "description": name + "摘要",
                                   "body": body}}


def test_memory_cross_problem_then_clear(client, fake_agents, monkeypatch, tmp_path):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "chat.db")
    monkeypatch.setattr(main, "store", store)
    pref = memory_note("one-step")
    skill = memory_note("trace", "progress", "py.function-return", body="先跟踪返回值。")
    claude = FakeProvider([{"reply": "好，先看一处。", "edits": [], "memory": [pref, skill]}])
    codex = FakeProvider([{"reply": "先看第一行。", "edits": [], "memory": []},
                          {"reply": "长期记忆已关闭。", "edits": []},
                          {"reply": "现在还没有长期笔记。", "edits": [], "memory": []}])
    codex.complete = Mock(wraps=codex.complete)
    fake_agents(claude=claude, codex=codex)
    first = "/api/problems/py-0a-001-add/chat"
    second = "/api/problems/data-0-001-book-key/chat"
    msg = client.post(first, json={"message": "一口气讲三步我会忘记开头"}).json()
    assert msg["assistant"]["content"] == "好，先看一处。"
    assert set(msg) == {"assistant", "user", "new_extra", "deleted_extras"}
    assert "memory" not in msg["assistant"] and "one-step" not in str(client.get(first).json())
    store.add_chat("data-0-001-book-key", "user", "上次的问题")
    payload = {"message": "你记得我什么？", "agent": "codex"}
    client.post(second, json=payload).raise_for_status()
    call = codex.complete.call_args.kwargs
    prompt = call["prompt"]
    assert call["schema"] is tutor.SCHEMA_WITH_MEMORY and "分清学生自述和助教观察" in call["system"]
    assert prompt.index("之前的对话") < prompt.index("## 长期笔记") < prompt.index("学生现在说")
    assert date.today().isoformat() in prompt and "one-step one-step摘要" in prompt
    assert pref["note"]["body"] in prompt and "trace trace摘要" in prompt and skill["note"]["body"] not in prompt
    client.put("/api/memory/settings", json={"enabled": False}).raise_for_status()
    client.post(second, json=payload).raise_for_status()
    call = codex.complete.call_args.kwargs
    assert call["schema"] is tutor.SCHEMA and "长期记忆已关闭" in call["prompt"]
    assert "one-step" not in call["prompt"] and "完整索引" not in call["prompt"]
    assert client.post("/api/memory/clear", json={}).json() == {"ok": True}
    client.put("/api/memory/settings", json={"enabled": True}).raise_for_status()
    client.post(second, json=payload).raise_for_status()
    assert "完整索引（空）" in codex.calls[-1]["prompt"] and "one-step" not in codex.calls[-1]["prompt"]
    assert len(claude.calls) == 1 and len(codex.calls) == 3


def test_memory_index_priority_dates_and_budget():
    notes = [memory_note("track", "progress", "python"), memory_note("goal", "learner"),
             memory_note("new", "progress", "py.function-return"), memory_note("b", "progress", "py.var-arith"),
             memory_note("a", "progress", "py.var-arith"), memory_note("old", "progress", "py.var-arith", "2020-01-01"),
             memory_note("pref", as_of="2019-01-01")]

    def context(ops):
        rows = [op["note"] | {"name": op["name"]} for op in ops]
        snap = MemorySnapshot(rows, {}, None, 0)
        return format_context(snap, "python", {"py.function-return", "py.var-arith"})

    idx, body = context(notes).split("\n相关正文")
    assert idx.splitlines()[2:] == ["[learner]", "goal goal摘要", "[feedback]", "pref pref摘要", "[progress]",
                                    "a a摘要", "b b摘要", "new new摘要", "old old摘要", "track track摘要"]
    assert [line.split("（")[0] for line in body.splitlines()[1:]] == ["pref", "a", "b", "new", "old", "goal", "track"]
    many = [memory_note(f"long-{i:02}", body="字" * 160) for i in range(30)] + [memory_note("tiny", body="短")]
    whole = context(many)
    idx, body = whole.split("\n相关正文")
    assert all(op["name"] + " " + op["note"]["description"] in idx.splitlines() for op in many)
    assert len("\n相关正文" + body) <= 1000 and len(whole) <= 1120 + 74 * len(many)
    assert body.count("字" * 160) == 5 and body.count("字") == 800 and "tiny（" in body


@pytest.mark.parametrize("retry_issue", ["empty", "edit"])
def test_memory_only_final_reply_saved(client, fake_agents, monkeypatch, tmp_path, retry_issue):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "db")
    monkeypatch.setattr(main, "store", store)
    first = {"reply": "", "edits": []} if retry_issue == "empty" else {
        "reply": "看这里", "edits": [edit("没有", "x", target="scratch")]}
    fake = FakeProvider([first | {"memory": [memory_note("discard")]},
                         {"reply": "在草稿看一行。", "edits": [edit("", "print(1)", target="scratch")],
                          "memory": [memory_note("keep")]}])
    fake_agents(claude=fake)
    url = "/api/problems/data-0-001-book-key"
    client.post(url + "/chat", json={"message": "我想先试一个草稿例子"}).raise_for_status()
    assert len(fake.calls) == 2 and len(store.chat("data-0-001-book-key")) == 2
    events = store.pending_events()
    assert [e["payload"]["row"]["name"] for e in events if e["type"] == "memory_notes"] == ["keep"]
    assert all(e["type"] != "study_help" for e in events)
    assert client.post(url + "/submit", json={"answer": 1}).json()["verdict"] == "accepted"
    assert store.submissions("data-0-001-book-key")[0]["hints_used"] == 0


def test_memory_uses_current_extra_skills(client, fake_agents, monkeypatch, tmp_path):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "db")
    monkeypatch.setattr(main, "store", store)
    parent = "py-0a-001-add"
    extra = store.create_extra(parent, "练另一个技能", "py.print")
    store.finish_extra(extra["row_id"], {"title": "输出", "mode": "stdio", "practice_skill": "py.print",
                                         "solution": "print(1)"}, [])
    ops = [memory_note("parent", "progress", "py.function-return", body="原题的进度正文"),
           memory_note("extra", "progress", "py.print", body="附加题的进度正文")]
    store.add_chat(parent, "assistant", "好。", snapshot=store.memory_snapshot(), memory=ops)
    fake = FakeProvider([{"reply": "先看输出。", "edits": [], "memory": []}])
    fake_agents(codex=fake)
    client.post(f"/api/problems/{parent}/chat", json={"message": "先看什么？", "current": extra["id"]}).raise_for_status()
    prompt = fake.calls[0]["prompt"]
    assert "附加题的进度正文" in prompt and "原题的进度正文" not in prompt and "parent parent摘要" in prompt


def test_failed_chat_discards_all_memory(client, fake_agents, monkeypatch, tmp_path):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "db")
    monkeypatch.setattr(main, "store", store)
    fake = FakeProvider([{"reply": "", "edits": [], "memory": [memory_note(name)]} for name in ("one", "two")])
    fake_agents(codex=fake)
    pid = "py-0a-001-add"
    assert client.post(f"/api/problems/{pid}/chat", json={"message": "先讲一步"}).status_code == 502
    assert len(fake.calls) == 2 and store.memory_snapshot().versions == {}
    assert [m["role"] for m in store.chat(pid)] == ["user"]


def test_clear_during_model_call_preserves_reply(client, fake_agents, monkeypatch, tmp_path):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "db")
    monkeypatch.setattr(main, "store", store)

    def respond(system, prompt):
        client.post("/api/memory/clear", json={}).raise_for_status()
        return {"reply": "先看看表头。", "edits": [], "memory": [memory_note("stale")]}

    fake_agents(claude=FakeProvider(respond))
    r = client.post("/api/problems/data-0-001-book-key/chat", json={"message": "这里先看什么？"})
    assert r.json()["assistant"]["content"] == "先看看表头。"
    assert store.memory_snapshot().versions == {}


def test_prompt_has_context_and_soft_rules():
    fake = FakeProvider([{"reply": "想想 pass 做了什么", "edits": []}])
    r = ask(fake, last_result={"verdict": "wrong_answer", "passed": 0, "total": 2,
                               "cases": [{"status": "wrong_answer", "input": {"args": [1, 2]}, "expected": 3, "actual": None}]})
    assert r.reply == "想想 pass 做了什么" and r.edits == [] and r.notes == []
    prompt, system = fake.calls[0]["prompt"], fake.calls[0]["system"]
    assert "  2|     pass" in prompt                    # 带行号的编辑框内容
    assert "return a + b" in prompt                     # 参考解（供 AI 判断）
    assert "wrong_answer" in prompt and "学生现在说\n我卡住了" in prompt
    assert "共用答案和草稿" in system and "不要一次把整个函数写完" in system
    assert "## 草稿（不判题）\n```\n（空）\n```" in prompt
    assert "3 行" not in system                          # 没有硬性行数


def test_long_edit_allowed():
    long_edit = edit("    pass", "    x = a\n    y = b\n    s = x + y\n    t = s\n    return t")
    fake = FakeProvider([{"reply": "我改好了", "edits": [long_edit]}])
    r = ask(fake)
    assert r.edits == [long_edit] and len(fake.calls) == 1   # 不按行数拦截


def test_multiple_edits_apply_in_sequence():
    edits = [edit("    pass", "    total = a + b\n    pass"), edit("    pass", "    return total")]
    fake = FakeProvider([{"reply": "分两步改", "edits": edits}])
    r = ask(fake)
    assert r.edits == edits and len(fake.calls) == 1
    texts, ok, issues = tutor.apply_edits({"answer": STARTER, "scratch": ""}, r.edits)
    assert texts["answer"] == "def add(a: int, b: int) -> int:\n    total = a + b\n    return total\n" and issues == []


def test_unlocatable_edit_retries_then_succeeds():
    fake = FakeProvider([
        {"reply": "改这里", "edits": [edit("2| pass", "return a + b")]},     # 带了行号，找不到
        {"reply": "改这里", "edits": [edit("    pass", "    return a + b")]},
    ])
    r = ask(fake)
    assert r.edits[0]["old"] == "    pass" and len(fake.calls) == 2
    assert "找不到" in fake.calls[1]["prompt"] and r.notes


def test_only_unlocatable_edits_dropped_after_retry():
    bad = {"reply": "改两处", "edits": [edit("nope", "x"), edit("    pass", "    return a + b")]}
    fake = FakeProvider([dict(bad), dict(bad)])
    r = ask(fake)
    assert r.edits == [edit("    pass", "    return a + b")] and len(r.notes) == 2


def test_predict_edits_target_answer_text():
    fake = FakeProvider([{"reply": "第二行接着写", "edits": [edit("1 1", "1 1\n2 3")]}])
    r = ask(fake, PREDICT, code="", answer="1 1", message="帮我把第二行加上")
    assert r.edits == [edit("1 1", "1 1\n2 3")] and len(fake.calls) == 1
    assert "  1| 1 1" in fake.calls[0]["prompt"]


def test_empty_old_means_append():
    fake = FakeProvider([{"reply": "先写第一行", "edits": [edit("", "1 1")]}])
    r = ask(fake, PREDICT, code="", answer="", message="帮我写第一行")
    assert r.edits == [edit("", "1 1")] and len(fake.calls) == 1
    assert tutor.apply_edits({"answer": ""}, r.edits)[0]["answer"] == "1 1"
    assert tutor.apply_edits({"answer": "a"}, r.edits)[0]["answer"] == "a\n1 1"


def test_mixed_edits_use_each_targets_latest_text():
    targets = {"answer": "x = 1", "scratch": "x = 1\naaa"}
    edits = [edit("x = 1", "value = 2", target="scratch"), edit("x = 1", "return 1"),
             edit("value = 2", "value = 3", target="scratch"), edit("", "print(value)", target="scratch")]
    out = {"reply": "分开改好了", "edits": edits}
    assert tutor.check(out, targets) == []
    assert tutor.apply_edits(targets, edits) == (
        {"answer": "return 1", "scratch": "value = 3\naaa\nprint(value)"}, [0, 1, 2, 3], [])
    for old in ("return 1", "aa"):
        assert tutor.check(out | {"edits": [*edits, edit(old, "z", target="scratch")]}, targets)


def test_scratch_chat_preserves_independent_submission(client, fake_agents, monkeypatch, tmp_path):
    from app import main
    from app.db import Store

    store = Store(tmp_path / "chat.db")
    monkeypatch.setattr(main, "store", store)
    pid = "data-0-001-book-key"
    url = f"/api/problems/{pid}"
    scratch = "a = 2\nb = 3"
    change = edit("b = 3", "b = 3\nprint(a + b)", target="scratch")
    fake = FakeProvider([{"reply": "在草稿里打印和。", "edits": [change]}])
    fake_agents(claude=fake)
    store.add_chat(pid, "assistant", "旧回复", [{"old": "x", "new": "y", "why": "示例"}])
    assert client.get(url + "/chat").json()[0]["edits"] == [edit("x", "y", "示例")]
    response = client.post(url + "/chat", json={"message": "在草稿里打印", "scratch": scratch})
    assert response.json()["assistant"]["edits"] == [change]
    assert "## 草稿（不判题）\n```\n  1| a = 2\n  2| b = 3\n```" in fake.calls[0]["prompt"]
    assert "当时改了答案" in fake.calls[0]["prompt"]
    assert client.post(url + "/submit", json={"answer": 1}).json()["verdict"] == "accepted"
    row, = store.submissions(pid)
    assert row["ai_lines"] == row["hints_used"] == 0


@pytest.fixture
def chat_client(client, fake_agents):
    fake = FakeProvider(lambda system, prompt: (
        {"reply": "我把 pass 换成了 return", "edits": [edit("    pass", "    return a + b", "要返回结果")]}
        if "帮我补" in prompt.split("学生现在说")[-1] else {"reply": "先想想 pass 会返回什么？", "edits": []}
    ))
    fake_agents(claude=fake)
    client.delete("/api/problems/py-0a-001-add/chat")
    return client


def test_chat_api_flow(chat_client):
    c = chat_client
    r1 = c.post("/api/problems/py-0a-001-add/chat", json={"message": "我卡住了", "code": STARTER}).json()
    assert r1["assistant"]["edits"] == []
    r2 = c.post("/api/problems/py-0a-001-add/chat", json={"message": "帮我补一下", "code": STARTER}).json()
    msg = r2["assistant"]
    assert msg["edits"][0]["new"] == "    return a + b" and msg["applied"] is False
    history = c.get("/api/problems/py-0a-001-add/chat").json()
    assert [m["role"] for m in history] == ["user", "assistant", "user", "assistant"]
    assert c.post(f"/api/problems/py-0a-001-add/chat/{msg['id']}/applied").json() == {"ok": True}
    assert c.get("/api/problems/py-0a-001-add/chat").json()[-1]["applied"] is True
    c.delete("/api/problems/py-0a-001-add/chat")
    assert c.get("/api/problems/py-0a-001-add/chat").json() == []


def test_assisted_submission_status(chat_client, monkeypatch, tmp_path):
    import app.main as main
    from app.db import Store

    monkeypatch.setattr(main, "store", Store(tmp_path / "db.sqlite"))  # 独立的空库，不受其他测试的提交影响
    sol = (FIXTURES / "py-0a-002-print-sum" / "solution.py").read_text(encoding="utf-8")
    r = chat_client.post("/api/problems/py-0a-002-print-sum/submit", json={"code": sol, "ai_lines": 2}).json()
    assert r["verdict"] == "accepted"
    status = {p["id"]: p["status"] for p in chat_client.get("/api/tracks/python/problems").json()}
    assert status["py-0a-002-print-sum"] == "assisted"
    chat_client.post("/api/problems/py-0a-002-print-sum/submit", json={"code": sol, "ai_lines": 0})
    status = {p["id"]: p["status"] for p in chat_client.get("/api/tracks/python/problems").json()}
    assert status["py-0a-002-print-sum"] == "solved"


def test_chat_disabled_returns_503(client):
    assert client.post("/api/problems/py-0a-001-add/chat", json={"message": "hi"}).status_code == 503


@pytest.mark.parametrize("field", ["code", "scratch"])
def test_chat_editor_length_limit(client, fake_agents, field):
    fake_agents(claude=FakeProvider([{"reply": "收到", "edits": []}]))
    url = "/api/problems/py-0a-001-add/chat"
    text = "a" * 100_000
    assert client.post(url, json={"message": "看一下", field: text}).status_code == 200
    assert client.post(url, json={"message": "看一下", field: text + "a"}).status_code == 422
