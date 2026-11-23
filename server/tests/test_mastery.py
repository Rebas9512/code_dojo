from datetime import date

from app.mastery import Exercise, Progress, schedule, weekly_stats
from app.problems import Skill

DAY = date(2026, 11, 22)


def problem(pid, intro=None, requires=(), fmt="write", track="python"):
    return Exercise(pid, pid, track, fmt, intro, tuple(requires), 1)


def attempt(pid, verdict="accepted", **kw):
    return dict(problem_id=pid, kind="submit", verdict=verdict, created_at="2026-11-22T12:00:00+00:00",
                hints_used=0, ai_lines=0, solution_seen=0, elapsed_ms=12000, syntax_error=0) | kw


def skill(sid, prereqs=(), track="python"):
    return Skill(track, sid, sid, "0", list(prereqs), "", 1)


def progress(problems, skills, rows, reviews=(), today=DAY, limit=5):
    return Progress(problems, {s.id: s for s in skills}, rows, list(reviews), limit, today)


def test_distinct_first_independent_solves_and_last_use():
    ps = [problem(str(i), "x") for i in range(7)] + [problem("fix", "x", fmt="fix")]
    rows = [attempt("0", "wrong_answer"), attempt("0"), attempt("1", ai_lines=1),
            attempt("2", hints_used=1), attempt("3", solution_seen=1), attempt("fix"), attempt("4"), attempt("4")]
    def state(rows, **kw):
        return progress(ps, [skill("x")], rows, **kw).states["x"]
    assert state(rows) == dict(state="learning", counted_solves=1, last_used=rows[-1]["created_at"])
    rows.append(attempt("0", kind="review"))
    assert state(rows)["state"] == "mastered"
    assert state(rows, today=date(2026, 12, 13))["state"] == "review"
    r = dict(problem_id="4", due=str(DAY), last_reviewed=None, result="new", step=0, rounds=0)
    assert state(rows, reviews=[r])["state"] == "review"
    assert state(rows[:1], reviews=[r | dict(due="2026-11-23", result="failed")])["state"] == "review"


def test_root_inspect_and_all_skills_in_combine():
    ps = [problem("root", "x", fmt="inspect", track="data"), problem("sql", "x", fmt="inspect", track="sql"),
          problem("both", "y", ["x"], "combine")]
    p = progress(ps, [skill("x"), skill("y")], [attempt(q.id) for q in ps])
    assert [p.states[s]["counted_solves"] for s in ("x", "y")] == [2, 1]


def test_selection_prerequisites_and_global_learning_limit():
    skills = [skill("base", track="data"), skill("x"), skill("y", ["base"]), skill("z", ["x"]), skill("w")]
    ps = [problem("base", "base", fmt="inspect", track="data"), problem("x", "x"), problem("y", "y"),
          problem("z", "z"), problem("w", "w"), problem("practice", requires=["x"])]
    ids = [p.id for p in ps[2:]]
    assert progress(ps, skills, []).next_new(ids)["id"] == "w"
    rows = [attempt("base"), attempt("x")]
    assert progress(ps, skills, rows).next_new(ids)["id"] == "y"
    rows.append(attempt("y"))
    assert progress(ps, skills, rows).next_new(ids)["id"] == "practice"
    rows.append(attempt("practice"))
    assert progress(ps, skills, rows).next_new(ids)["id"] == "z"


def test_stuck_separate_triggers_and_first_attempt_window():
    ps = [problem(str(i), "x") for i in range(12)] + [problem("pre", "base"), problem("pred", "x", fmt="predict")]
    skills = [skill("x", ["base"]), skill("base")]
    rows = [attempt("0", "wrong_answer"), attempt("0"), attempt("pred", "wrong_answer")]
    assert progress(ps, skills, rows).stuck(ps[0]) is None
    rows.append(attempt("1", "wrong_answer"))
    assert progress(ps, skills, rows).stuck(ps[0])["problem"]["id"] == "pre"
    rows = [attempt(str(i), "wrong_answer" if i % 2 else "accepted") for i in range(10)]
    p = progress(ps, skills, rows)
    assert p.rate == .5 and p.stuck(ps[0])
    rows[1:2] = [attempt("1")]
    rows[3:4] = [attempt("3")]
    assert progress(ps, skills, rows).stuck(ps[0]) is None


def test_review_intervals_choice_and_daily_limit():
    days = [schedule(DAY, i, True)[1] for i in range(5)]
    assert days == ["2026-11-25", "2026-11-29", "2026-12-13", "2027-01-21", "2027-01-21"]
    assert schedule(DAY, 3, False) == schedule(DAY, 3, True, rewrite=True) == (0, "2026-11-23")
    ps = [problem("a", "x"), problem("variant", requires=["x"]), problem("intro", "x")]
    r = dict(problem_id="a", step=1, rounds=1, due=str(DAY), last_reviewed=None, result="passed")
    p = progress(ps, [skill("x")], [attempt("a")], [r])
    assert p.next_item(["a"])["id"] == "intro"
    assert p.review_item(r | {"step": 0, "rounds": 0})["id"] == "a"
    p = progress(ps, [skill("x")], [attempt(q.id) for q in ps], [r])
    assert p.review_item(r)["generate"]
    done = r | dict(problem_id="variant", due="2026-12-01", last_reviewed=str(DAY))
    assert not progress(ps, [skill("x")], [], [r, done], limit=1).queue


def test_weekly_stats_exclude_review_and_count_hints_once():
    ps = [problem("a"), problem("b")]
    rows = [attempt("a", "compile_error", syntax_error=1, hints_used=1), attempt("a", hints_used=2),
            attempt("b", ai_lines=2), attempt("b", kind="review", hints_used=3)]
    week = weekly_stats(rows, {p.id:p for p in ps}, DAY)[-1]
    assert week == dict(week="2026-11-16", first_rate=.5, syntax_errors=1, hints=2, elapsed_ms=12000, ai_rate=.5)
