"""按学习顺序、提交记录和复习队列计算掌握度与推荐。日期使用服务器本地日历。"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from .problems import Problem, Skill

INTERVALS = (1, 3, 7, 21, 60)


def local_day(timestamp: str) -> date:
    return datetime.fromisoformat(timestamp).astimezone().date()


@dataclass(frozen=True)
class Exercise:
    id: str
    title: str
    track: str
    format: str
    introduces: str | None
    requires: tuple[str, ...]
    difficulty: int
    parent: str | None = None
    available: bool = True

    @classmethod
    def from_problem(cls, p: Problem) -> 'Exercise':
        m = p.meta
        return cls(p.id, m.title, m.track, m.format, m.skills.introduces, tuple(m.skills.requires),
                   m.difficulty, getattr(p, "parent_id", None))

    @property
    def counted(self) -> bool:
        return self.format in ("write", "variant", "combine") or (self.track == "data" and self.format == "inspect")

    @property
    def skills(self) -> set[str]:
        return set(self.requires).union([self.introduces] if self.introduces else [])

    def link(self) -> dict:
        item = {"id": self.id, "title": self.title}
        return item | {"parent": self.parent} if self.parent else item


def independent(row: dict) -> bool:
    return row["verdict"] == "accepted" and not (row["hints_used"] or row["ai_lines"] or row["solution_seen"])


def schedule(day: date, step: int, success: bool, rewrite: bool = False) -> tuple[int, str]:
    # 重写成功相当于重新独立做对原题，次日开始第一轮复习。
    step = min(step + 1, len(INTERVALS) - 1) if success and not rewrite else 0
    return step, (day + timedelta(days=INTERVALS[step])).isoformat()


class Progress:
    def __init__(self, exercises: list[Exercise], skills: dict[str, Skill], rows: list[dict],
                 reviews: list[dict], limit: int, today: date):
        self.exercises = {p.id: p for p in exercises}
        self.rows = rows
        self.skills = skills
        self.rank: dict[str, int] = {}
        for i, p in enumerate(exercises):
            if p.introduces:
                self.rank.setdefault(p.introduces, i)
        self.first: dict[str, dict] = {}
        self.seen: set[str] = set()
        self.solved: set[str] = set()
        introduced: set[str] = set()
        credit: dict[str, set[str]] = defaultdict(set)
        last: dict[str, str] = {}
        for row in rows:
            if row["kind"] not in ("submit", "review"):
                continue
            p = self.exercises.get(row["problem_id"])
            if p is None:
                continue
            self.seen.add(p.id)
            first = row["kind"] == "submit" and p.id not in self.first
            if first:
                self.first[p.id] = row
            if row["verdict"] == "accepted":
                self.solved.add(p.id)
                if p.introduces:
                    introduced.add(p.introduces)
            for sid in p.skills:
                last[sid] = row["created_at"]
                if p.counted and (first or row["kind"] == "review") and independent(row):
                    credit[sid].add(p.id)

        due_skills, failed_skills = set(), set()
        self.queue: list[dict] = []
        remaining = limit - sum(r["last_reviewed"] == today.isoformat() for r in reviews)
        for r in sorted(reviews, key=lambda r: (r["due"] or "", r["problem_id"])):
            source = self.exercises.get(r["problem_id"])
            if source is None or not source.available:
                continue
            if r["result"] == "failed":
                failed_skills.update(source.skills)
            if r["due"] and r["due"] <= today.isoformat():
                due_skills.update(source.skills)
                if len(self.queue) < remaining:
                    self.queue.append(r)

        self.states = {}
        for sid in skills:
            count = len(credit[sid])
            used = last.get(sid)
            state = "unlearned"
            if sid in failed_skills:
                state = "review"
            elif count >= 2:
                stale = used and (today - local_day(used)).days >= 21
                state = "review" if stale or sid in due_skills else "mastered"
            elif sid in introduced or count:
                state = "learning"
            self.states[sid] = dict(state=state, counted_solves=count, last_used=used)
        self.learning = {sid for sid, s in self.states.items() if s["state"] == "learning"}
        self.recent = [r for pid, r in self.first.items() if self.exercises[pid].format != "predict"][-10:]
        self.rate = sum(r["verdict"] == "accepted" for r in self.recent) / len(self.recent) if self.recent else None

    def state(self, sid: str) -> str:
        return self.states.get(sid, {}).get("state", "unlearned")

    def focus(self, p: Exercise) -> str | None:
        return p.introduces or max(p.requires, key=lambda s: self.rank.get(s, -1), default=None)

    def eligible(self, p: Exercise) -> bool:
        if any(self.state(sid) == "unlearned" for sid in p.requires):
            return False
        if p.introduces:
            if self.state(p.introduces) == "unlearned" and len(self.learning) >= 3:
                return False
            skill = self.skills.get(p.introduces)
            if skill is None:
                return False
            for sid in skill.prereqs:
                if self.state(sid) == "unlearned" or (
                    self.skills[sid].track == p.track and self.state(sid) != "mastered"
                ):
                    return False
        return True

    def next_new(self, ids: list[str], exclude: str | None = None) -> dict | None:
        options = [self.exercises[pid] for pid in ids if pid != exclude and pid not in self.solved
                   and self.eligible(self.exercises[pid])]
        if len(self.learning) >= 3:
            practice = next((p for p in options if p.counted and p.skills & self.learning), None)
            if practice:
                return practice.link()
        return options[0].link() if options else None

    def review_item(self, r: dict) -> dict:
        source = self.exercises[r["problem_id"]]
        target = source
        generate = False
        retry_id = r.get("rewrite_target")
        retry = self.exercises.get(retry_id) if retry_id else None
        if retry and retry.available:
            target = retry
        elif source.counted and r["rounds"] > 0:
            focus = self.focus(source)
            candidates = [p for p in self.exercises.values() if p.available and p.track == source.track and p.counted
                          and p.id != source.id and p.id not in self.seen and self.focus(p) == focus
                          and (focus or p.parent)
                          and (not p.parent or p.parent == (source.parent or source.id))]
            target = min(candidates, key=lambda p: (bool(p.parent), p.introduces != focus), default=source)
            generate = target == source
        return target.link() | {"source": source.id, "due": r["due"], "step": r["step"],
                                "rewrite": r["result"] in ("rewrite", "failed"), "generate": generate}

    def next_item(self, ids: list[str], exclude: str | None = None) -> dict | None:
        due = next((r for r in self.queue if r["problem_id"] in ids
                    or self.exercises[r["problem_id"]].parent in ids), None)
        return self.review_item(due) if due else self.next_new(ids, exclude)

    def stuck(self, p: Exercise) -> dict | None:
        sid = self.focus(p)
        if not sid or sid not in self.skills:
            return None
        attempts = [r for pid, r in self.first.items()
                    if self.exercises[pid].counted and sid in self.exercises[pid].skills]
        twice = len(attempts) >= 2 and all(r["verdict"] != "accepted" for r in attempts[-2:])
        if not (twice or (len(self.recent) == 10 and self.rate is not None and self.rate < .7)):
            return None
        skill = self.skills[sid]
        prereqs = sorted(skill.prereqs, key=lambda pre: self.state(pre) == "mastered")
        target = next(iter(prereqs), sid)
        candidates = [q for q in self.exercises.values() if not q.parent and q.id != p.id and self.focus(q) == target]
        small = min(candidates, key=lambda q: (q.difficulty, q.id in self.solved), default=None)
        return {"skill": skill.name, "target_id": target, "target": self.skills[target].name if target in self.skills else skill.name,
                "problem": small.link() if small else None, "root": not prereqs}


def weekly_stats(rows: list[dict], exercises: dict[str, Exercise], today: date) -> list[dict[str, Any]]:
    monday = today - timedelta(days=today.weekday())
    weeks = {(monday - timedelta(weeks=i)).isoformat(): dict(first=0, passed=0, syntax=0, hints=0,
             elapsed=[], solves=0, assisted=0) for i in reversed(range(8))}
    seen, solved, hints = set(), set(), {}
    for r in rows:
        if r["kind"] != "submit":
            continue
        pid = r["problem_id"]
        day = local_day(r["created_at"])
        week = weeks.get((day - timedelta(days=day.weekday())).isoformat())
        ok = r["verdict"] == "accepted"
        if week:
            if pid not in seen and pid in exercises and exercises[pid].format != "predict":
                week["first"] += 1
                week["passed"] += ok
            week["syntax"] += r["syntax_error"]
            week["hints"] += max(0, r["hints_used"] - hints.get(pid, 0))
            if ok and pid not in solved and r["elapsed_ms"] is not None:
                week["elapsed"].append(r["elapsed_ms"])
            if ok:
                week["solves"] += 1
                week["assisted"] += bool(r["ai_lines"])
        hints[pid] = max(hints.get(pid, 0), r["hints_used"])
        seen.add(pid)
        if ok:
            solved.add(pid)
    return [dict(week=day, first_rate=w["passed"]/w["first"] if w["first"] else None,
                 syntax_errors=w["syntax"], hints=w["hints"],
                 elapsed_ms=sum(w["elapsed"])/len(w["elapsed"]) if w["elapsed"] else None,
                 ai_rate=w["assisted"]/w["solves"] if w["solves"] else None) for day, w in weeks.items()]
