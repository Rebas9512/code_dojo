"""附加题：出题 + 沙箱验证、后台任务、接口、助教的增删动作。用 FakeProvider 代替真 AI，判题用真的 Docker 沙箱。"""

import json
import time

import pytest

from app.ai import extra as extra_gen
from app.ai.provider import AIError, FakeProvider

TESTS = {"examples": [{"args": [2, 3], "expected": 6}, {"args": [0, 5], "expected": 0}],
         "hidden": [{"args": [-2, 3], "expected": -6}, {"args": [1, 1], "expected": 1}, {"args": [7, 8], "expected": 56}]}


def spec(**over):
    base = {
        "title": "两数相乘",
        "statement": "## 题目\n返回 a 与 b 的乘积。\n\n## 示例\n`multiply(2, 3)` → `6`\n\n## 约束\n- 整数",
        "mode": "function", "entry": "multiply", "signature": "def multiply(a: int, b: int) -> int:",
        "compare": "exact", "starter": "def multiply(a: int, b: int) -> int:\n    pass\n",
        "solution": "def multiply(a, b):\n    return a * b\n",
        "tests_json": json.dumps(TESTS),
        "wrong_solutions": ["def multiply(a, b):\n    return a + b\n"],
    }
    return base | over


def parent():
    import app.main as main
    return main.bank.get("py-0a-001-add")


def test_generate_valid_first_try(client):
    import app.main as main
    fake = FakeProvider([spec()])
    s, notes = extra_gen.generate(fake, main.judge, parent(), request="", skill_names={}, existing=[])
    assert s["title"] == "两数相乘" and notes == [] and len(fake.calls) == 1
    assert "原题参考解" in fake.calls[0]["prompt"] and "return a + b" in fake.calls[0]["prompt"]


def test_generate_retries_when_tests_miss_a_wrong_solution(client):
    import app.main as main
    weak = spec(wrong_solutions=["def multiply(a, b):\n    return a * b if a else 0\n"])  # 测试抓不住这个错误写法
    fake = FakeProvider([weak, spec()])
    s, notes = extra_gen.generate(fake, main.judge, parent(), request="", skill_names={}, existing=[])
    assert len(fake.calls) == 2 and "错误写法居然全部通过" in notes[0]
    assert "没通过验证" in fake.calls[1]["prompt"]


def test_generate_gives_up_after_three_failures(client):
    import app.main as main
    broken = spec(solution="def multiply(a, b):\n    return a - b\n")
    fake = FakeProvider([dict(broken), dict(broken), dict(broken)])
    with pytest.raises(AIError, match="3 次都没通过验证"):
        extra_gen.generate(fake, main.judge, parent(), request="", skill_names={}, existing=[])


def wait_ready(client, pid, seq, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        rows = {e["seq"]: e for e in client.get(f"/api/problems/{pid}/extras").json()}
        if rows.get(seq, {}).get("status") != "generating":
            return rows.get(seq)
        time.sleep(0.3)
    raise AssertionError("附加题一直没出好")


@pytest.fixture
def fresh(client, monkeypatch, tmp_path):
    import app.main as main
    from app.db import Store
    monkeypatch.setattr(main, "store", Store(tmp_path / "db.sqlite"))
    return client


def test_extra_api_flow(fresh, monkeypatch):
    import app.main as main
    monkeypatch.setattr(main, "ai", FakeProvider([spec()]))
    created = fresh.post("/api/problems/py-0a-001-add/extras", json={"request": "换成乘法"}).json()
    assert created["seq"] == 1 and created["status"] == "generating"
    ready = wait_ready(fresh, "py-0a-001-add", 1)
    assert ready["status"] == "ready" and ready["title"] == "两数相乘"
    xid = ready["id"]
    d = fresh.get(f"/api/problems/{xid}").json()
    assert d["parent"] == "py-0a-001-add" and d["extra_seq"] == 1 and d["starter"].startswith("def multiply")
    assert d["prev"] is None and d["next"] is None and "hidden" not in d
    assert fresh.get(f"/api/problems/{xid}/lesson").json()["sections"][0]["skill"] == "py.function-return"
    ok = fresh.post(f"/api/problems/{xid}/submit", json={"code": "def multiply(a, b):\n    return a * b\n"}).json()
    assert ok["verdict"] == "accepted" and ok["total"] == 5
    assert fresh.delete("/api/problems/py-0a-001-add/extras/1").json() == {"ok": True}
    assert fresh.get("/api/problems/py-0a-001-add/extras").json() == []
    assert fresh.get(f"/api/problems/{xid}").status_code == 404
    # 编号不复用
    monkeypatch.setattr(main, "ai", FakeProvider([spec()]))
    assert fresh.post("/api/problems/py-0a-001-add/extras", json={}).json()["seq"] == 2
    wait_ready(fresh, "py-0a-001-add", 2)


def test_failed_extra_is_reported(fresh, monkeypatch):
    import app.main as main
    broken = spec(solution="def multiply(a, b):\n    return a - b\n")
    monkeypatch.setattr(main, "ai", FakeProvider([dict(broken), dict(broken), dict(broken)]))
    fresh.post("/api/problems/py-0a-001-add/extras", json={})
    row = wait_ready(fresh, "py-0a-001-add", 1)
    assert row["status"] == "failed" and "没通过验证" in row["error"]
    assert fresh.get(f"/api/problems/{row['id']}").status_code == 409


def test_tutor_can_make_and_delete_extras(fresh, monkeypatch):
    import app.main as main

    def respond(system, prompt):
        if "出题助手" in system:
            return spec()
        said = prompt.split("学生现在说")[-1]
        if "删" in said:
            return {"reply": "删掉了附加题 1", "edits": [], "make_extra": "", "delete_extras": [1]}
        if "再来" in said:
            return {"reply": "正在出一道附加题，好了会出现在左边", "edits": [], "make_extra": "同样的套路换成乘法",
                    "delete_extras": []}
        return {"reply": "先想想乘法怎么写", "edits": [], "make_extra": "", "delete_extras": []}

    fake = FakeProvider(respond)
    monkeypatch.setattr(main, "ai", fake)
    r = fresh.post("/api/problems/py-0a-001-add/chat", json={"message": "再来一道类似的", "code": ""}).json()
    assert r["new_extra"]["seq"] == 1 and r["deleted_extras"] == []
    ready = wait_ready(fresh, "py-0a-001-add", 1)
    # 在附加题上和助教聊：助教知道学生在看哪一道
    fresh.post("/api/problems/py-0a-001-add/chat", json={"message": "这题怎么想", "code": "", "current": ready["id"]})
    tutor_prompts = [c["prompt"] for c in fake.calls if "教学助手" in c["system"]]
    assert "学生现在在看：附加题 1：两数相乘" in tutor_prompts[-1]
    assert "已有的附加题：附加题 1：两数相乘" in tutor_prompts[-1]
    assert "def multiply" in tutor_prompts[-1]                       # 上下文换成了附加题本身
    r2 = fresh.post("/api/problems/py-0a-001-add/chat", json={"message": "把附加题1删了", "code": ""}).json()
    assert r2["deleted_extras"] == [1] and fresh.get("/api/problems/py-0a-001-add/extras").json() == []
    # 原题和附加题共用一段对话
    assert len(fresh.get("/api/problems/py-0a-001-add/chat").json()) == 6


def test_current_must_belong_to_parent(fresh, monkeypatch):
    import app.main as main
    monkeypatch.setattr(main, "ai", FakeProvider([spec()]))
    fresh.post("/api/problems/py-0a-001-add/extras", json={})
    xid = wait_ready(fresh, "py-0a-001-add", 1)["id"]
    monkeypatch.setattr(main, "ai", FakeProvider([]))
    bad = fresh.post("/api/problems/py-0a-002-print-sum/chat", json={"message": "hi", "current": xid})
    assert bad.status_code == 400
    assert fresh.post(f"/api/problems/{xid}/extras", json={}).status_code == 400   # 附加题不能再出附加题


def test_algo_extra_uses_python_and_cross_track_skills(fresh, monkeypatch):
    import app.main as main

    fake = FakeProvider([spec()])
    monkeypatch.setattr(main, "ai", fake)
    pid = "algo-1-001-reverse-list"
    assert fresh.post(f"/api/problems/{pid}/extras", json={}).status_code == 200
    ready = wait_ready(fresh, pid, 1)
    assert ready["status"] == "ready"
    detail = fresh.get(f"/api/problems/{ready['id']}").json()
    assert detail["track"] == "algo" and detail["language"] == "python"
    assert "函数与返回值" in fake.calls[0]["prompt"]
