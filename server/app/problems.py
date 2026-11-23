"""题库加载：按 docs/problem-format.md 读取 problems/ 目录。

目录有改动时自动重新加载（按文件修改时间判断），改题不用重启服务。
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .inspect_data import InspectExercise, data_block
from .tracks import LoadError, Track, load_track, load_tracks, normalize_stage, read_yaml

Format = Literal["predict", "complete", "fix", "write", "variant", "combine", "inspect"]


class SkillRef(BaseModel):
    requires: list[str] = Field(default_factory=list)
    introduces: str | None = None


class Constraints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    no_loops: bool = False
    forbid_calls: list[str] = Field(default_factory=list)
    forbid_imports: list[str] = Field(default_factory=list)


class QueryCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1)
    query: str = Field(min_length=1)
    ordered: bool = False


class ProbeCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1)
    probe: str = Field(min_length=1)
    expect: Literal["error", "ok"]


class ProblemMeta(BaseModel):
    """problem.yaml 的公共字段；未知字段保留（如 wrong_examples），方便内容侧先行试验。"""

    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    track: str
    stage: str
    order: int
    week: int | None = None
    format: Format
    difficulty: int = Field(ge=1, le=100)
    skills: SkillRef = Field(default_factory=SkillRef)
    source: str = "original"
    leetcode: str | None = None
    milestones: list[str] = Field(default_factory=list)
    hints: list[str] = Field(default_factory=list)
    optional: bool = False                # 选修
    unit: int | None = None               # 直接指定单元（见 units.group_units）
    replaces_premium: str | None = None   # 替代的 LeetCode 会员题 slug

    mode: Literal["function", "class", "stdio", "predict", "inspect", "dml", "script"] | None = None
    # Python
    entry: str | None = None
    signature: str | None = None
    compare: Literal["exact", "unordered", "float", "checker", "allclose", "frame"] = "exact"
    rtol: float = Field(default=1e-5, ge=0, allow_inf_nan=False)
    atol: float = Field(default=1e-8, ge=0, allow_inf_nan=False)
    ignore_row_order: bool = False
    ignore_index: bool = False
    check_column_names: bool = True
    constraints: Constraints | None = None
    time_limit_ms: int | None = Field(default=None, gt=0)
    convert: dict[str, Any] | None = None

    # SQL
    datasets: list[str] = Field(default_factory=list)
    ordered: bool = False
    check_query: str | None = None
    checks: list[QueryCheck | ProbeCheck] = Field(default_factory=list)

    @field_validator("week", mode="before")
    @classmethod
    def _positive_week(cls, value: Any) -> int:
        if type(value) is not int or value < 1:
            raise ValueError("week 应为正整数")
        return value

    @field_validator("stage", mode="before")
    @classmethod
    def _stage_to_str(cls, v: Any) -> str:
        return normalize_stage(v)

    def check_language(self, language: str) -> None:
        if self.mode == "script":
            if language != "sql" or not self.checks:
                raise ValueError("script 模式需要 SQL 题和非空的 checks")
        elif self.checks:
            raise ValueError("checks 只用于 script 模式")
        if self.mode == "dml":
            if language != "sql" or not (self.check_query or "").strip():
                raise ValueError("dml 模式需要 SQL 题和非空的 check_query")
        elif self.check_query is not None:
            raise ValueError("check_query 只用于 dml 模式")
        if self.format == "inspect" and self.mode == "inspect":
            return
        if language == "none" or self.format == "inspect" or self.mode == "inspect":
            raise ValueError("看数据作答题的 format 和 mode 都应为 inspect")
        if language == "python":
            if self.mode is None:
                raise ValueError("Python 题必须有 mode")
            if self.mode in ("function", "class") and not self.entry:
                raise ValueError(f"{self.mode} 模式必须有 entry")
            if self.mode == "function" and not self.signature:
                raise ValueError("function 模式必须有 signature")
        if language == "sql":
            if self.mode not in (None, "dml", "script"):
                raise ValueError("SQL 代码题省略 mode 或使用 dml、script")
            if not self.datasets:
                raise ValueError("SQL 题必须至少有一个 dataset")


@dataclass
class Problem:
    meta: ProblemMeta
    track: Track
    path: Path
    statement: str
    starter: str
    inspect: InspectExercise | None = None

    @property
    def id(self) -> str:
        return self.meta.id

    @cached_property
    def tests(self) -> dict[str, Any]:
        """tests.json 第一次用到时才读：全题库约 46 MB，启动时全解析要 0.4 秒、占两百多 MB 内存。"""
        raw = self.read("tests.json")
        return json.loads(raw) if raw else {}

    @property
    def sort_key(self) -> tuple[int, int, str]:
        stages = list(self.track.stages)
        return (stages.index(self.meta.stage), self.meta.order, self.meta.id)

    def file(self, name: str) -> Path:
        return self.path / name

    def read(self, name: str) -> str | None:
        p = self.file(name)
        return p.read_text(encoding="utf-8") if p.exists() else None

    def cases(self, which: Literal["examples", "all"]) -> list[dict[str, Any]]:
        examples = list(self.tests.get("examples", []))
        if which == "examples":
            return examples
        return examples + list(self.tests.get("hidden", []))

    def judge_options(self) -> dict[str, Any]:
        m = self.meta
        return dict(runtime=self.track.runtime, time_limit_ms=m.time_limit_ms, entry=m.entry, compare=m.compare,
                    convert=m.convert, checker=self.read("checker.py") if m.compare == "checker" else None,
                    constraints=m.constraints.model_dump() if m.constraints else None,
                    compare_options=m.model_dump(include={"rtol", "atol", "ignore_row_order", "ignore_index",
                                                          "check_column_names"}))


class LessonStep(BaseModel):
    """课的一步：read 讲解、example 示例代码或数据、quiz 单选，每一步标明讲哪个技能。"""

    model_config = ConfigDict(extra="allow")

    type: Literal["read", "example", "quiz"]
    skill: str
    md: str | None = None
    data: dict | None = None
    code: str | None = None
    stdin: str | None = None
    db: str | None = None
    patch: str | None = None
    q: str | None = None
    options: list[str] = Field(default_factory=list)
    answer: int | None = None
    explain: str | None = None

    @model_validator(mode="after")
    def _check(self) -> "LessonStep":
        if self.type == "example" and (self.code is None) == (self.data is None):
            raise ValueError("example 需要 code 或 data，二选一")
        need = {"read": ["md"], "example": [], "quiz": ["q", "answer"]}[self.type]
        missing = [k for k in need if getattr(self, k) is None]
        if missing:
            raise ValueError(f"{self.type} 步骤缺少 {', '.join(missing)}")
        if self.type == "quiz" and not (0 <= (self.answer or 0) < len(self.options)):
            raise ValueError("quiz 的 answer 超出选项范围")
        return self


class LessonMeta(BaseModel):
    """一个 lesson 文件讲一组相关技能。"""

    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    track: str
    skills: list[str]
    steps: list[LessonStep]

    @model_validator(mode="after")
    def _check_skills(self) -> "LessonMeta":
        bad = sorted({st.skill for st in self.steps} - set(self.skills))
        if bad:
            raise ValueError(f"步骤里的技能不在本文件的 skills 里：{', '.join(bad)}")
        return self


@dataclass
class Lesson:
    meta: LessonMeta
    path: Path

    @property
    def id(self) -> str:
        return self.meta.id


@dataclass
class ExtraProblem(Problem):
    """附加题：AI 照着原题出、验证过的题，存在数据库里，文件内容放内存。id 形如 x-12。"""

    files: dict[str, str] = field(default_factory=dict)
    parent_id: str = ""
    seq: int = 0

    def read(self, name: str) -> str | None:
        return self.files.get(name)


def extra_id(row_id: int) -> str:
    return f"x-{row_id}"


def build_extra(parent: Problem, row_id: int, seq: int, spec: dict[str, Any]) -> ExtraProblem:
    pm = parent.meta
    is_sql = parent.track.language == "sql" and not parent.inspect
    mode = spec.get("mode")
    sql_files = {f"datasets/{i}.sql": sql for i, sql in enumerate(spec["datasets"])} if is_sql else {}
    fmt = "predict" if mode == "predict" else ("write" if pm.format == "predict" else pm.format)
    refs = SkillRef.model_validate(spec["review_skills"]) if "review_skills" in spec else pm.skills
    if spec.get("practice_skill"):
        refs = SkillRef(requires=[spec["practice_skill"]])
    meta = ProblemMeta(
        id=extra_id(row_id), title=spec["title"], track=pm.track, stage=pm.stage, order=pm.order,
        format=spec.get("review_format", fmt), difficulty=pm.difficulty, skills=refs, source="ai",
        datasets=list(sql_files), ordered=spec.get("ordered", False), check_query=spec.get("check_query"),
        checks=spec.get("checks", []), mode=mode, entry=spec.get("entry"), signature=spec.get("signature"),
        compare=spec.get("compare") or "exact", time_limit_ms=pm.time_limit_ms,
        **{k: spec[k] for k in ("constraints", "rtol", "atol", "ignore_index", "ignore_row_order",
                                "check_column_names") if k in spec},
    )
    meta.check_language(parent.track.language)
    if parent.inspect:
        return ExtraProblem(meta=meta, track=parent.track, path=parent.path, statement=spec["statement"],
                            starter="", inspect=InspectExercise.load(spec), parent_id=parent.id, seq=seq)
    starter = spec.get("starter") or default_starter(meta, parent.track.language)
    extra = ExtraProblem(
        meta=meta, track=parent.track, path=parent.path, statement=spec.get("statement", ""), starter=starter,
        files=sql_files | {("solution.sql" if is_sql else "solution.py"): spec["solution"]}, parent_id=parent.id, seq=seq,
    )
    extra.tests = spec.get("tests", {})
    return extra


@dataclass
class Skill:
    track: str
    id: str
    name: str
    stage: str
    prereqs: list[str]
    card: str
    group: int | None = None


def default_starter(meta: ProblemMeta, language: str) -> str:
    if language == "sql":
        if meta.mode == "script":
            return "-- 在这里写 SQL 脚本\n"
        if meta.mode == "dml":
            return "-- 在这里写修改语句\n"
        return "-- 在这里写 SQL 查询\n"
    if meta.mode == "function":
        return f"{meta.signature}\n    pass\n"
    if meta.mode == "class":
        return f"class {meta.entry}:\n    def __init__(self):\n        pass\n"
    if meta.mode == "stdio":
        return "# 从标准输入读取数据，用 print 输出结果\n"
    return ""


def load_problem(problem_dir: Path, track: Track | None = None) -> Problem:
    meta = ProblemMeta.model_validate(read_yaml(problem_dir / "problem.yaml"))
    if track is None:
        track = load_track(problem_dir.parents[1] / "track.yaml")
    if meta.track != track.id:
        raise ValueError(f"题目的学习线 {meta.track} 与所在目录 {track.id} 不符")
    if meta.stage not in track.stages:
        raise ValueError(f"{track.id} 未知阶段 {meta.stage}")
    if meta.stage != normalize_stage(problem_dir.parent.name):
        raise ValueError(f"阶段 {meta.stage} 与目录 {problem_dir.parent.name} 不符")
    meta.check_language(track.language)
    if meta.compare in ("allclose", "frame") and (track.runtime != "ds" or meta.mode not in ("function", "class")):
        raise ValueError(f"{meta.compare} 需要 runtime: ds 的函数或类方法返回值")
    if meta.compare == "checker" and not (problem_dir / "checker.py").is_file():
        raise ValueError("compare: checker 需要 checker.py")
    if meta.id != problem_dir.name:
        raise ValueError(f"id {meta.id} 和文件夹名 {problem_dir.name} 不一致")
    statement_path = problem_dir / "statement.md"
    statement = statement_path.read_text(encoding="utf-8") if statement_path.exists() else ""
    if meta.format == "inspect":
        exercise = InspectExercise.load(meta.model_dump(), problem_dir)
        return Problem(meta=meta, track=track, path=problem_dir, statement=statement, starter="", inspect=exercise)
    starter_name = "starter.sql" if track.language == "sql" else "starter.py"
    starter_path = problem_dir / starter_name
    starter = starter_path.read_text(encoding="utf-8") if starter_path.exists() else default_starter(meta, track.language)
    if track.language == "python" and meta.mode != "predict" and not (problem_dir / "tests.json").exists():
        raise ValueError("缺少 tests.json")
    return Problem(meta=meta, track=track, path=problem_dir, statement=statement, starter=starter)


def load_skills(path: Path, track: Track) -> dict[str, Skill]:
    if not path.exists():
        return {}
    data = read_yaml(path) or {}
    if data.get("track") != track.id:
        raise ValueError(f"技能文件的学习线应为 {track.id}")
    skills = {}
    for raw in data.get("skills", []):
        skill = Skill(
            track=track.id,
            id=raw["id"],
            name=raw.get("name", raw["id"]),
            stage=normalize_stage(raw.get("stage")),
            prereqs=list(raw.get("prereqs", []) or []),
            card=raw.get("card", "") or "",
            group=raw.get("group"),
        )
        if skill.id in skills or not skill.id.startswith(track.skill_prefix + "."):
            raise ValueError(f"技能 id 重复或前缀不符：{skill.id}")
        if skill.group is not None and type(skill.group) is not int:
            raise ValueError(f"技能 {skill.id} 的 group 必须是整数")
        if skill.stage not in track.stages:
            raise ValueError(f"技能 {skill.id} 的阶段 {skill.stage} 不在线内")
        skills[skill.id] = skill
    return skills


def shared_db(track_dir: Path, name: str) -> list[str]:
    directory = track_dir / "_db" / name
    return [(directory / file).read_text(encoding="utf-8") for file in ("schema.sql", "seed.sql")]


class ProblemBank:
    """线程安全、按修改时间自动重载的题库。

    查"题库有没有改"要 stat 上万个文件（NTFS / fuseblk 盘上约 0.8 秒），不能放在每个请求里。
    请求路径只调 ensure_fresh()：已加载就直接返回；改动由后台线程按间隔发现并重载。
    CODE_DOJO_BANK_WATCH：秒数（默认 3）= 后台检查间隔；off = 只加载一次，连修改时间也不查（桌面应用，题库随更新包整体替换）；
    sync = 每次请求都检查（旧行为，测试用）。显式调用 refresh() 永远会检查。
    """

    def __init__(self, root: Path):
        self.root = root
        self._lock = threading.Lock()
        self._watching = False
        self._stamp: float | None = None
        self.tracks: dict[str, Track] = {}
        self.skill_index: dict[str, Skill] = {}
        self.problems: dict[str, Problem] = {}
        self.lessons: dict[str, Lesson] = {}
        self.skill_lesson: dict[str, Lesson] = {}   # 技能 id → 讲它的 lesson 文件
        self.skills: dict[str, dict[str, Skill]] = {}
        self.errors: list[LoadError] = []
        self._ordered: list[Problem] = []                  # 学习顺序，加载时排好
        self._by_track: dict[str, list[Problem]] = {}

    def _current_stamp(self) -> float:
        newest = self.root.stat().st_mtime
        for p in self.root.rglob("*"):
            if "node_modules" in p.parts:
                continue
            try:
                newest = max(newest, p.stat().st_mtime)
            except FileNotFoundError:
                continue
        return newest

    def refresh(self, force: bool = False, stamp: float | None = None) -> None:
        stamp = self._current_stamp() if stamp is None else stamp
        with self._lock:
            if not force and stamp == self._stamp:
                return
            problems: dict[str, Problem] = {}
            lessons: dict[str, Lesson] = {}
            skill_lesson: dict[str, Lesson] = {}
            skills: dict[str, dict[str, Skill]] = {}
            tracks, errors = load_tracks(self.root)
            skill_index: dict[str, Skill] = {}
            for track, config in tracks.items():
                track_dir = self.root / track
                skills[track] = {}
                if config.status == "planned":
                    continue
                try:
                    local = load_skills(track_dir / "skills.yaml", config)
                    duplicate = skill_index.keys() & local.keys()
                    if duplicate:
                        raise ValueError(f"技能 id 跨线重复：{', '.join(sorted(duplicate))}")
                    skills[track] = local
                    skill_index.update(local)
                except Exception as exc:  # noqa: BLE001 - 坏文件只记录，不让服务挂掉
                    errors.append(LoadError(str(track_dir / "skills.yaml"), str(exc)))
                for yaml_path in sorted(track_dir.glob("*/*/problem.yaml")):
                    if yaml_path.parent.parent.name.startswith("_") or yaml_path.parent.parent.name == "lessons":
                        continue
                    try:
                        problem = load_problem(yaml_path.parent, config)
                        if problem.id in problems:
                            raise ValueError(f"id 重复：{problem.id}")
                        problems[problem.id] = problem
                    except Exception as exc:  # noqa: BLE001
                        errors.append(LoadError(str(yaml_path.parent), str(exc)))
                for yaml_path in sorted(track_dir.glob("lessons/*/lesson.yaml")):
                    try:
                        meta = LessonMeta.model_validate(read_yaml(yaml_path))
                        if meta.track != track:
                            raise ValueError(f"课的学习线应为 {track}")
                        if meta.id != yaml_path.parent.name:
                            raise ValueError(f"id {meta.id} 和文件夹名 {yaml_path.parent.name} 不一致")
                        if meta.id in lessons:
                            raise ValueError(f"id 重复：{meta.id}")
                        for step in meta.steps:
                            if step.data is not None:
                                step.data = data_block(step.data, yaml_path.parent)
                        lesson = Lesson(meta=meta, path=yaml_path.parent)
                        twice = [sk for sk in meta.skills if sk in skill_lesson]
                        if twice:
                            raise ValueError(
                                "这些技能已经在别的 lesson 文件里讲过："
                                + ", ".join(f"{sk}（{skill_lesson[sk].id}）" for sk in twice)
                            )
                        lessons[meta.id] = lesson
                        for sk in meta.skills:
                            skill_lesson[sk] = lesson
                    except Exception as exc:  # noqa: BLE001
                        errors.append(LoadError(str(yaml_path.parent), str(exc)))
            ordered = sorted(problems.values(), key=lambda p: (p.track.order, p.track.id, p.sort_key))
            by_track: dict[str, list[Problem]] = {t: [] for t in tracks}
            for p in ordered:
                by_track[p.meta.track].append(p)
            self.tracks, self.skill_index, self._ordered, self._by_track = tracks, skill_index, ordered, by_track
            self.problems, self.lessons, self.skill_lesson, self.skills, self.errors, self._stamp = (
                problems, lessons, skill_lesson, skills, errors, stamp,
            )

    def ensure_fresh(self) -> None:
        """请求路径用的廉价版 refresh：不在请求里扫文件。"""
        mode = os.environ.get("CODE_DOJO_BANK_WATCH", "3").strip().lower()
        if mode == "sync":
            self.refresh()
            return
        if self._stamp is None:
            self.refresh(stamp=0.0 if mode == "off" else None)
        if mode != "off" and not self._watching:
            self._start_watch(float(mode))

    def _start_watch(self, interval: float) -> None:
        with self._lock:
            if self._watching:
                return
            self._watching = True

        def loop() -> None:
            while True:
                time.sleep(interval)
                self.refresh()  # 坏文件在 refresh 里记进 errors，不会抛出

        threading.Thread(target=loop, name="problem-bank-watch", daemon=True).start()

    def ordered(self, track: str | None = None) -> list[Problem]:
        """按学习顺序排好的题（共享列表，调用方不要修改）。"""
        self.ensure_fresh()
        return self._ordered if track is None else self._by_track[track]

    def get(self, problem_id: str) -> Problem | None:
        self.ensure_fresh()
        return self.problems.get(problem_id)

    def lesson_sections(self, problem: Problem, *, with_setup: bool = False) -> list[dict[str, Any]]:
        """一道题的"课"：新引入的技能放最前（new=True），然后是用到的技能；没有教学内容的技能只给知识卡。"""
        self.ensure_fresh()
        m = problem.meta
        order = ([m.skills.introduces] if m.skills.introduces else []) + [
            sk for sk in reversed(m.skills.requires) if sk != m.skills.introduces
        ]
        sections = []
        for sk in order:
            lesson = self.skill_lesson.get(sk)
            steps = [st.model_dump(exclude_none=True) for st in lesson.meta.steps if st.skill == sk] if lesson else []
            if with_setup and lesson:
                for step in steps:
                    if step.get("db"):
                        step["setup"] = shared_db(lesson.path.parents[1], step["db"])
                        if step.get("patch"):
                            step["setup"].append(step["patch"])
            info = self.skill_index.get(sk)
            sections.append({
                "skill": sk,
                "name": info.name if info else sk,
                "card": info.card if info else "",
                "new": sk == m.skills.introduces,
                "lesson": lesson.meta.title if lesson else None,
                "steps": steps,
            })
        return sections
