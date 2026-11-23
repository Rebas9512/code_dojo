"""分组、跨阶段引用、练习题跟随和没有题目的单元。"""

from pathlib import Path

import pytest

from app.problems import Problem, ProblemMeta, Skill, SkillRef
from app.tracks import load_track
from app.units import Unit, group_units, progress_frontier


def test_group_assignment(tmp_path: Path):
    path = tmp_path / "python" / "track.yaml"
    path.parent.mkdir()
    path.write_text("""
id: python
name: 基础
summary: 测试
order: 1
language: python
runtime: python
status: active
requires: []
skill_prefix: py
stages:
  - {id: A, name: 入门, units: {0: 起步, 2: 组合, 3: 后续}}
  - {id: B, name: 练习}
""", encoding="utf-8")
    track = load_track(path)
    def skill(sid, stage, group=None):
        return Skill("python", sid, sid, stage, [], "", group)

    skills = [skill("py.one", "A", 1), skill("py.two", "A", 2), skill("py.free", "A"), skill("py.practice", "B"),
              Skill("foreign", "foreign.high", "跨线技能", "A", [], "", 9)]

    def problem(pid, order, requires=(), introduces=None, stage="A"):
        meta = ProblemMeta(id=pid, title=pid, track="python", stage=stage, order=order, format="write",
                           difficulty=1, skills=SkillRef(requires=list(requires), introduces=introduces))
        return Problem(meta, track, path.parent, "", "")

    ordered = [
        problem("first", 1), problem("max", 2, ["py.two"], "py.one"),
        problem("follow", 3, ["foreign.high", "py.practice"]),
        problem("lower", 4, ["py.one"]), problem("free", 5, ["py.free"]),
        problem("new-stage", 1, ["py.two"], stage="B"),
    ]
    stages = group_units(track, {s.id: s for s in skills}, ordered)
    assert [(u.id, u.name, [p.id for p in u.problems]) for u in stages["A"]] == [
        ("0", "起步", ["first"]), ("1", "第 1 组", ["lower", "free"]),
        ("2", "组合", ["max", "follow"]), ("3", "后续", []),
    ]
    assert [s.id for s in stages["A"][0].skills] == ["py.free"]
    whole, = stages["B"]
    assert (whole.id, whole.name, [p.id for p in whole.problems]) == ("B", "练习", ["new-stage"])


def test_pinned_unit(tmp_path: Path):
    """problem.yaml 里写 unit: N 覆盖推算；后面没有本阶段技能的练习题跟着它走。"""
    path = tmp_path / "algo" / "track.yaml"
    path.parent.mkdir()
    path.write_text("""
id: algo
name: 算法
summary: 测试
order: 2
language: python
runtime: python
status: active
requires: []
skill_prefix: algo
stages:
  - {id: "1", name: 基础, units: {1: 数组, 2: 栈}}
""", encoding="utf-8")
    track = load_track(path)
    skills = [Skill("algo", "algo.hash", "哈希", "1", [], "", 1), Skill("algo", "algo.stack", "栈", "1", [], "", 2)]

    def problem(pid, order, requires=(), introduces=None, unit=None):
        extra = {"unit": unit} if unit is not None else {}
        meta = ProblemMeta(id=pid, title=pid, track="algo", stage="1", order=order, format="write",
                           difficulty=1, skills=SkillRef(requires=list(requires), introduces=introduces), **extra)
        return Problem(meta, track, path.parent, "", "")

    ordered = [problem("hash", 1, introduces="algo.hash"), problem("pinned", 2, ["py.list"], unit=2),
               problem("follow", 3, ["py.list"]), problem("stack", 4, introduces="algo.stack")]
    stages = group_units(track, {s.id: s for s in skills}, ordered)
    assert [[p.id for p in u.problems] for u in stages["1"]] == [["hash"], ["pinned", "follow", "stack"]]


@pytest.mark.parametrize(("status", "expected"), [
    ({}, "a"),
    ({"b": "attempted"}, "c"),
    ({"c": "assisted"}, "a"),
    ({"a": "solved", "b": "assisted", "c": "attempted"}, "d"),
    ({"d": "solved"}, "e"),
    ({"a": "solved", "b": "solved", "c": "solved", "d": "solved", "e": "solved"}, None),
    ({"选修二": "attempted"}, "d"),
    ({"e": "attempted"}, None),
])
def test_progress_frontier(status, expected):
    path = Path(__file__).parent / "fixtures/problems/python/track.yaml"
    track = load_track(path)

    def unit(stage, uid, ids):
        problems = []
        for order, pid in enumerate(ids):
            meta = ProblemMeta(id=pid, title=f"题 {pid}", track="python", stage=stage, order=order,
                               format="write", difficulty=1, skills=SkillRef(), optional=pid.startswith("选修"))
            problems.append(Problem(meta, track, path.parent, "", ""))
        return Unit(uid, uid, problems=problems)

    stages = {"0A": [unit("0A", "1", ["选修一", "a", "b", "c"]), unit("0A", "2", ["选修二", "d"])],
              "0B": [unit("0B", "1", ["e", "选修三"])]}
    assert progress_frontier(stages, status) == ({"id": expected, "title": f"题 {expected}"} if expected else None)
