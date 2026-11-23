"""学习线配置、跨线技能以及地图与题目列表的一致性。"""

import shutil
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.db import Store
from app.problems import ProblemBank

FIXTURES = Path(__file__).parent / "fixtures/problems"
REVERSE = "algo-1-001-reverse-list"


@pytest.fixture
def tracks_api(tmp_path, monkeypatch):
    import app.main as main

    store = Store(tmp_path / "tracks.sqlite")
    monkeypatch.setattr(main, "store", store)
    monkeypatch.setattr(main, "bank", ProblemBank(FIXTURES))
    return TestClient(main.app), store


def test_load_tracks_and_refresh_stages(tmp_path):
    root = tmp_path / "problems"
    shutil.copytree(FIXTURES, root)
    bank = ProblemBank(root)
    bank.refresh()
    assert not bank.errors and list(bank.tracks) == ["data", "python", "algo", "sql", "dsfix", "math"]
    assert bank.skills["math"] == {} and bank.skill_index["py.function-return"].track == "python"
    config = root / "algo/track.yaml"
    raw = yaml.safe_load(config.read_text(encoding="utf-8"))
    raw["stages"].insert(0, {"id": 7, "name": "新阶段"})
    config.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    bank.refresh()
    assert next(iter(bank.tracks["algo"].stages.items())) == ("7", "新阶段")


@pytest.mark.parametrize(("field", "value"), [("track", "missing"), ("stage", "unknown")])
def test_invalid_problem_isolated(tmp_path, field, value):
    root = tmp_path / "problems"
    shutil.copytree(FIXTURES, root)
    path = root / "algo" / "1" / REVERSE / "problem.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw[field] = value
    path.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    bank = ProblemBank(root)
    bank.refresh()
    assert len(bank.problems) == 14 and REVERSE not in bank.problems
    assert len(bank.errors) == 1 and value in bank.errors[0].message and REVERSE in bank.errors[0].path


def test_bad_planned_config_isolated(tmp_path):
    root = tmp_path / "problems"
    shutil.copytree(FIXTURES, root)
    path = root / "math/track.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("status: planned", "status: unknown"), encoding="utf-8")
    bank = ProblemBank(root)
    bank.refresh()
    assert list(bank.tracks) == ["data", "python", "algo", "sql", "dsfix"] and len(bank.problems) == 15
    assert len(bank.errors) == 1 and bank.errors[0].path == str(path)


def test_track_map_progress(tracks_api):
    client, store = tracks_api
    rows = client.get("/api/tracks").json()
    assert [r["id"] for r in rows] == ["data", "python", "algo", "sql", "dsfix", "math"]
    root, first, algo, sql, ds, planned = rows
    assert ds["runtime"] == "ds" and ds["total"] == 7
    assert (root["name"], root["total"], root["language"]) == ("认识数据", 2, "none")
    assert first.keys() == {
        "id", "name", "summary", "order", "language", "runtime", "status", "requires", "stages", "total",
        "solved", "assisted", "attempted", "skills", "next", "requires_done", "mastered",
    }
    assert [first["name"], first["language"], first["order"], first["skills"]] == ["Python 基础", "python", 1, 2]
    problems = client.get("/api/tracks/python/problems").json()
    def unstarted(uid, name, total=0, skill=None):
        return {"id": uid, "name": name, "total": total, "solved": 0, "assisted": 0, "attempted": 0, "mastered": 0,
                "skills": [{"id": skill[0], "name": skill[1], "status": None}] if skill else [],
                "next": None}

    assert first["stages"] == [
        {"id": "0A", "name": "语法基础", "total": 4, "solved": 0, "units": [
            unstarted("1", "第 1 组", 2, ("py.var-arith", "变量与算术")),
            unstarted("6", "第 6 组", 2, ("py.function-return", "函数与返回值")),
        ]},
        {"id": "0B", "name": "算法入门", "total": 0, "solved": 0, "units": [unstarted("0B", "算法入门")]},
    ]
    assert [p["unit"] for p in problems] == ["6", "1", "6", "1"]
    assert not algo["requires_done"] and algo["requires"] == ["python"]
    assert sql["requires"] == ["data"] and sql["runtime"] == "pglite" and not sql["requires_done"]
    assert planned["status"] == "planned" and planned["total"] == planned["skills"] == 0 and planned["next"] is None

    assert all(s["units"] == [] and s["total"] == s["solved"] == 0 for s in planned["stages"])

    def submit(i, verdict, ai_lines=0):
        store.add_submission(problem_id=problems[i]["id"], track="python", kind="submit", code="",
                             result={"verdict": verdict}, elapsed_ms=None, hints_used=0, ai_lines=ai_lines)

    submit(0, "accepted", 1)
    submit(1, "accepted")
    submit(2, "wrong_answer")
    first = client.get("/api/tracks").json()[1]
    assert (first["solved"], first["assisted"], first["attempted"], first["total"]) == (2, 1, 1, 4)
    assert first["stages"][0]["solved"] == 2
    unit = first["stages"][0]["units"][1]
    assert (unit["solved"], unit["assisted"], unit["attempted"], unit["total"]) == (1, 1, 1, 2)
    assert unit["skills"][0]["status"] == "assisted" and unit["next"]["id"] == problems[2]["id"]
    assert first["next"] == {"id": problems[2]["id"], "title": problems[2]["title"]}
    submit(2, "accepted")
    submit(3, "accepted")
    _, first, algo, *_ = client.get("/api/tracks").json()
    assert first["next"] is None and algo["requires_done"]


def test_requires_empty_track_is_unfinished(tracks_api, monkeypatch):
    import app.main as main

    client, _ = tracks_api
    main.bank.refresh()
    monkeypatch.setattr(main.bank.tracks["math"], "requires", ["sql"])
    assert client.get("/api/tracks").json()[-1]["requires_done"] is False


def test_cross_track_skill_links(tracks_api):
    client, store = tracks_api
    store.add_submission(problem_id=REVERSE, track="algo", kind="submit", code="", result={"verdict": "accepted"},
                         elapsed_ms=None, hints_used=0)
    reverse, = client.get("/api/tracks/algo/skills").json()
    assert reverse == {
        "id": "algo.reverse-list", "name": "反转链表", "stage": "1", "group": None,
        "card": "逐个反转节点的连接方向。", "prereqs": [{"id": "py.function-return", "name": "函数与返回值", "track": "python"}],
        "lesson": None, "problems": [{"id": REVERSE, "title": "反转链表", "format": "write", "status": "solved"}],
        "used_by": 0, "state": "learning", "counted_solves": 1,
        "last_used": store.submissions(REVERSE)[0]["created_at"],
    }
    arithmetic, function = client.get("/api/tracks/python/skills").json()
    assert arithmetic["group"] < function["group"]
    assert function["used_by"] == 3
    assert function["lesson"] == {"id": "py-0a-l01-basics", "title": "变量、算术和函数"}
    detail = client.get(f"/api/problems/{REVERSE}").json()
    assert detail["language"] == "python" and detail["track"] == "algo"
    card, = [c for c in detail["skill_cards"] if c["id"] == function["id"]]
    assert card["name"] == function["name"] and card["card"] == function["card"]
    section, = [s for s in client.get(f"/api/problems/{REVERSE}/lesson").json()["sections"] if not s["new"]]
    assert section["name"] == function["name"] and section["steps"]


@pytest.mark.parametrize("view", ["skills", "problems"])
def test_planned_and_unknown_track(tracks_api, view):
    client, _ = tracks_api
    assert client.get(f"/api/tracks/math/{view}").json() == []
    missing = client.get(f"/api/tracks/nope/{view}")
    assert missing.status_code == 404 and "没有这条学习线" in missing.json()["detail"]


def test_skill_taught_in_two_tracks_is_reported(tmp_path):
    root = tmp_path / "problems"
    shutil.copytree(FIXTURES, root)
    meta = {"id": "algo-1-l01-return", "title": "返回值", "track": "algo", "skills": ["py.function-return"],
            "steps": [{"type": "read", "skill": "py.function-return", "md": "返回值"}]}
    lesson = root / "algo/lessons" / meta["id"]
    lesson.mkdir(parents=True)
    (lesson / "lesson.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")
    bank = ProblemBank(root)
    bank.refresh()
    assert len(bank.errors) == 1 and "py.function-return" in bank.errors[0].message
    assert bank.skill_lesson["py.function-return"].id == "py-0a-l01-basics"
