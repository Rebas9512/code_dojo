"""只检查一条线时，也要读取传递前置线的技能。"""

from pathlib import Path
import sys

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/curriculum"))
import check_curve


@pytest.fixture
def curriculum(tmp_path, monkeypatch):
    monkeypatch.setattr(check_curve, "PROBLEMS", tmp_path)
    for tid, prefix, deps, stage in [("leaf", "leaf", ["middle"], 3), ("middle", "mid", ["base"], 2),
                                      ("base", "py", [], "0a")]:
        path = tmp_path / tid
        path.mkdir()
        track = {"id": tid, "name": tid, "summary": "测试", "order": 1, "language": "python", "runtime": "python",
                 "status": "active", "requires": deps, "skill_prefix": prefix, "stages": [{"id": stage, "name": "阶段"}]}
        (path / "track.yaml").write_text(yaml.safe_dump(track), encoding="utf-8")
        skills = [] if tid == "middle" else [
            {"id": "py.print" if tid == "base" else "leaf.output", "name": "输出", "stage": stage,
             "prereqs": [] if tid == "base" else ["py.print"], "card": "用 print 输出。"},
        ]
        (path / "skills.yaml").write_text(yaml.safe_dump({"track": tid, "skills": skills}), encoding="utf-8")
    problem = tmp_path / "leaf/3/leaf-3-001-print"
    problem.mkdir(parents=True)
    meta = {"id": problem.name, "track": "leaf", "stage": 3, "order": 1, "format": "predict", "mode": "predict",
            "difficulty": 1, "skills": {"requires": ["py.print"], "introduces": None}}
    (problem / "problem.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")
    (problem / "statement.md").write_text("输出是什么？", encoding="utf-8")
    (problem / "solution.py").write_text("print(1)", encoding="utf-8")
    return tmp_path


def errors():
    return [e for _, report in check_curve.check_curriculum("leaf", False, False) for e in report.errors]


def test_transitive_track_skills_are_learned(curriculum):
    assert errors() == []
    path = curriculum / "middle/track.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw["requires"] = []
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    assert any("py.print" in e for e in errors())


@pytest.mark.parametrize(("requires", "message"), [(["unknown"], "不存在"), (["leaf"], "有环")])
def test_invalid_track_graph(curriculum, requires, message):
    path = curriculum / "base/track.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw["requires"] = requires
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    assert any(message in e for e in errors())



@pytest.mark.parametrize("language", ["python", "sql", "none"])
def test_inspect_needs_data_instead_of_solution(curriculum, language):
    track_file = curriculum / "leaf/track.yaml"
    config = yaml.safe_load(track_file.read_text(encoding="utf-8"))
    config["language"] = language
    config["runtime"] = {"python": "python", "sql": "pglite", "none": "none"}[language]
    track_file.write_text(yaml.safe_dump(config), encoding="utf-8")
    directory = curriculum / "leaf/3/leaf-3-001-print"
    meta_path = directory / "problem.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) | {
        "format": "inspect", "mode": "inspect", "data": [{"kind": "csv", "file": "books.csv"}],
        "answer": {"type": "short", "accept": ["1"]}, "explain": "有一本书。",
    }
    meta_path.write_text(yaml.safe_dump(meta), encoding="utf-8")
    (directory / "solution.py").unlink()
    assert any("books.csv" in e for e in errors())
    (directory / "books.csv").write_text("id\n1", encoding="utf-8")
    assert errors() == []
    (directory / "solution.py").write_text("不是一段合法的 Python 代码。", encoding="utf-8")
    assert errors() == []

@pytest.mark.parametrize(("week", "valid"), [(1, True), (10, True), (0, False), (-1, False),
                                              (True, False), (2.5, False), ("1", False), (None, False)])
def test_week_is_positive_integer(curriculum, week, valid):
    from app.problems import ProblemMeta
    path = curriculum / "leaf/3/leaf-3-001-print/problem.yaml"
    meta = yaml.safe_load(path.read_text(encoding="utf-8")) | {"title": "输出", "week": week}
    path.write_text(yaml.safe_dump(meta), encoding="utf-8")
    if valid:
        assert errors() == []
        assert ProblemMeta(**meta).week == week
    else:
        assert any("week 应为正整数" in e for e in errors())
        with pytest.raises(ValueError, match="week 应为正整数"):
            ProblemMeta(**meta)


def test_standard_skills_follow_solution_closure(curriculum):
    """标准写法和参考解同一规则：requires ∪ introduces 及其前置链上的技能都能用，不用为此改题目的 requires。"""
    directory = curriculum / "leaf/3/leaf-3-001-print"
    path = directory / "problem.yaml"
    skills_path = curriculum / "base/skills.yaml"
    skills = yaml.safe_load(skills_path.read_text())
    skills["skills"].append(dict(skills["skills"][0], id="py.output", prereqs=["py.print"]))
    skills_path.write_text(yaml.safe_dump(skills))
    meta = yaml.safe_load(path.read_text()) | {"format": "write", "mode": "stdio", "skills": {"requires": ["py.output"]}}
    path.write_text(yaml.safe_dump(meta))
    (directory / "tests.json").write_text("{}")
    (directory / "standard.py").write_text("print(1)")
    assert not any("标准写法" in msg for msg in errors())
    meta["skills"]["requires"] = []
    path.write_text(yaml.safe_dump(meta))
    assert any("标准写法用到 py.print" in msg for msg in errors())


def test_project_combines_only_previously_introduced_skills(curriculum):
    """项目部分不引入新技能；本线或前置线引入过的技能都可以组合（py.print 来自前置线 base）。"""
    path = curriculum / "leaf/track.yaml"
    track = yaml.safe_load(path.read_text())
    track["stages"][0].update(kind="project", units={1: "项目"})
    path.write_text(yaml.safe_dump(track))
    path = curriculum / "leaf/3/leaf-3-001-print/problem.yaml"
    problem = yaml.safe_load(path.read_text())
    problem.update(project="report", part=1, unit=1, format="combine", mode="function",
                   entry="show", signature="def show():")
    problem["skills"]["introduces"] = "leaf.output"
    path.write_text(yaml.safe_dump(problem))
    issues = errors()
    assert any("不能引入新技能" in e for e in issues)
    assert not any("py.print 尚未" in e for e in issues)
