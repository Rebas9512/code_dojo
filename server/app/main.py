"""code-dojo API。

本地运行：cd server && uv run uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import os
import threading
from contextlib import asynccontextmanager
from dataclasses import replace
from datetime import date
from collections import Counter, defaultdict
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from .ai import extra as extra_gen
from .ai import tutor
from .ai.provider import AIError, AIProvider, AgentId, ClaudeCodeProvider, CodexProvider, available_agents
from .auth import install_auth
from .config import load_settings
from .db import Store, ReviewConflict
from .frontend import Frontend
from .mastery import Exercise, Progress, weekly_stats
from .result_preview import compact_result
from .judge import Judge
from .problems import ExtraProblem, Problem, ProblemBank, build_extra, shared_db
from .sql_judge import sql_cases
from .sync import ProgressSync
from .tracks import Track
from .units import group_units, introduction_status, progress_frontier, stage_progress

settings = load_settings()
bank = ProblemBank(settings.problems_dir)
judge = Judge.from_settings(settings)
ai_slots = threading.BoundedSemaphore(2)
providers: dict[str, AIProvider] = {
    "claude": ClaudeCodeProvider(settings.claude_bin, settings.ai_model, settings.ai_workdir, slots=ai_slots),
    "codex": CodexProvider(settings.codex_bin, settings.codex_model, settings.ai_workdir, slots=ai_slots),
}


def select_agent(requested: AgentId | None) -> tuple[str, AIProvider]:
    for agent in available_agents(settings):
        if requested is None or agent["id"] == requested:
            return agent["id"], providers[agent["id"]]
    if requested:
        raise HTTPException(400, f"本机未启用 {requested.title()} 助教，请重新选择")
    raise HTTPException(503, "AI 助教没有开启")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    progress_sync.start()  # 第一次同步在后台跑，合并进来的记录会让 learning() 的缓存按版本号失效
    try:
        learning()  # 就绪前载入题库并算好进度，首页第一个请求不用等
        yield
    finally:
        progress_sync.close()


app = FastAPI(title="code-dojo", lifespan=lifespan, openapi_url=None if settings.auth_enabled else "/openapi.json")
if os.environ.get("CODE_DOJO_DESKTOP_PYTHON"):
    from .desktop_sql import router as desktop_sql
    app.include_router(desktop_sql)
install_auth(app, settings)
store = Store(settings.data_dir / "code_dojo.db")
progress_sync = ProgressSync(store, settings.sync_repo)


@app.get("/api/sync")
def sync_status() -> dict:
    return progress_sync.status()


@app.post("/api/sync")
def sync_now() -> dict:
    return progress_sync.sync()


class SqlCase(BaseModel):
    affected_rows: int | None = Field(default=None, ge=0)
    status: Literal["passed", "wrong_answer", "runtime_error", "timeout"]
    actual: dict | None = None
    expected: dict
    difference: dict | None = None
    error: str | None = None
    time_ms: int = Field(default=0, ge=0)


class SqlResult(BaseModel):
    verdict: Literal["accepted", "wrong_answer", "runtime_error", "timeout"]
    cases: list[SqlCase]


class ReviewRequest(BaseModel):
    review_source: str = ""
    review_due: str = ""


class RunRequest(ReviewRequest):
    sql_result: SqlResult | None = None
    code: str = Field(default="", max_length=100_000)
    answer: str | None = Field(default=None, max_length=20_000)  # 预测输出或看数据作答
    elapsed_ms: int | None = Field(default=None, ge=0)
    hints_used: int = Field(default=0, ge=0)
    ai_lines: int = Field(default=0, ge=0)  # 当前代码里应用过的 AI 修改建议行数

    def submitted_text(self, problem: Problem) -> str:
        if problem.meta.mode in ("inspect", "predict"):
            return self.answer or ""
        return self.code

    @field_validator("answer", mode="before")
    @classmethod
    def choice_index(cls, value: Any) -> Any:
        return str(value) if type(value) is int else value


class PlaygroundRequest(BaseModel):
    problem_id: str | None = None
    code: str = Field(default="", max_length=50_000)
    stdin: str = Field(default="", max_length=20_000)


class ChatRequest(ReviewRequest):
    agent: AgentId | None = None
    message: str = Field(min_length=1, max_length=4000)
    code: str = Field(default="", max_length=100_000)
    answer: str | None = Field(default=None, max_length=20_000)
    current: str | None = None  # 学生正在看的题：原题 id 或附加题 id（x-12）


class ExtraRequest(ReviewRequest):
    agent: AgentId | None = None
    practice_skill: str | None = None
    request: str = Field(default="", max_length=1000)


def summary(p: Problem, status: str | None = None) -> dict[str, Any]:
    m = p.meta
    return {
        "id": m.id,
        "title": m.title,
        "track": m.track,
        "stage": m.stage,
        "order": m.order,
        "week": m.week,
        "format": m.format,
        "mode": m.mode,
        "difficulty": m.difficulty,
        "skills": m.skills.model_dump(),
        "milestones": m.milestones,
        "leetcode": m.leetcode,
        "optional": m.optional,
        "status": status,
    }


def ref(p: Problem | None) -> dict[str, str] | None:
    return None if p is None else {"kind": "problem", "id": p.id, "title": p.meta.title}


def neighbors(track: str, problem_id: str) -> tuple[dict[str, str] | None, dict[str, str] | None]:
    ordered = bank.ordered(track)
    idx = next((i for i, q in enumerate(ordered) if q.id == problem_id), None)
    if idx is None:
        return None, None
    return ref(ordered[idx - 1] if idx > 0 else None), ref(ordered[idx + 1] if idx + 1 < len(ordered) else None)


def require(problem_id: str) -> Problem:
    """原题或附加题（x-12）。"""
    if problem_id.startswith("x-"):
        return require_extra(problem_id)
    p = bank.get(problem_id)
    if p is None:
        raise HTTPException(404, f"没有这道题：{problem_id}")
    return p


def require_parent(problem_id: str) -> Problem:
    if problem_id.startswith("x-"):
        raise HTTPException(400, "这里要原题的 id，不是附加题")
    return require(problem_id)


def require_extra(extra_id: str) -> ExtraProblem:
    try:
        row = store.get_extra(int(extra_id[2:]))
    except ValueError:
        row = None
    if row is None or row["deleted"]:
        raise HTTPException(404, f"没有这道附加题：{extra_id}")
    if row["status"] != "ready":
        raise HTTPException(409, "这道附加题还在出题中" if row["status"] == "generating" else "这道附加题出题失败了")
    parent = bank.get(row["parent_id"])
    if parent is None:
        raise HTTPException(404, f"附加题的原题不见了：{row['parent_id']}")
    return build_extra(parent, row["row_id"], row["seq"], row["spec"])


def extra_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {k: row[k] for k in ("id", "seq", "title", "status", "error", "request", "practice_skill", "created_at")}


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/api/judge/status")
def judge_status() -> dict[str, Any]:
    return {"judge_mode": judge.backends["python"], "judge_backends": judge.backends,
            "ds_state": judge.local.ds_state() if judge.backends["ds"] == "local" else "docker"}


@app.get("/api/status")
def status() -> dict[str, Any]:
    bank.ensure_fresh()
    agents = available_agents(settings)
    return {
        "ok": True,
        "problems": len(bank.problems),
        "load_errors": [e.__dict__ for e in bank.errors],
        "judge_image": settings.judge_image,
        "judge_image_present": judge.image_present() if judge.backends["python"] == "docker" else None,
        **judge_status(),
        "ai": agents[0]["id"] if agents else "off",
        "ai_model": agents[0]["model"] if agents else None,
        "ai_agents": agents,
    }


def require_track(track: str) -> Track:
    bank.ensure_fresh()
    if track not in bank.tracks:
        raise HTTPException(404, f"没有这条学习线：{track}")
    return bank.tracks[track]


@app.exception_handler(ReviewConflict)
async def review_conflict(_request: Request, exc: ReviewConflict) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


_learning: tuple[tuple, Progress] | None = None


def learning() -> Progress:
    """全部学习进度。按（题库版本、数据库写入次数、日期）缓存，没有新提交时各接口直接复用。"""
    global _learning
    bank.ensure_fresh()
    # 先取版本号再读数据：并发的重载或写入只会让缓存比版本号新，不会更旧。
    key = (bank, bank._stamp, store, store.version, date.today())
    if _learning is not None and _learning[0] == key:
        return _learning[1]
    catalog = [Exercise.from_problem(p) for p in bank.ordered()]
    parents = {p.id: p for p in catalog}
    for e in store.extra_catalog():
        if p := parents.get(e["parent_id"]):
            fmt = "predict" if e["mode"] == "predict" else ("write" if p.format == "predict" else p.format)
            extra = replace(p, id=e["id"], title=e["title"], format=fmt, parent=p.id, available=not e["deleted"])
            if e["review_format"]:
                refs = e["review_skills"]
                extra = replace(extra, format=e["review_format"], introduces=refs["introduces"], requires=tuple(refs["requires"]))
            if target := e["practice_skill"]:
                extra = replace(extra, introduces=None, requires=(target,))
            catalog.append(extra)
    store.initialize_reviews({p.id for p in catalog if p.counted})  # 只在首次读取时补排日程，写库后版本号会变
    key = key[:3] + (store.version, key[4])
    state = Progress(catalog, bank.skill_index, store.study_rows(), store.review_rows(), store.daily_limit(), key[4])
    _learning = (key, state)
    return state


def validate_review(req: ReviewRequest, p: Problem) -> None:
    if not req.review_source and not req.review_due:
        return
    state = learning()
    for r in state.queue:
        if r["problem_id"] == req.review_source and r["due"] == req.review_due:
            item = state.review_item(r)
            if not item["generate"] and item["id"] == p.id:
                return
    raise ReviewConflict("这道复习题已更新，请返回今日计划。")


@app.get("/api/today")
def today_plan() -> dict:
    ordered = bank.ordered()
    state = learning()
    return {"date": date.today(), "daily_limit": store.daily_limit(), "first_rate": state.rate,
            "first_count": len(state.recent), "reviews": [state.review_item(r) for r in state.queue],
            "tracks": [{"id": t.id, "name": t.name, "next": state.next_new(
                [p.id for p in ordered if p.meta.track == t.id])} for t in bank.tracks.values() if t.status == "active"]}


class PlanSettings(BaseModel):
    daily_limit: int = Field(ge=0, le=2**63 - 1)


@app.put("/api/today/settings")
def update_plan(req: PlanSettings) -> dict:
    store.set_limit(req.daily_limit)
    return {"daily_limit": req.daily_limit}


@app.get("/api/stats")
def stats() -> dict:
    state = learning()
    return {"weeks": weekly_stats(state.rows, state.exercises, date.today())}


@app.get("/api/tracks")
def tracks() -> list[dict[str, Any]]:
    ordered = bank.ordered()
    state = learning()
    statuses = {tid: store.status_by_problem(tid) for tid in bank.tracks}
    last_active = store.last_active_by_track()
    skill_status = introduction_status(ordered, statuses)
    rows = {}
    for track in bank.tracks.values():
        problems = bank.ordered(track.id)
        status = statuses.get(track.id, {})
        counts = Counter(status.get(p.id) for p in problems)
        stages = group_units(track, bank.skills[track.id], problems)
        upcoming = state.next_item([p.id for p in problems])
        rows[track.id] = {
            "id": track.id, "name": track.name, "summary": track.summary, "order": track.order,
            "language": track.language, "runtime": track.runtime, "status": track.status, "requires": track.requires,
            "stages": stage_progress(track, stages, status, skill_status, state),
            "mastered": sum(state.state(sid) == "mastered" for sid in bank.skills[track.id]),
            "skills": len(bank.skills[track.id]), "total": len(problems),
            "solved": counts["solved"] + counts["assisted"], "assisted": counts["assisted"],
            "attempted": counts["attempted"],
            "next": upcoming,
            "frontier": progress_frontier(stages, status),
            "last_active": last_active.get(track.id),
        }
    completed = {tid for tid, row in rows.items() if row["total"] > 0 and row["solved"] == row["total"]}
    for row in rows.values():
        row["requires_done"] = all(tid in completed for tid in row["requires"])
    return list(rows.values())


@app.get("/api/tracks/{track}/problems")
def track_problems(track: str) -> list[dict[str, Any]]:
    config = require_track(track)
    status = store.status_by_problem(track)
    ordered = bank.ordered(track)
    stages = group_units(config, bank.skills[track], ordered)
    unit_ids = {p.id: u.id for units in stages.values() for u in units for p in u.problems}
    return [dict(summary(p, status.get(p.id)), unit=unit_ids[p.id]) for p in ordered]


@app.get("/api/tracks/{track}/skills")
def track_skills(track: str) -> list[dict[str, Any]]:
    config = require_track(track)
    skills = bank.skills[track]
    if not skills:
        return []
    introductions: dict[str, list] = defaultdict(list)
    used_by: Counter[str] = Counter()
    statuses: dict[str, dict[str, str]] = {}
    ordered = bank.ordered()
    state = learning()
    for p in ordered:
        intro = p.meta.skills.introduces
        used_by.update(set(p.meta.skills.requires) - {intro})
        if intro in skills:
            if p.meta.track not in statuses:
                statuses[p.meta.track] = store.status_by_problem(p.meta.track)
            introductions[intro].append({
                "id": p.id, "title": p.meta.title, "format": p.meta.format, "status": statuses[p.meta.track].get(p.id),
            })
    stages = list(config.stages)
    out = []
    for s in sorted(skills.values(), key=lambda s: (stages.index(s.stage), s.group or 0)):
        lesson = bank.skill_lesson.get(s.id)
        out.append({
            "id": s.id, "name": s.name, "stage": s.stage, "group": s.group, "card": s.card,
            "prereqs": [{"id": pre.id, "name": pre.name, "track": pre.track}
                        for sid in s.prereqs if (pre := bank.skill_index.get(sid))],
            "lesson": {"id": lesson.id, "title": lesson.meta.title} if lesson else None,
            **state.states[s.id], "problems": introductions[s.id], "used_by": used_by[s.id],
        })
    return out


@app.get("/api/problems/{problem_id}")
def problem_detail(problem_id: str) -> dict[str, Any]:
    p = require(problem_id)
    m = p.meta
    prev, nxt = neighbors(m.track, p.id)
    state = learning()
    skills = bank.skill_index
    skill_ids = list(m.skills.requires) + ([m.skills.introduces] if m.skills.introduces else [])
    detail = summary(p, store.status_by_problem(m.track).get(p.id)) | {
        "language": p.track.language,
        "statement": p.statement,
        "starter": p.starter,
        "signature": m.signature,
        "entry": m.entry,
        "hints": m.hints,
        "examples": p.cases("examples"),
        "skill_cards": [
            {"id": sid, "name": skills[sid].name, "card": skills[sid].card, "new": sid == m.skills.introduces}
            for sid in skill_ids if sid in skills
        ],
        "stuck": state.stuck(Exercise.from_problem(p)),
        "continue_with": state.next_item([q.id for q in state.exercises.values() if q.track == m.track and not q.parent], p.id),
        "prev": prev,
        "next": nxt,
        "has_lesson": any(sec["steps"] for sec in bank.lesson_sections(p)),
        "parent": p.parent_id if isinstance(p, ExtraProblem) else None,
        "extra_seq": p.seq if isinstance(p, ExtraProblem) else None,
    }
    if p.inspect:
        detail["data"] = p.inspect.data
        detail["answer"] = {k: p.inspect.answer[k] for k in ("type", "options") if k in p.inspect.answer}
    if p.track.language == "python" and m.mode == "predict":
        detail["program"] = p.read("solution.py") or ""
    if not p.inspect and p.track.language == "sql":
        detail["datasets"] = m.datasets
        detail["ordered"] = m.ordered
    return detail


@app.get("/api/problems/{problem_id}/sql-cases")
def problem_sql_cases(problem_id: str, scope: Literal["sample", "all"] = "sample") -> dict:
    p = require(problem_id)
    if p.track.language != "sql" or p.inspect:
        raise HTTPException(400, "这道题不使用 SQL 数据集")
    try:
        return sql_cases(p, settings.data_dir, all_cases=scope == "all")
    except (ValueError, OSError) as exc:
        raise HTTPException(500, f"准备 SQL 数据集失败：{exc}") from exc


def judge_problem(p: Problem, req: RunRequest, which: str) -> dict[str, Any]:
    m = p.meta
    if p.inspect:
        if req.answer is None:
            raise HTTPException(400, "看数据作答题需要提交 answer")
        return p.inspect.grade(req.answer)
    if p.track.language == "sql":
        report = req.sql_result
        total = len(m.datasets) if which == "all" else 1
        if report is None or len(report.cases) != total:
            raise HTTPException(400, f"需要上报 {total} 个数据集的结果")
        cases = [c.model_dump() | {"hidden": i > 0} for i, c in enumerate(report.cases)]
        verdict = next((c.status for c in report.cases if c.status != "passed"), "accepted")
        if verdict != report.verdict:
            raise HTTPException(400, "判定与数据集结果不一致")
        return {"verdict": verdict, "cases": cases, "passed": sum(c.status == "passed" for c in report.cases),
                "total": total}
    if m.mode == "predict":
        if req.answer is None:
            raise HTTPException(400, "predict 题需要提交 answer")
        return judge.run(mode="predict", code=p.read("solution.py") or "", cases=[], answer=req.answer,
                         **p.judge_options())
    cases = p.cases(which)  # type: ignore[arg-type]
    result = judge.run(
        mode=m.mode or "function",
        code=req.code,
        cases=cases,
        **p.judge_options(),
    )
    n_examples = len(p.cases("examples"))
    for i, case in enumerate(result["cases"]):
        case["hidden"] = i >= n_examples
    return result


@app.post("/api/problems/{problem_id}/run")
def run(problem_id: str, req: RunRequest) -> dict[str, Any]:
    p = require(problem_id)
    validate_review(req, p)
    result = compact_result(judge_problem(p, req, "examples"))
    store.add_submission(problem_id=p.id, track=p.meta.track, kind="run", code=req.submitted_text(p),
                         result=result, elapsed_ms=req.elapsed_ms, hints_used=req.hints_used, ai_lines=req.ai_lines,
                         review_source=req.review_source, review_due=req.review_due)
    return result


@app.post("/api/problems/{problem_id}/submit")
def submit(problem_id: str, req: RunRequest) -> dict[str, Any]:
    p = require(problem_id)
    validate_review(req, p)
    result = compact_result(judge_problem(p, req, "all"))
    sid = store.add_submission(problem_id=p.id, track=p.meta.track, kind="review" if req.review_source else "submit",
                               code=req.submitted_text(p),
                               result=result, elapsed_ms=req.elapsed_ms, hints_used=req.hints_used,
                               ai_lines=req.ai_lines, counted=Exercise.from_problem(p).counted,
                               review_source=req.review_source, review_due=req.review_due)
    if result["verdict"] == "accepted":
        progress_sync.request()
    return result | {"submission_id": sid}


@app.post("/api/problems/{problem_id}/hints/{number}")
def use_hint(problem_id: str, number: int, req: ReviewRequest) -> dict:
    p = require(problem_id)
    validate_review(req, p)
    if not 1 <= number <= len(p.meta.hints):
        raise HTTPException(404, "没有这条提示")
    store.record_help(p.id, solution=False, source=req.review_source, due=req.review_due, author=number)
    return {"hint": p.meta.hints[number - 1]}


@app.post("/api/problems/{problem_id}/solution")
def show_solution(problem_id: str, req: ReviewRequest) -> dict:
    p = require(problem_id)
    validate_review(req, p)
    if p.inspect:
        answer = p.inspect.answer
        content = answer["options"][answer["correct"]] if answer["type"] == "choice" else answer["accept"][0]
        content += "\n" + p.inspect.explain
    elif p.meta.mode == "predict":
        result = judge_problem(p, RunRequest(answer=""), "all")
        if not result.get("cases"):
            raise HTTPException(503, "暂时无法运行参考程序")
        content = result["cases"][0]["expected"]
    else:
        content = p.read("solution.sql" if p.track.language == "sql" else "solution.py")
    if not content:
        raise HTTPException(404, "这道题没有题解")
    store.record_help(p.id, solution=True, source=req.review_source, due=req.review_due)
    return {"solution": content}


@app.get("/api/problems/{problem_id}/submissions")
def submissions(problem_id: str) -> list[dict[str, Any]]:
    require(problem_id)
    return store.submissions(problem_id)


# ---------- 课（每道题的"课"标签，problem-format v1.2） ----------

@app.get("/api/problems/{problem_id}/lesson")
def problem_lesson(problem_id: str) -> dict[str, Any]:
    p = require(problem_id)
    return {"sections": bank.lesson_sections(p, with_setup=True)}


@app.get("/api/playground/bookstore")
def playground_bookstore() -> list[str]:
    """SQL 看数据题没有自己的数据集，草稿用课里的书店库。"""
    return shared_db(bank.root / "sql", "bookstore")


@app.post("/api/playground/run")
def playground_run(req: PlaygroundRequest) -> dict[str, Any]:
    """运行一段 Python（课里的示例代码），只看输出、不判对错。"""
    runtime = "ds" if req.problem_id and require(req.problem_id).track.runtime == "ds" else "python"
    r = judge.run(mode="stdio", code=req.code, cases=[{"stdin": req.stdin, "expected": ""}],
                  runtime=runtime, time_limit_ms=3000 if runtime == "python" else None)
    if not r["cases"]:  # 语法错误、判题环境出错或整体超时
        return {"status": r["verdict"], "stdout": "", "error": r["error"], "time_ms": 0}
    c = r["cases"][0]
    status = "ok" if c["status"] in ("passed", "wrong_answer") else c["status"]
    return {"status": status, "stdout": c["actual"], "error": c["error"], "time_ms": c["time_ms"]}


# ---------- 附加题 ----------

def run_extra_job(provider: AIProvider, row_id: int, parent_id: str, request: str, practice_skill: str | None = None,
                  review_source: str = "") -> None:
    """后台线程：出题 + 验证，结果写回数据库。"""
    try:
        parent = bank.get(parent_id)
        existing = [e["title"] for e in store.extras(parent_id) if e["status"] == "ready" and e["title"]]
        skill_names = {sk.id: sk.name for sk in bank.skill_index.values()}
        allowed = None
        if review_source:
            parent = require(review_source)
            request += "。从初始代码独立作答，不要出预测、补全或改错题。"
        if practice_skill:
            state = learning()
            allowed = {sid for sid in bank.skill_index if state.state(sid) == "mastered"} | {practice_skill}
            refs = parent.meta.skills.model_copy(update={"introduces": None, "requires": [practice_skill]})
            parent = replace(parent, meta=parent.meta.model_copy(update={"skills": refs}))
        spec, notes = extra_gen.generate(provider, judge, parent, request=request, skill_names=skill_names, existing=existing,
                                        allowed=allowed, review=bool(review_source))
        if review_source:
            spec["review_format"] = "inspect" if parent.inspect else "variant"
            spec["review_skills"] = parent.meta.skills.model_dump()
        if practice_skill:
            spec["practice_skill"] = practice_skill
        store.finish_extra(row_id, spec, notes)
    except Exception as exc:  # noqa: BLE001 - 任何失败都记到这道附加题上，前端显示
        store.fail_extra(row_id, str(exc))


def start_extra(provider: AIProvider, parent: Problem, request: str, practice_skill: str | None = None,
                review_source: str = "") -> dict[str, Any]:
    row = store.create_extra(parent.id, request, practice_skill)
    threading.Thread(target=run_extra_job, args=(provider, row["row_id"], parent.id, request, practice_skill, review_source),
                     daemon=True).start()
    return extra_summary(row)


@app.get("/api/problems/{problem_id}/extras")
def list_extras(problem_id: str) -> list[dict[str, Any]]:
    p = require_parent(problem_id)
    return [extra_summary(e) for e in store.extras(p.id)]


@app.post("/api/problems/{problem_id}/extras")
def create_extra(problem_id: str, req: ExtraRequest) -> dict[str, Any]:
    parent = require_parent(problem_id)
    if req.practice_skill and req.practice_skill not in bank.skill_index:
        raise HTTPException(422, "没有这个练习技能")
    if req.review_source or req.review_due:
        state = learning()
        source = state.exercises.get(req.review_source)
        if source is None or (source.parent or source.id) != parent.id or not any(
            r["problem_id"] == source.id and r["due"] == req.review_due and state.review_item(r)["generate"]
            for r in state.queue
        ):
            raise ReviewConflict("复习计划已更新，请返回今日计划。")
    _, provider = select_agent(req.agent)
    return start_extra(provider, parent, req.request, req.practice_skill, req.review_source)


@app.delete("/api/problems/{problem_id}/extras/{seq}")
def delete_extra(problem_id: str, seq: int) -> dict[str, bool]:
    p = require_parent(problem_id)
    if not store.delete_extra(p.id, seq):
        raise HTTPException(404, f"没有附加题 {seq}")
    return {"ok": True}


# ---------- AI 助教 ----------

@app.get("/api/problems/{problem_id}/chat")
def chat_history(problem_id: str) -> list[dict[str, Any]]:
    require(problem_id)
    return store.chat(problem_id)


@app.post("/api/problems/{problem_id}/chat")
def chat_send(problem_id: str, req: ChatRequest) -> dict[str, Any]:
    """一道原题和它的附加题共用一段对话（记在原题 id 下）；current 指明学生正在看哪一道。"""
    parent = require_parent(problem_id)
    agent, provider = select_agent(req.agent)
    cur: Problem = parent
    label = "题目（原题）"
    if req.current and req.current != parent.id:
        cur = require(req.current)
        if not isinstance(cur, ExtraProblem) or cur.parent_id != parent.id:
            raise HTTPException(400, "current 不是这道题的附加题")
        label = f"附加题 {cur.seq}：{cur.meta.title}"
    validate_review(req, cur)
    history = store.chat(parent.id)
    user_msg = store.add_chat(parent.id, "user", req.message)
    skill_names = {s.id: s.name for s in bank.skill_index.values()}
    try:
        reply = tutor.ask(
            provider, cur,
            code=req.code, answer=req.answer,
            last_result=store.latest_result(cur.id),
            history=history, message=req.message,
            skill_names=skill_names,
            lesson=bank.lesson_sections(cur),
            applied_edits=store.applied_count(parent.id),
            effort=settings.ai_effort,
            current_label=label,
            extras=store.extras(parent.id),
        )
    except AIError as exc:
        raise HTTPException(502, f"AI 助教出错：{exc}") from exc
    new_extra = None
    if reply.make_extra:
        new_extra = start_extra(provider, parent, reply.make_extra)
    deleted = [seq for seq in reply.delete_extras if store.delete_extra(parent.id, seq)]
    notes = reply.notes + ([f"出附加题：{reply.make_extra}"] if new_extra else []) + (
        [f"删掉附加题：{deleted}"] if deleted else [])
    if not (new_extra or deleted):
        store.record_help(cur.id, solution=False, source=req.review_source, due=req.review_due)
    assistant_msg = store.add_chat(parent.id, "assistant", reply.reply, edits=reply.edits, notes=notes, agent=agent)
    return {"user": user_msg, "assistant": assistant_msg, "new_extra": new_extra, "deleted_extras": deleted}


@app.post("/api/problems/{problem_id}/chat/{message_id}/applied")
def chat_applied(problem_id: str, message_id: int) -> dict[str, bool]:
    """前端把助教的修改写进编辑框之后回报一声，用于统计"改过几次"。"""
    require(problem_id)
    if not store.mark_applied(problem_id, message_id):
        raise HTTPException(404, "这条消息没有修改")
    return {"ok": True}


@app.delete("/api/problems/{problem_id}/chat")
def chat_clear(problem_id: str) -> dict[str, bool]:
    require(problem_id)
    store.clear_chat(problem_id)
    return {"ok": True}


if settings.web_dist:
    app.mount("/", Frontend(settings.web_dist), name="web")
