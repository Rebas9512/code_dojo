"""端到端：API → 题库 → 本地或 Docker 判题 → 存储。"""

from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures" / "problems"


def solution(rel: str) -> str:
    return (FIXTURES / rel / "solution.py").read_text(encoding="utf-8")


def test_health_and_listing(client, judging):
    assert client.get("/api/health").json() == {"ok": True}
    status = client.get("/api/status").json()
    assert status["judge_mode"] == judging.backends["python"]
    assert status["judge_backends"] == judging.backends
    assert status["load_errors"] == []
    assert status["problems"] == 15
    ids = [p["id"] for p in client.get("/api/tracks/python/problems").json()]
    # 两条线各自按阶段、题目顺序排列
    assert ids == [
        "py-0a-001-add", "py-0a-002-print-sum", "py-0a-004-fill-return", "py-0a-003-predict-loop",
    ]
    assert [p["id"] for p in client.get("/api/tracks/algo/problems").json()] == [
        "algo-1-001-reverse-list", "algo-5-001-lru-cache",
    ]


def test_detail_hides_hidden_tests_and_solution(client):
    d = client.get("/api/problems/py-0a-001-add").json()
    assert d["starter"].startswith("def add(a: int, b: int) -> int:")
    assert len(d["examples"]) == 2
    assert "hidden" not in d and "solution" not in d
    assert d["next"]["id"] == "py-0a-002-print-sum" and d["prev"] is None and d["has_lesson"] is True
    assert {c["id"] for c in d["skill_cards"]} == {"py.var-arith", "py.function-return"}


def test_function_accept_and_wrong(client):
    ok = client.post("/api/problems/py-0a-001-add/submit", json={"code": solution("python/0A/py-0a-001-add")}).json()
    assert ok["verdict"] == "accepted" and ok["passed"] == ok["total"] == 5
    bad = client.post("/api/problems/py-0a-001-add/submit", json={"code": "def add(a, b):\n    return a - b\n"}).json()
    assert bad["verdict"] == "wrong_answer"
    assert any(c["hidden"] for c in bad["cases"])
    # 提交记录和状态
    subs = client.get("/api/problems/py-0a-001-add/submissions").json()
    assert [s["verdict"] for s in subs][:2] == ["wrong_answer", "accepted"]
    status = {p["id"]: p["status"] for p in client.get("/api/tracks/python/problems").json()}
    assert status["py-0a-001-add"] == "solved"


def test_run_only_uses_examples(client):
    r = client.post("/api/problems/py-0a-001-add/run", json={"code": solution("python/0A/py-0a-001-add")}).json()
    assert r["total"] == 2


def test_stdio(client):
    r = client.post("/api/problems/py-0a-002-print-sum/submit",
                    json={"code": solution("python/0A/py-0a-002-print-sum")}).json()
    assert r["verdict"] == "accepted"


def test_predict(client):
    d = client.get("/api/problems/py-0a-003-predict-loop").json()
    assert "print(i, total)" in d["program"]
    right = client.post("/api/problems/py-0a-003-predict-loop/submit", json={"answer": "1 1\n2 3\n3 6\n"}).json()
    assert right["verdict"] == "accepted"
    wrong = client.post("/api/problems/py-0a-003-predict-loop/submit", json={"answer": "1 1\n2 3\n3 5"}).json()
    assert wrong["verdict"] == "wrong_answer"
    assert wrong["cases"][0]["expected"].strip().endswith("3 6")


def test_linked_list_convert(client):
    r = client.post("/api/problems/algo-1-001-reverse-list/submit",
                    json={"code": solution("algo/1/algo-1-001-reverse-list")}).json()
    assert r["verdict"] == "accepted", r


def test_class_mode(client):
    r = client.post("/api/problems/algo-5-001-lru-cache/submit",
                    json={"code": solution("algo/5/algo-5-001-lru-cache")}).json()
    assert r["verdict"] == "accepted", r
    starter = client.get("/api/problems/algo-5-001-lru-cache").json()["starter"]
    r2 = client.post("/api/problems/algo-5-001-lru-cache/submit", json={"code": starter}).json()
    assert r2["verdict"] == "wrong_answer"


def test_errors_are_readable(client):
    syntax = client.post("/api/problems/py-0a-001-add/run", json={"code": "def add(a, b)\n    return 1\n"}).json()
    assert syntax["verdict"] == "compile_error" and "第 1 行" in syntax["error"]
    crash = client.post("/api/problems/py-0a-001-add/run", json={"code": "def add(a, b):\n    return [][0]\n"}).json()
    assert crash["verdict"] == "runtime_error" and "第 2 行" in crash["cases"][0]["error"]
    tle = client.post("/api/problems/py-0a-001-add/run",
                      json={"code": "def add(a, b):\n    while True:\n        pass\n"}).json()
    assert tle["verdict"] == "timeout"
    assert [c["status"] for c in tle["cases"]] == ["timeout", "skipped"]


def test_unknown_problem(client):
    assert client.get("/api/problems/nope").status_code == 404
