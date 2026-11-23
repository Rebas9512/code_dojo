"""AI 助教（共享编辑框）：用 FakeProvider 代替真 AI，测上下文组装、修改定位、重试和接口。"""

from pathlib import Path

import pytest

from app.ai import tutor
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


def edit(old, new, why="w"):
    return {"old": old, "new": new, "why": why}


def test_prompt_has_context_and_soft_rules():
    fake = FakeProvider([{"reply": "想想 pass 做了什么", "edits": []}])
    r = ask(fake, last_result={"verdict": "wrong_answer", "passed": 0, "total": 2,
                               "cases": [{"status": "wrong_answer", "input": {"args": [1, 2]}, "expected": 3, "actual": None}]})
    assert r.reply == "想想 pass 做了什么" and r.edits == [] and r.notes == []
    prompt, system = fake.calls[0]["prompt"], fake.calls[0]["system"]
    assert "  2|     pass" in prompt                    # 带行号的编辑框内容
    assert "return a + b" in prompt                     # 参考解（供 AI 判断）
    assert "wrong_answer" in prompt and "学生现在说\n我卡住了" in prompt
    assert "共用一个编辑框" in system and "不要一次把整个函数写完" in system   # 共享编辑框 + 软约束
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
    text, ok, issues = tutor.apply_edits(STARTER, r.edits)
    assert text == "def add(a: int, b: int) -> int:\n    total = a + b\n    return total\n" and issues == []


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
    assert tutor.apply_edits("", r.edits)[0] == "1 1"
    assert tutor.apply_edits("a", r.edits)[0] == "a\n1 1"


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
