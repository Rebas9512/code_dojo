"""每道题的"课"（problem-format v1.2）：按技能拼课、加载检查、示例代码运行、助教上下文。"""

from pathlib import Path

import yaml

from app.ai.provider import FakeProvider
from app.problems import ProblemBank


def test_problem_lesson_new_skill_first(client):
    secs = client.get("/api/problems/py-0a-001-add/lesson").json()["sections"]
    assert [(s["skill"], s["new"]) for s in secs] == [("py.function-return", True), ("py.var-arith", False)]
    new = secs[0]
    assert [st["type"] for st in new["steps"]] == ["read", "example", "quiz"]
    assert new["name"] == "函数与返回值" and new["lesson"] == "变量、算术和函数"
    assert [st["type"] for st in secs[1]["steps"]] == ["read"]


def test_problem_without_new_skill_shows_used_skills(client):
    secs = client.get("/api/problems/py-0a-002-print-sum/lesson").json()["sections"]
    assert [(s["skill"], s["new"]) for s in secs] == [("py.var-arith", False)]


def test_playground_run(client):
    ok = client.post("/api/playground/run", json={"code": "print(6 * 7)"}).json()
    assert ok["status"] == "ok" and ok["stdout"].strip() == "42"
    with_input = client.post("/api/playground/run", json={"code": "print(input() * 2)", "stdin": "ab\n"}).json()
    assert with_input["stdout"].strip() == "abab"
    err = client.post("/api/playground/run", json={"code": "print(1)\nprint(1/0)"}).json()
    assert err["status"] == "runtime_error" and "ZeroDivisionError" in err["error"]
    syntax = client.post("/api/playground/run", json={"code": "print(("}).json()
    assert syntax["status"] == "compile_error"


def test_tutor_sees_the_lesson(client, fake_agents):
    fake = FakeProvider([{"reply": "看课里 double 那个例子", "edits": []}])
    fake_agents(claude=fake)
    client.delete("/api/problems/py-0a-001-add/chat")
    client.post("/api/problems/py-0a-001-add/chat", json={"message": "return 是什么", "code": ""})
    prompt, system = fake.calls[0]["prompt"], fake.calls[0]["system"]
    assert "新知识：函数与返回值" in prompt and "return x * 2" in prompt and "正确答案：把结果交给调用者" in prompt
    assert "用到的已学知识" in prompt and "\"课\"标签" in system
    client.delete("/api/problems/py-0a-001-add/chat")


def write_lesson(root: Path, lid: str, data: dict) -> None:
    d = root / "python" / "lessons" / lid
    d.mkdir(parents=True, exist_ok=True)
    (d / "lesson.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def test_bad_lessons_reported(tmp_path):
    root = tmp_path / "problems"
    (root / "python").mkdir(parents=True)
    config = Path(__file__).parent / "fixtures/problems/python/track.yaml"
    (root / "python/track.yaml").write_bytes(config.read_bytes())
    base = {"title": "课", "track": "python"}
    # 步骤的技能不在 skills 里
    write_lesson(root, "py-0a-l01-a", base | {"id": "py-0a-l01-a", "skills": ["py.a"],
                                              "steps": [{"type": "read", "skill": "py.b", "md": "x"}]})
    # quiz 答案越界
    write_lesson(root, "py-0a-l02-b", base | {"id": "py-0a-l02-b", "skills": ["py.c"],
                                              "steps": [{"type": "quiz", "skill": "py.c", "q": "?", "options": ["a"], "answer": 3}]})
    # 同一个技能在两个文件里讲
    write_lesson(root, "py-0a-l03-c", base | {"id": "py-0a-l03-c", "skills": ["py.d"],
                                              "steps": [{"type": "read", "skill": "py.d", "md": "x"}]})
    write_lesson(root, "py-0a-l04-d", base | {"id": "py-0a-l04-d", "skills": ["py.d"],
                                              "steps": [{"type": "read", "skill": "py.d", "md": "y"}]})
    bank = ProblemBank(root)
    bank.refresh(force=True)
    messages = " | ".join(e.message for e in bank.errors)
    assert "不在本文件的 skills 里" in messages
    assert "answer 超出选项范围" in messages
    assert "已经在别的 lesson 文件里讲过" in messages
    assert set(bank.lessons) == {"py-0a-l03-c"}
